import asyncio
from typing import Any


class Plugin:
    """Minimal plug-in base class: Provides asynchronous life cycle hooks. Overwrite as needed."""

    name: str = "plugin"

    def __init__(self) -> None:
        self._started = False

    async def setup(self, app: Any) -> None:
        """Plug-in preparation phase (called early in the application run)."""
        await asyncio.sleep(0)

    async def start(self) -> None:
        """Plugin startup (usually called after a protocol connection is established)."""
        self._started = True
        await asyncio.sleep(0)

    async def on_protocol_connected(self, protocol: Any) -> None:
        """Notification after the protocol channel is established."""
        await asyncio.sleep(0)

    async def on_incoming_json(self, message: Any) -> None:
        """Notification when a JSON message is received."""
        await asyncio.sleep(0)

    async def on_incoming_audio(self, data: bytes) -> None:
        """Notification when audio data is received."""
        await asyncio.sleep(0)

    async def on_device_state_changed(self, state: Any) -> None:
        """Device status change notification (broadcast by the application)."""
        await asyncio.sleep(0)

    async def stop(self) -> None:
        """Plugin stopped (called before shutdown is applied)."""
        self._started = False
        await asyncio.sleep(0)

    async def shutdown(self) -> None:
        """Plugin final cleanup (called during application shutdown)."""
        await asyncio.sleep(0)
