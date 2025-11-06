from typing import Any, Optional

from src.constants.constants import AbortReason, DeviceState
from src.plugins.base import Plugin


class UIPlugin(Plugin):
    """UI Plug-in - Manage CLI/GUI display"""

    name = "ui"

    # Device status text mapping
    STATE_TEXT_MAP = {
        DeviceState.IDLE: "Standby",
        DeviceState.LISTENING: "Listening...",
        DeviceState.SPEAKING: "Talking...",
    }

    def __init__(self, mode: Optional[str] = None) -> None:
        super().__init__()
        self.app = None
        self.mode = (mode or "cli").lower()
        self.display = None
        self._is_gui = False
        self.is_first = True

    async def setup(self, app: Any) -> None:
        """Initialize UI plugin."""
        self.app = app

        # Create the corresponding display instance
        self.display = self._create_display()

        # Disable in-app console input
        if hasattr(app, "use_console_input"):
            app.use_console_input = False

    def _create_display(self):
        """Create a display instance based on the mode."""
        if self.mode == "gui":
            from src.display.gui_display import GuiDisplay

            self._is_gui = True
            return GuiDisplay()
        else:
            from src.display.cli_display import CliDisplay

            self._is_gui = False
            return CliDisplay()

    async def start(self) -> None:
        """Start the UI display."""
        if not self.display:
            return

        # Bind callback
        await self._setup_callbacks()

        # Start display
        self.app.spawn(self.display.start(), name=f"ui:{self.mode}:start")

    async def _setup_callbacks(self) -> None:
        """Set display callback."""
        if self._is_gui:
            # The GUI needs to be scheduled to asynchronous tasks
            callbacks = {
                "press_callback": self._wrap_callback(self._press),
                "release_callback": self._wrap_callback(self._release),
                "auto_callback": self._wrap_callback(self._auto_toggle),
                "abort_callback": self._wrap_callback(self._abort),
                "send_text_callback": self._send_text,
            }
        else:
            # CLI directly passes coroutine functions
            callbacks = {
                "auto_callback": self._auto_toggle,
                "abort_callback": self._abort,
                "send_text_callback": self._send_text,
            }

        await self.display.set_callbacks(**callbacks)

    def _wrap_callback(self, coro_func):
        """Wrap coroutine functions into schedulable lambdas."""
        return lambda: self.app.spawn(coro_func(), name="ui:callback")

    async def on_incoming_json(self, message: Any) -> None:
        """Process incoming JSON messages."""
        if not self.display or not isinstance(message, dict):
            return

        msg_type = message.get("type")

        # tts/stt both update text
        if msg_type in ("tts", "stt"):
            if text := message.get("text"):
                await self.display.update_text(text)

        # llm update expression
        elif msg_type == "llm":
            if emotion := message.get("emotion"):
                await self.display.update_emotion(emotion)

    async def on_device_state_changed(self, state: Any) -> None:
        """Device status change processing."""
        if not self.display:
            return

        # skip first call
        if self.is_first:
            self.is_first = False
            return

        # Update emoticons and status
        await self.display.update_emotion("neutral")
        if status_text := self.STATE_TEXT_MAP.get(state):
            await self.display.update_status(status_text, True)

    async def shutdown(self) -> None:
        """Clean up UI resources and close the window."""
        if self.display:
            await self.display.close()
            self.display = None

    # ===== Callback function =====

    async def _send_text(self, text: str):
        """Send text to the server."""
        if self.app.device_state == DeviceState.SPEAKING:
            audio_plugin = self.app.plugins.get_plugin("audio")
            if audio_plugin:
                await audio_plugin.codec.clear_audio_queue()
            await self.app.abort_speaking(None)
        if await self.app.connect_protocol():
            await self.app.protocol.send_wake_word_detected(text)

    async def _press(self):
        """Manual mode: Press to start recording."""
        await self.app.start_listening_manual()

    async def _release(self):
        """Manual mode: release to stop recording."""
        await self.app.stop_listening_manual()

    async def _auto_toggle(self):
        """Automatic mode switching."""
        await self.app.start_auto_conversation()

    async def _abort(self):
        """Interrupt the conversation."""
        await self.app.abort_speaking(AbortReason.USER_INTERRUPTION)
