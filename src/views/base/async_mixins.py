# -*- coding: utf-8 -*-
"""The Mixin class for asynchronous operations provides the bridging function between Qt components and asynchronous operations."""

import asyncio

from PyQt5.QtCore import QObject, pyqtSignal

from src.utils.logging_config import get_logger

logger = get_logger(__name__)


class AsyncMixin:
    """Asynchronous operation Mixin class."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._async_tasks = set()
        self.logger = get_logger(self.__class__.__name__)

    def run_async(self, coro, callback=None, error_callback=None):
        """Run asynchronous coroutines in Qt environment."""
        task = asyncio.create_task(coro)
        self._async_tasks.add(task)

        def done_callback(future):
            self._async_tasks.discard(future)
            try:
                result = future.result()
                if callback:
                    callback(result)
            except Exception as e:
                self.logger.error(f"Asynchronous task execution failed: {e}", exc_info=True)
                if error_callback:
                    error_callback(e)

        task.add_done_callback(done_callback)
        return task

    async def cleanup_async_tasks(self):
        """Clean up all asynchronous tasks."""
        if self._async_tasks:
            for task in self._async_tasks.copy():
                if not task.done():
                    task.cancel()

            await asyncio.gather(*self._async_tasks, return_exceptions=True)
            self._async_tasks.clear()


class AsyncSignalEmitter(QObject):
    """Asynchronous signal transmitter."""

    # Define common signals
    data_ready = pyqtSignal(object)
    error_occurred = pyqtSignal(str)
    progress_updated = pyqtSignal(int)
    status_changed = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.logger = get_logger(self.__class__.__name__)

    def emit_data(self, data):
        """Transmit data signals."""
        self.data_ready.emit(data)

    def emit_error(self, error_message: str):
        """Send an error signal."""
        self.error_occurred.emit(error_message)

    def emit_progress(self, progress: int):
        """Emit a progress signal."""
        self.progress_updated.emit(progress)

    def emit_status(self, status: str):
        """Emit status signals."""
        self.status_changed.emit(status)
