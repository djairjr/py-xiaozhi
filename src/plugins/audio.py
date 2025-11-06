import asyncio
import os
from typing import Any

from src.audio_codecs.audio_codec import AudioCodec
from src.constants.constants import DeviceState, ListeningMode
from src.plugins.base import Plugin

# from src.utils.opus_loader import setup_opus
# setup_opus()


class AudioPlugin(Plugin):
    name = "audio"

    def __init__(self) -> None:
        super().__init__()
        self.app = None  # ApplicationExample
        self.codec: AudioCodec | None = None
        self._loop = None
        self._send_sem = asyncio.Semaphore(4)

    async def setup(self, app: Any) -> None:
        self.app = app
        self._loop = app._main_loop

        if os.getenv("XIAOZHI_DISABLE_AUDIO") == "1":
            return

        try:
            self.codec = AudioCodec()
            await self.codec.initialize()
            # Callback after recording encoding (from audio thread)
            self.codec.set_encoded_audio_callback(self._on_encoded_audio)
            # Exposed to applications for easy use by wake word plug-ins
            try:
                setattr(self.app, "audio_codec", self.codec)
            except Exception:
                pass
        except Exception:
            self.codec = None

    async def start(self) -> None:
        if self.codec:
            try:
                await self.codec.start_streams()
            except Exception:
                pass

    async def on_protocol_connected(self, protocol: Any) -> None:
        # Make sure the audio stream is started when the protocol is connected
        if self.codec:
            try:
                await self.codec.start_streams()
            except Exception:
                pass

    async def on_incoming_json(self, message: Any) -> None:
        # Example: Do not process
        await asyncio.sleep(0)

    async def on_incoming_audio(self, data: bytes) -> None:
        if self.codec:
            try:
                await self.codec.write_audio(data)
            except Exception:
                pass

    async def stop(self) -> None:
        """Stop audio streaming (leave codec instance)"""
        if self.codec:
            try:
                await self.codec.stop_streams()
            except Exception:
                pass

    async def shutdown(self) -> None:
        """Completely closes and releases audio resources."""
        if self.codec:
            try:
                # Make sure to stop the stream first and then close it (to prevent the callback from still executing)
                try:
                    await self.codec.stop_streams()
                except Exception:
                    pass

                # Close and release all audio resources
                await self.codec.close()
            except Exception:
                # Logged in codec.close()
                pass
            finally:
                # Clear references to help GC
                self.codec = None

        # Clear application references to break potential circular references
        if self.app and hasattr(self.app, "audio_codec"):
            try:
                self.app.audio_codec = None
            except Exception:
                pass

    # -------------------------
    # Internal: Send microphone audio
    # -------------------------
    def _on_encoded_audio(self, encoded_data: bytes) -> None:
        # Audio thread callback -> switch back to main loop
        try:
            if not self.app or not self._loop or not self.app.running:
                return
            if self._loop.is_closed():
                return
            self._loop.call_soon_threadsafe(self._schedule_send_audio, encoded_data)
        except Exception:
            pass

    def _schedule_send_audio(self, encoded_data: bytes) -> None:
        if not self.app or not self.app.running or not self.app.protocol:
            return

        async def _send():
            async with self._send_sem:
                # Send microphone audio only in allowed device states
                try:
                    if not (
                        self.app.protocol
                        and self.app.protocol.is_audio_channel_opened()
                    ):
                        return
                    if self._should_send_microphone_audio():
                        await self.app.protocol.send_audio(encoded_data)
                except Exception:
                    pass

        # Task management handed over to application
        self.app.spawn(_send(), name="audio:send")

    def _should_send_microphone_audio(self) -> bool:
        """Aligned with the application state machine:

        - Sent when LISTENING
        - Sent when SPEAKING and AEC are on and keep_listening and REALTIME mode"""
        try:
            if not self.app:
                return False
            if self.app.device_state == DeviceState.LISTENING and not self.app.aborted:
                return True
            return (
                self.app.device_state == DeviceState.SPEAKING
                and getattr(self.app, "aec_enabled", False)
                and bool(getattr(self.app, "keep_listening", False))
                and getattr(self.app, "listening_mode", None) == ListeningMode.REALTIME
            )
        except Exception:
            return False
