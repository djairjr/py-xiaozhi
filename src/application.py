import asyncio
import sys
import threading
from pathlib import Path
from typing import Any, Awaitable

# Allow running directly as a script: add the project root directory to sys.path (the upper level of src)
try:
    project_root = Path(__file__).resolve().parents[1]
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
except Exception:
    pass

from src.constants.constants import DeviceState, ListeningMode
from src.plugins.calendar import CalendarPlugin
from src.plugins.iot import IoTPlugin
from src.plugins.manager import PluginManager
from src.plugins.mcp import McpPlugin
from src.plugins.shortcuts import ShortcutsPlugin
from src.plugins.ui import UIPlugin
from src.plugins.wake_word import WakeWordPlugin
from src.protocols.mqtt_protocol import MqttProtocol
from src.protocols.websocket_protocol import WebsocketProtocol
from src.utils.config_manager import ConfigManager
from src.utils.logging_config import get_logger
from src.utils.opus_loader import setup_opus

logger = get_logger(__name__)
setup_opus()


class Application:
    _instance = None
    _lock = threading.Lock()

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = Application()
        return cls._instance

    def __init__(self):
        if Application._instance is not None:
            logger.error("Try to create multiple instances of Application")
            raise Exception("Application is a singleton class, please use get_instance() to get the instance")
        Application._instance = self

        logger.debug("Initialize Application instance")

        # Configuration
        self.config = ConfigManager.get_instance()

        # state
        self.running = False
        self.protocol = None

        # Device status (only the main program can rewrite, the plug-in can only read)
        self.device_state = DeviceState.IDLE
        try:
            aec_enabled_cfg = bool(self.config.get_config("AEC_OPTIONS.ENABLED", True))
        except Exception:
            aec_enabled_cfg = True
        self.aec_enabled = aec_enabled_cfg
        self.listening_mode = (
            ListeningMode.REALTIME if self.aec_enabled else ListeningMode.AUTO_STOP
        )
        self.keep_listening = False

        # Unified task pool (replaces _main_tasks/_bg_tasks)
        self._tasks: set[asyncio.Task] = set()

        # shutdown event
        self._shutdown_event: asyncio.Event | None = None

        # event loop
        self._main_loop: asyncio.AbstractEventLoop | None = None

        # Concurrency control
        self._state_lock: asyncio.Lock | None = None
        self._connect_lock: asyncio.Lock | None = None

        # plug-in
        self.plugins = PluginManager()

    # -------------------------
    # life cycle
    # -------------------------
    async def run(self, *, protocol: str = "websocket", mode: str = "gui") -> int:
        logger.info("Start Application, protocol=%s", protocol)
        try:
            self.running = True
            self._main_loop = asyncio.get_running_loop()
            self._initialize_async_objects()
            self._set_protocol(protocol)
            self._setup_protocol_callbacks()
            # Plug-in: setup (delay the import of AudioPlugin, ensure that the above setup_opus has been executed)
            from src.plugins.audio import AudioPlugin

            # Register audio, UI, MCP, IoT, wake words, shortcut keys and schedule plug-ins (UI mode is passed in from the run parameter)
            self.plugins.register(
                McpPlugin(),
                IoTPlugin(),
                AudioPlugin(),
                WakeWordPlugin(),
                CalendarPlugin(),
                UIPlugin(mode=mode),
                ShortcutsPlugin(),
            )
            await self.plugins.setup_all(self)
            # Broadcast the initial state after startup to ensure that "Standby" can be seen when the UI is ready
            try:
                await self.plugins.notify_device_state_changed(self.device_state)
            except Exception:
                pass
            # await self.connect_protocol()
            # Plugin: start
            await self.plugins.start_all()
            # Waiting for shutdown
            await self._wait_shutdown()
            return 0

        except Exception as e:
            logger.error(f"Application failed: {e}", exc_info=True)
            return 1
        finally:
            try:
                await self.shutdown()
            except Exception as e:
                logger.error(f"Error closing app: {e}")

    async def connect_protocol(self):
        """Make sure the protocol channel is open and broadcast once that the protocol is ready. Returns whether it is opened."""
        # Opened and return directly
        try:
            if self.is_audio_channel_opened():
                return True
            if not self._connect_lock:
                # When the lock is not initialized, try it directly.
                opened = await asyncio.wait_for(
                    self.protocol.open_audio_channel(), timeout=12.0
                )
                if not opened:
                    logger.error("Protocol connection failed")
                    return False
                logger.info("The protocol connection has been established. Press Ctrl+C to exit.")
                await self.plugins.notify_protocol_connected(self.protocol)
                return True

            async with self._connect_lock:
                if self.is_audio_channel_opened():
                    return True
                opened = await asyncio.wait_for(
                    self.protocol.open_audio_channel(), timeout=12.0
                )
                if not opened:
                    logger.error("Protocol connection failed")
                    return False
                logger.info("The protocol connection has been established. Press Ctrl+C to exit.")
                await self.plugins.notify_protocol_connected(self.protocol)
                return True
        except asyncio.TimeoutError:
            logger.error("Protocol connection timeout")
            return False

    def _initialize_async_objects(self) -> None:
        logger.debug("Initialize an asynchronous object")
        self._shutdown_event = asyncio.Event()
        self._state_lock = asyncio.Lock()
        self._connect_lock = asyncio.Lock()

    def _set_protocol(self, protocol_type: str) -> None:
        logger.debug("Set protocol type: %s", protocol_type)
        if protocol_type == "mqtt":
            self.protocol = MqttProtocol(asyncio.get_running_loop())
        else:
            self.protocol = WebsocketProtocol()

    # -------------------------
    # Manual listening (press and hold to talk)
    # -------------------------
    async def start_listening_manual(self) -> None:
        try:
            ok = await self.connect_protocol()
            if not ok:
                return
            self.keep_listening = False

            # If interrupt is sent while speaking
            if self.device_state == DeviceState.SPEAKING:
                logger.info("Send interruption while speaking")
                await self.protocol.send_abort_speaking(None)
                await self.set_device_state(DeviceState.IDLE)
            await self.protocol.send_start_listening(ListeningMode.MANUAL)
            await self.set_device_state(DeviceState.LISTENING)
        except Exception:
            pass

    async def stop_listening_manual(self) -> None:
        try:
            await self.protocol.send_stop_listening()
            await self.set_device_state(DeviceState.IDLE)
        except Exception:
            pass

    # -------------------------
    # Automatic/real-time conversation: select mode based on AEC and current configuration, enable persistent session
    # -------------------------
    async def start_auto_conversation(self) -> None:
        try:
            ok = await self.connect_protocol()
            if not ok:
                return

            mode = (
                ListeningMode.REALTIME if self.aec_enabled else ListeningMode.AUTO_STOP
            )
            self.listening_mode = mode
            self.keep_listening = True
            await self.protocol.send_start_listening(mode)
            await self.set_device_state(DeviceState.LISTENING)
        except Exception:
            pass

    def _setup_protocol_callbacks(self) -> None:
        self.protocol.on_network_error(self._on_network_error)
        self.protocol.on_incoming_json(self._on_incoming_json)
        self.protocol.on_incoming_audio(self._on_incoming_audio)
        self.protocol.on_audio_channel_opened(self._on_audio_channel_opened)
        self.protocol.on_audio_channel_closed(self._on_audio_channel_closed)

    async def _wait_shutdown(self) -> None:
        await self._shutdown_event.wait()

    # -------------------------
    # Unified task management (streamlined)
    # -------------------------
    def spawn(self, coro: Awaitable[Any], name: str) -> asyncio.Task:
        """Create tasks and register them, and cancel them when shutting down."""
        if not self.running or (self._shutdown_event and self._shutdown_event.is_set()):
            logger.debug(f"Skip task creation (app is closing): {name}")
            return None
        task = asyncio.create_task(coro, name=name)
        self._tasks.add(task)

        def _done(t: asyncio.Task):
            self._tasks.discard(t)
            if not t.cancelled() and t.exception():
                logger.error(f"Task {name} ended abnormally: {t.exception()}", exc_info=True)

        task.add_done_callback(_done)
        return task

    def schedule_command_nowait(self, fn, *args, **kwargs) -> None:
        """Simplified "immediate dispatch": throw any callable back to the main loop for execution.

        - If you return to the coroutine, a subtask will be automatically created for execution (fire-and-forget).
        - If it is a synchronous function, run it directly in the event loop thread (try to keep it as lightweight as possible)."""
        if not self._main_loop or self._main_loop.is_closed():
            logger.warning("Main event loop is not ready, refusing to schedule")
            return

        def _runner():
            try:
                res = fn(*args, **kwargs)
                if asyncio.iscoroutine(res):
                    self.spawn(res, name=f"call:{getattr(fn, '__name__', 'anon')}")
            except Exception as e:
                logger.error(f"Scheduled callable execution failed: {e}", exc_info=True)

        # Make sure to execute in the event loop thread
        self._main_loop.call_soon_threadsafe(_runner)

    # -------------------------
    # Protocol callback
    # -------------------------
    def _on_network_error(self, error_message=None):
        if error_message:
            logger.error(error_message)

        self.keep_listening = False
        # Request to close on error
        # if self._shutdown_event and not self._shutdown_event.is_set():
        #     self._shutdown_event.set()

    def _on_incoming_audio(self, data: bytes):
        logger.debug(f"Received binary message, length: {len(data)}")
        # Forward to plugin
        self.spawn(self.plugins.notify_incoming_audio(data), "plugin:on_audio")

    def _on_incoming_json(self, json_data):
        try:
            msg_type = json_data.get("type") if isinstance(json_data, dict) else None
            logger.info(f"Received JSON message: type={msg_type}")
            # Map TTS start/stop to device status (supports automatic/real-time and does not pollute manual mode)
            if msg_type == "tts":
                state = json_data.get("state")
                if state == "start":
                    # LISTENING is maintained during the start of TTS only when the session is maintained and in real-time mode; otherwise SPEAKING is displayed
                    if (
                        self.keep_listening
                        and self.listening_mode == ListeningMode.REALTIME
                    ):
                        self.spawn(
                            self.set_device_state(DeviceState.LISTENING),
                            "state:tts_start_rt",
                        )
                    else:
                        self.spawn(
                            self.set_device_state(DeviceState.SPEAKING),
                            "state:tts_start_speaking",
                        )
                elif state == "stop":
                    if self.keep_listening:
                        # Continue the conversation: Restart monitoring according to the current mode
                        async def _restart_listening():
                            try:
                                # REALTIME and no need to send again when LISTENING
                                if not (
                                    self.listening_mode == ListeningMode.REALTIME
                                    and self.device_state == DeviceState.LISTENING
                                ):
                                    await self.protocol.send_start_listening(
                                        self.listening_mode
                                    )
                            except Exception:
                                pass
                            self.keep_listening and await self.set_device_state(
                                DeviceState.LISTENING
                            )

                        self.spawn(_restart_listening(), "state:tts_stop_restart")
                    else:
                        self.spawn(
                            self.set_device_state(DeviceState.IDLE),
                            "state:tts_stop_idle",
                        )
            # Forward to plugin
            self.spawn(self.plugins.notify_incoming_json(json_data), "plugin:on_json")
        except Exception:
            logger.info("Receive JSON message")

    async def _on_audio_channel_opened(self):
        logger.info("The protocol channel is open")
        # After the channel is opened, enter LISTENING (: simplified to direct reading and writing)
        await self.set_device_state(DeviceState.LISTENING)

    async def _on_audio_channel_closed(self):
        logger.info("The protocol channel is closed")
        # Channel closes back to IDLE
        await self.set_device_state(DeviceState.IDLE)

    async def set_device_state(self, state: DeviceState):
        """Only called internally by the main program: Set device status. Please read-only access the plug-in."""
        # print(f"set_device_state: {state}")
        if not self._state_lock:
            self.device_state = state
            try:
                await self.plugins.notify_device_state_changed(state)
            except Exception:
                pass
            return
        async with self._state_lock:
            if self.device_state == state:
                return
            logger.info(f"Set device state: {state}")
            self.device_state = state
        # Broadcast outside the lock to avoid potential long-term blocking caused by plug-in callbacks
        try:
            await self.plugins.notify_device_state_changed(state)
            if state == DeviceState.LISTENING:
                await asyncio.sleep(0.5)
                self.aborted = False
        except Exception:
            pass

    # -------------------------
    # Read-only accessor (for plug-ins)
    # -------------------------
    def get_device_state(self):
        return self.device_state

    def is_idle(self) -> bool:
        return self.device_state == DeviceState.IDLE

    def is_listening(self) -> bool:
        return self.device_state == DeviceState.LISTENING

    def is_speaking(self) -> bool:
        return self.device_state == DeviceState.SPEAKING

    def get_listening_mode(self):
        return self.listening_mode

    def is_keep_listening(self) -> bool:
        return bool(self.keep_listening)

    def is_audio_channel_opened(self) -> bool:
        try:
            return bool(self.protocol and self.protocol.is_audio_channel_opened())
        except Exception:
            return False

    def get_state_snapshot(self) -> dict:
        return {
            "device_state": self.device_state,
            "listening_mode": self.listening_mode,
            "keep_listening": bool(self.keep_listening),
            "audio_opened": self.is_audio_channel_opened(),
        }

    async def abort_speaking(self, reason):
        """Stop speech output."""

        if self.aborted:
            logger.debug(f"Already aborted, ignore repeated abort requests: {reason}")
            return

        logger.info(f"Abort speech output, reason: {reason}")
        self.aborted = True
        await self.protocol.send_abort_speaking(reason)
        await self.set_device_state(DeviceState.IDLE)

    # -------------------------
    # UI auxiliary: directly called by plug-ins or tools
    # -------------------------
    def set_chat_message(self, role, message: str) -> None:
        """Forward text updates into a UI-recognizable JSON message (reusing UIPlugin's on_incoming_json).
        role:"assistant" | "user"Affects message type mapping."""
        try:
            msg_type = "tts" if str(role).lower() == "assistant" else "stt"
        except Exception:
            msg_type = "tts"
        payload = {"type": msg_type, "text": message}
        # Asynchronously dispatched via the plugin event bus
        self.spawn(self.plugins.notify_incoming_json(payload), "ui:text_update")

    def set_emotion(self, emotion: str) -> None:
        """Set emoticons: via UIPlugin’s on_incoming_json route."""
        payload = {"type": "llm", "emotion": emotion}
        self.spawn(self.plugins.notify_incoming_json(payload), "ui:emotion_update")

    # -------------------------
    # shut down
    # -------------------------
    async def shutdown(self):
        if not self.running:
            return
        logger.info("Closing Application...")
        self.running = False

        if self._shutdown_event is not None:
            self._shutdown_event.set()

        try:
            # Cancel all registration tasks
            if self._tasks:
                for t in list(self._tasks):
                    if not t.done():
                        t.cancel()
                await asyncio.gather(*self._tasks, return_exceptions=True)
                self._tasks.clear()

            # Close the protocol (limited time, avoid blocking exit)
            if self.protocol:
                try:
                    try:
                        self._main_loop.create_task(self.protocol.close_audio_channel())
                    except asyncio.TimeoutError:
                        logger.warning("Turn off protocol timeout, skip waiting")
                except Exception as e:
                    logger.error(f"Failed to close protocol: {e}")

            # Plug-in: stop/shutdown
            try:
                await self.plugins.stop_all()
            except Exception:
                pass
            try:
                await self.plugins.shutdown_all()
            except Exception:
                pass

            logger.info("Application close completed")
        except Exception as e:
            logger.error(f"Error closing app: {e}", exc_info=True)
