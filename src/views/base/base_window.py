# -*- coding: utf-8 -*-
"""Base Window Class - The base class for all PyQt windows
Supports asynchronous operations and qasync integration"""

import asyncio
from typing import Optional

from PyQt5.QtCore import QTimer, pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QWidget

from src.utils.logging_config import get_logger

logger = get_logger(__name__)


class BaseWindow(QMainWindow):
    """Base class for all windows, providing asynchronous support."""

    # Define signal
    window_closed = pyqtSignal()
    status_updated = pyqtSignal(str)

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.logger = get_logger(self.__class__.__name__)

        # Asynchronous task management
        self._tasks = set()
        self._shutdown_event = asyncio.Event()

        # Timers are used to update the UI periodically (in conjunction with asynchronous operations)
        self._update_timer = QTimer()
        self._update_timer.timeout.connect(self._on_timer_update)

        # Initialize UI
        self._setup_ui()
        self._setup_connections()
        self._setup_styles()

        self.logger.debug(f"{self.__class__.__name__} initialization completed")

    def _setup_ui(self):
        """Setup UI - subclass override"""

    def _setup_connections(self):
        """Set signal connection - subclass override"""

    def _setup_styles(self):
        """Setting styles - subclass override"""

    def _on_timer_update(self):
        """Timer update callback - subclass override"""

    def start_update_timer(self, interval_ms: int = 1000):
        """Start scheduled updates."""
        self._update_timer.start(interval_ms)
        self.logger.debug(f"Start scheduled update, interval: {interval_ms}ms")

    def stop_update_timer(self):
        """Stop scheduled updates."""
        self._update_timer.stop()
        self.logger.debug("Stop scheduled updates")

    def create_task(self, coro, name: str = None):
        """Create asynchronous tasks and manage them."""
        task = asyncio.create_task(coro, name=name)
        self._tasks.add(task)

        def done_callback(t):
            self._tasks.discard(t)
            if not t.cancelled() and t.exception():
                self.logger.error(f"Asynchronous task exception: {t.exception()}", exc_info=True)

        task.add_done_callback(done_callback)
        return task

    async def shutdown_async(self):
        """Close the window asynchronously."""
        self.logger.info("Start closing window asynchronously")

        # Set close event
        self._shutdown_event.set()

        # Stop timer
        self.stop_update_timer()

        # Cancel all tasks
        for task in self._tasks.copy():
            if not task.done():
                task.cancel()

        # Wait for task to complete
        if self._tasks:
            await asyncio.gather(*self._tasks, return_exceptions=True)

        self.logger.info("The window is closed asynchronously")

    def closeEvent(self, event):
        """Window close event."""
        self.logger.info("Window close event triggers")

        # Set close event flag
        self._shutdown_event.set()

        # If it is an activation window, cancel the activation process
        if hasattr(self, "device_activator") and self.device_activator:
            self.device_activator.cancel_activation()
            self.logger.info("Activation cancellation signal sent")

        # Send shutdown signal
        self.window_closed.emit()

        # Stop timer
        self.stop_update_timer()

        # Cancel all tasks (synchronous mode)
        for task in self._tasks.copy():
            if not task.done():
                task.cancel()

        # Accept closing event
        event.accept()

        self.logger.info("Window closing processing completed")

    def update_status(self, message: str):
        """Update status message."""
        self.status_updated.emit(message)
        self.logger.debug(f"Status update: {message}")

    def is_shutdown_requested(self) -> bool:
        """Check if shutdown is requested."""
        return self._shutdown_event.is_set()
