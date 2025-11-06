"""Countdown timer service.

Manage the creation, execution, cancellation and status query of countdown tasks"""

import asyncio
import json
from asyncio import Task
from datetime import datetime, timedelta
from typing import Any, Dict, Optional

from src.utils.logging_config import get_logger

logger = get_logger(__name__)


class TimerService:
    """Countdown timer service, manages all countdown tasks."""

    def __init__(self):
        # Use a dictionary to store active timers, the key is timer_id and the value is a TimerTask object
        self._timers: Dict[int, "TimerTask"] = {}
        self._next_timer_id = 0
        # Use locks to protect access to _timers and _next_timer_id to ensure thread safety
        self._lock = asyncio.Lock()
        self.DEFAULT_DELAY = 5  # Default delay seconds

    async def start_countdown(
        self, command: str, delay: int = None, description: str = ""
    ) -> Dict[str, Any]:
        """Start a countdown task.

        Args:
            command: MCP tool call to be executed (JSON format string, including name and arguments fields)
            delay: delay time (seconds), default is 5 seconds
            description: task description

        Returns:
            Dict[str, Any]: Dictionary containing task information"""
        if delay is None:
            delay = self.DEFAULT_DELAY

        # Verification delay time
        try:
            delay = int(delay)
            if delay <= 0:
                logger.warning(
                    f"Supplied delay time {delay} is invalid, use default value {self.DEFAULT_DELAY} seconds"
                )
                delay = self.DEFAULT_DELAY
        except (ValueError, TypeError):
            logger.warning(
                f"The supplied delay '{delay}' is invalid, use default value {self.DEFAULT_DELAY} seconds"
            )
            delay = self.DEFAULT_DELAY

        # Verify command format
        try:
            json.loads(command)
        except json.JSONDecodeError:
            logger.error(f"Failed to start countdown: command format error, unable to parse JSON: {command}")
            return {
                "success": False,
                "message": f"The command format is incorrect and JSON cannot be parsed: {command}",
            }

        # Get the current event loop
        loop = asyncio.get_running_loop()

        async with self._lock:
            timer_id = self._next_timer_id
            self._next_timer_id += 1

            # Create a countdown task
            timer_task = TimerTask(
                timer_id=timer_id,
                command=command,
                delay=delay,
                description=description,
                service=self,
            )

            # Create an asynchronous task
            task = loop.create_task(timer_task.run())
            timer_task.task = task

            self._timers[timer_id] = timer_task

        logger.info(f"Start countdown {timer_id}, command will be executed after {delay} seconds: {command}")

        return {
            "success": True,
            "message": f"Countdown {timer_id} has been started and will execute in {delay} seconds",
            "timer_id": timer_id,
            "delay": delay,
            "command": command,
            "description": description,
            "start_time": datetime.now().isoformat(),
            "estimated_execution_time": (
                datetime.now() + timedelta(seconds=delay)
            ).isoformat(),
        }

    async def cancel_countdown(self, timer_id: int) -> Dict[str, Any]:
        """Cancel the specified countdown task.

        Args:
            timer_id: the timer ID to be canceled

        Returns:
            Dict[str, Any]: Cancel result"""
        try:
            timer_id = int(timer_id)
        except (ValueError, TypeError):
            logger.error(f"Failed to cancel countdown: invalid timer_id {timer_id}")
            return {"success": False, "message": f"Invalid timer_id: {timer_id}"}

        async with self._lock:
            if timer_id in self._timers:
                timer_task = self._timers.pop(timer_id)
                if timer_task.task:
                    timer_task.task.cancel()

                logger.info(f"Countdown {timer_id} successfully canceled")
                return {
                    "success": True,
                    "message": f"Countdown {timer_id} canceled",
                    "timer_id": timer_id,
                    "cancelled_at": datetime.now().isoformat(),
                }
            else:
                logger.warning(f"Attempt to cancel countdown {timer_id} that does not exist or has completed")
                return {
                    "success": False,
                    "message": f"Event countdown with ID {timer_id} not found",
                    "timer_id": timer_id,
                }

    async def get_active_timers(self) -> Dict[str, Any]:
        """Get the status of all active countdown tasks.

        Returns:
            Dict[str, Any]: list of active timers"""
        async with self._lock:
            active_timers = []
            current_time = datetime.now()

            for timer_id, timer_task in self._timers.items():
                remaining_time = timer_task.get_remaining_time()
                if remaining_time > 0:
                    active_timers.append(
                        {
                            "timer_id": timer_id,
                            "command": timer_task.command,
                            "description": timer_task.description,
                            "delay": timer_task.delay,
                            "remaining_seconds": remaining_time,
                            "start_time": timer_task.start_time.isoformat(),
                            "estimated_execution_time": timer_task.execution_time.isoformat(),
                            "progress": timer_task.get_progress(),
                        }
                    )

            return {
                "success": True,
                "total_active_timers": len(active_timers),
                "timers": active_timers,
                "current_time": current_time.isoformat(),
            }

    async def cleanup_timer(self, timer_id: int):
        """Removes completed timers from the manager."""
        async with self._lock:
            if timer_id in self._timers:
                del self._timers[timer_id]
                logger.debug(f"Cleanup completed countdown {timer_id}")

    async def cleanup_all(self):
        """Clean up all countdown tasks (called when the app is closed)"""
        logger.info("Cleaning up all countdown tasks...")
        async with self._lock:
            active_timer_ids = list(self._timers.keys())
            for timer_id in active_timer_ids:
                if timer_id in self._timers:
                    timer_task = self._timers.pop(timer_id)
                    if timer_task.task:
                        timer_task.task.cancel()
                    logger.info(f"Countdown task {timer_id} canceled")
        logger.info("Countdown task cleanup completed")


class TimerTask:
    """A single countdown task."""

    def __init__(
        self,
        timer_id: int,
        command: str,
        delay: int,
        description: str,
        service: TimerService,
    ):
        self.timer_id = timer_id
        self.command = command
        self.delay = delay
        self.description = description
        self.service = service
        self.start_time = datetime.now()
        self.execution_time = self.start_time + timedelta(seconds=delay)
        self.task: Optional[Task] = None

    async def run(self):
        """Execute countdown task."""
        try:
            # Wait delay time
            await asyncio.sleep(self.delay)

            # execute command
            await self._execute_command()

        except asyncio.CancelledError:
            logger.info(f"Countdown {self.timer_id} is canceled")
        except Exception as e:
            logger.error(f"An error occurred during the execution of countdown {self.timer_id}: {e}", exc_info=True)
        finally:
            # clean up after yourself
            await self.service.cleanup_timer(self.timer_id)

    async def _execute_command(self):
        """Execute the command after the countdown ends."""
        logger.info(f"The countdown {self.timer_id} is over, ready to execute the MCP tool: {self.command}")

        try:
            # Parse MCP tool call command
            command_dict = json.loads(self.command)

            # Verify command format (MCP tool calling format)
            if "name" not in command_dict or "arguments" not in command_dict:
                raise ValueError("MCP command format is incorrect, must contain 'name' and 'arguments' fields")

            tool_name = command_dict["name"]
            arguments = command_dict["arguments"]

            # Get the MCP server and execute the tool
            from src.mcp.mcp_server import McpServer

            mcp_server = McpServer.get_instance()

            # Find tool
            tool = None
            for t in mcp_server.tools:
                if t.name == tool_name:
                    tool = t
                    break

            if not tool:
                raise ValueError(f"MCP tool does not exist: {tool_name}")

            # Execute MCP tool
            result = await tool.call(arguments)

            # Parse results
            result_data = json.loads(result)
            is_success = not result_data.get("isError", False)

            if is_success:
                logger.info(
                    f"Countdown {self.timer_id} successfully executed the MCP tool, tool: {tool_name}"
                )
                await self._notify_execution_result(True, f"{tool_name} executed")
            else:
                error_text = result_data.get("content", [{}])[0].get("text", "unknown error")
                logger.error(f"Countdown {self.timer_id} failed to execute MCP tool: {error_text}")
                await self._notify_execution_result(False, error_text)

        except json.JSONDecodeError:
            error_msg = f"Countdown {self.timer_id}: MCP command format error, unable to parse JSON"
            logger.error(error_msg)
            await self._notify_execution_result(False, error_msg)
        except Exception as e:
            error_msg = f"Countdown {self.timer_id} Error while executing MCP tool: {e}"
            logger.error(error_msg, exc_info=True)
            await self._notify_execution_result(False, error_msg)

    async def _notify_execution_result(self, success: bool, result: Any):
        """Notify execution results (broadcast through TTS)"""
        try:
            from src.application import Application

            app = Application.get_instance()
            if success:
                message = f"Countdown {self.timer_id} execution completed"
                if self.description:
                    message = f"{self.description} execution completed"
            else:
                message = f"Countdown {self.timer_id} execution failed"
                if self.description:
                    message = f"{self.description} execution failed"

            print("Countdown:", message)
            await app._send_text_tts(message)
        except Exception as e:
            logger.warning(f"Notification countdown execution result failed: {e}")

    def get_remaining_time(self) -> float:
        """Get remaining time (seconds)"""
        now = datetime.now()
        remaining = (self.execution_time - now).total_seconds()
        return max(0, remaining)

    def get_progress(self) -> float:
        """Get the progress (floating point number between 0-1)"""
        elapsed = (datetime.now() - self.start_time).total_seconds()
        return min(1.0, elapsed / self.delay)


# Global service instance
_timer_service = None


def get_timer_service() -> TimerService:
    """Get the countdown timer service singleton."""
    global _timer_service
    if _timer_service is None:
        _timer_service = TimerService()
        logger.debug("Create a countdown timer service instance")
    return _timer_service
