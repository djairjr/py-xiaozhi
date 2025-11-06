"""Countdown timer MCP utility function.

Asynchronous tool functions provided to the MCP server"""

import json
from typing import Any, Dict

from src.utils.logging_config import get_logger

from .timer_service import get_timer_service

logger = get_logger(__name__)


async def start_countdown_timer(args: Dict[str, Any]) -> str:
    """Start a countdown task.

    Args:
        args: a dictionary containing the following arguments
            - command: MCP tool call to be executed (JSON format string, including name and arguments fields)
            - delay: delay time (seconds), optional, default is 5 seconds
            - description: task description, optional

    Returns:
        str: result string in JSON format"""
    try:
        command = args["command"]
        delay = args.get("delay")
        description = args.get("description", "")

        logger.info(f"[TimerTools] Start countdown - command: {command}, delay: {delay} seconds")

        timer_service = get_timer_service()
        result = await timer_service.start_countdown(
            command=command, delay=delay, description=description
        )

        logger.info(f"[TimerTools] Countdown start result: {result['success']}")
        return json.dumps(result, ensure_ascii=False, indent=2)

    except KeyError as e:
        error_msg = f"Missing required parameter: {e}"
        logger.error(f"[TimerTools] {error_msg}")
        return json.dumps({"success": False, "message": error_msg}, ensure_ascii=False)
    except Exception as e:
        error_msg = f"Failed to start countdown: {str(e)}"
        logger.error(f"[TimerTools] {error_msg}", exc_info=True)
        return json.dumps({"success": False, "message": error_msg}, ensure_ascii=False)


async def cancel_countdown_timer(args: Dict[str, Any]) -> str:
    """Cancel the specified countdown task.

    Args:
        args: a dictionary containing the following arguments
            - timer_id: the timer ID to be canceled

    Returns:
        str: result string in JSON format"""
    try:
        timer_id = args["timer_id"]

        logger.info(f"[TimerTools] Cancel countdown {timer_id}")

        timer_service = get_timer_service()
        result = await timer_service.cancel_countdown(timer_id)

        logger.info(f"[TimerTools] Countdown cancellation result: {result['success']}")
        return json.dumps(result, ensure_ascii=False, indent=2)

    except KeyError as e:
        error_msg = f"Missing required parameter: {e}"
        logger.error(f"[TimerTools] {error_msg}")
        return json.dumps({"success": False, "message": error_msg}, ensure_ascii=False)
    except Exception as e:
        error_msg = f"Failed to cancel countdown: {str(e)}"
        logger.error(f"[TimerTools] {error_msg}", exc_info=True)
        return json.dumps({"success": False, "message": error_msg}, ensure_ascii=False)


async def get_active_countdown_timers(args: Dict[str, Any]) -> str:
    """Get the status of all active countdown tasks.

    Args:
        args: empty dictionary (this function requires no parameters)

    Returns:
        str: list of active timers in JSON format"""
    try:
        logger.info("[TimerTools] Get event countdown list")

        timer_service = get_timer_service()
        result = await timer_service.get_active_timers()

        logger.info(f"[TimerTools] Current number of active countdowns: {result['total_active_timers']}")
        return json.dumps(result, ensure_ascii=False, indent=2)

    except Exception as e:
        error_msg = f"Failed to get event countdown: {str(e)}"
        logger.error(f"[TimerTools] {error_msg}", exc_info=True)
        return json.dumps({"success": False, "message": error_msg}, ensure_ascii=False)
