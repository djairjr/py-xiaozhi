from abc import ABC, abstractmethod
from typing import Callable, Optional

from src.utils.logging_config import get_logger


class BaseDisplay(ABC):
    """Abstract base class for display interfaces."""

    def __init__(self):
        self.logger = get_logger(self.__class__.__name__)

    @abstractmethod
    async def set_callbacks(
        self,
        press_callback: Optional[Callable] = None,
        release_callback: Optional[Callable] = None,
        mode_callback: Optional[Callable] = None,
        auto_callback: Optional[Callable] = None,
        abort_callback: Optional[Callable] = None,
        send_text_callback: Optional[Callable] = None,
    ):
        """Set the callback function."""

    @abstractmethod
    async def update_button_status(self, text: str):
        """Update button state."""

    @abstractmethod
    async def update_status(self, status: str, connected: bool):
        """Update status text."""

    @abstractmethod
    async def update_text(self, text: str):
        """Update TTS text."""

    @abstractmethod
    async def update_emotion(self, emotion_name: str):
        """Update emoticons."""

    @abstractmethod
    async def start(self):
        """Start display."""

    @abstractmethod
    async def close(self):
        """Turn off display."""
