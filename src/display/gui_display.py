# -*- coding: utf-8 -*-
"""GUI display module - implemented using QML."""

import asyncio
import os
import signal
from abc import ABCMeta
from pathlib import Path
from typing import Callable, Optional

from PyQt5.QtCore import QObject, Qt, QTimer, QUrl
from PyQt5.QtGui import QCursor, QFont
from PyQt5.QtQuickWidgets import QQuickWidget
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget

from src.display.base_display import BaseDisplay
from src.display.gui_display_model import GuiDisplayModel
from src.utils.resource_finder import find_assets_dir


# Create compatible metaclasses
class CombinedMeta(type(QObject), ABCMeta):
    pass


class GuiDisplay(BaseDisplay, QObject, metaclass=CombinedMeta):
    """GUI display class - modern interface based on QML"""

    # constant definition
    EMOTION_EXTENSIONS = (".gif", ".png", ".jpg", ".jpeg", ".webp")
    DEFAULT_WINDOW_SIZE = (880, 560)
    DEFAULT_FONT_SIZE = 12
    QUIT_TIMEOUT_MS = 3000

    def __init__(self):
        super().__init__()
        QObject.__init__(self)

        # Qt components
        self.app = None
        self.root = None
        self.qml_widget = None
        self.system_tray = None

        # data model
        self.display_model = GuiDisplayModel()

        # Expression management
        self._emotion_cache = {}
        self._last_emotion_name = None

        # Status management
        self.auto_mode = False
        self._running = True
        self.current_status = ""
        self.is_connected = True

        # Window drag state
        self._dragging = False
        self._drag_position = None

        # callback function mapping
        self._callbacks = {
            "button_press": None,
            "button_release": None,
            "mode": None,
            "auto": None,
            "abort": None,
            "send_text": None,
        }

    # =========================================================================
    # Public API - Callbacks and Updates
    # =========================================================================

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
        self._callbacks.update(
            {
                "button_press": press_callback,
                "button_release": release_callback,
                "mode": mode_callback,
                "auto": auto_callback,
                "abort": abort_callback,
                "send_text": send_text_callback,
            }
        )

    async def update_status(self, status: str, connected: bool):
        """Update status text and handle related logic."""
        self.display_model.update_status(status, connected)

        # Track status changes
        status_changed = status != self.current_status
        connected_changed = bool(connected) != self.is_connected

        if status_changed:
            self.current_status = status
        if connected_changed:
            self.is_connected = bool(connected)

        # Update system tray
        if (status_changed or connected_changed) and self.system_tray:
            self.system_tray.update_status(status, self.is_connected)

    async def update_text(self, text: str):
        """Update TTS text."""
        self.display_model.update_text(text)

    async def update_emotion(self, emotion_name: str):
        """Update emoticon display."""
        if emotion_name == self._last_emotion_name:
            return

        self._last_emotion_name = emotion_name
        asset_path = self._get_emotion_asset_path(emotion_name)

        # Convert a local file path to a QML usable URL (file:///...),
        # Non-files (such as emoji characters) are left intact.
        def to_qml_url(p: str) -> str:
            if not p:
                return ""
            if p.startswith(("qrc:/", "file:")):
                return p
            # Convert to file URL only if path exists, avoid treating emoji as path
            try:
                if os.path.exists(p):
                    return QUrl.fromLocalFile(p).toString()
            except Exception:
                pass
            return p

        url_or_text = to_qml_url(asset_path)
        self.display_model.update_emotion(url_or_text)

    async def update_button_status(self, text: str):
        """Update button state."""
        if self.auto_mode:
            self.display_model.update_button_text(text)

    async def toggle_mode(self):
        """Switch conversation mode."""
        if self._callbacks["mode"]:
            self._on_mode_button_click()
            self.logger.debug("Switched conversation mode via shortcut keys")

    async def toggle_window_visibility(self):
        """Toggle window visibility."""
        if not self.root:
            return

        if self.root.isVisible():
            self.logger.debug("Hide windows via shortcut keys")
            self.root.hide()
        else:
            self.logger.debug("Show windows via shortcut keys")
            self._show_main_window()

    async def close(self):
        """Close window handling."""
        self._running = False
        if self.system_tray:
            self.system_tray.hide()
        if self.root:
            self.root.close()

    # =========================================================================
    # Start process
    # =========================================================================

    async def start(self):
        """Start the GUI."""
        try:
            self._configure_environment()
            self._create_main_window()
            self._load_qml()
            self._setup_interactions()
            await self._finalize_startup()
        except Exception as e:
            self.logger.error(f"GUI startup failed: {e}", exc_info=True)
            raise

    def _configure_environment(self):
        """Configure the environment."""
        os.environ.setdefault("QT_LOGGING_RULES", "qt.qpa.fonts.debug=false")

        self.app = QApplication.instance()
        if self.app is None:
            raise RuntimeError("QApplication not found, please make sure you are running in a qasync environment")

        self.app.setQuitOnLastWindowClosed(False)
        self.app.setFont(QFont("PingFang SC", self.DEFAULT_FONT_SIZE))

        self._setup_signal_handlers()
        self._setup_activation_handler()

    def _create_main_window(self):
        """Create the main window."""
        self.root = QWidget()
        self.root.setWindowTitle("")
        self.root.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)

        # Calculate window size based on configuration
        window_size, is_fullscreen = self._calculate_window_size()
        self.root.resize(*window_size)

        # Save the status of whether it is full screen or not and use it when showing
        self._is_fullscreen = is_fullscreen

        self.root.closeEvent = self._closeEvent

    def _calculate_window_size(self) -> tuple:
        """Calculate the window size according to the configuration and return (width, height, full screen or not)"""
        try:
            from src.utils.config_manager import ConfigManager

            config_manager = ConfigManager.get_instance()
            window_size_mode = config_manager.get_config(
                "SYSTEM_OPTIONS.WINDOW_SIZE_MODE", "default"
            )

            # Get screen size (available area, exclude taskbar, etc.)
            desktop = QApplication.desktop()
            screen_rect = desktop.availableGeometry()
            screen_width = screen_rect.width()
            screen_height = screen_rect.height()

            # Calculate window size based on mode
            if window_size_mode == "default":
                # Default uses 50%
                width = int(screen_width * 0.5)
                height = int(screen_height * 0.5)
                is_fullscreen = False
            elif window_size_mode == "screen_75":
                width = int(screen_width * 0.75)
                height = int(screen_height * 0.75)
                is_fullscreen = False
            elif window_size_mode == "screen_100":
                # 100% use true full screen mode
                width = screen_width
                height = screen_height
                is_fullscreen = True
            else:
                # Unknown mode uses 50%
                width = int(screen_width * 0.5)
                height = int(screen_height * 0.5)
                is_fullscreen = False

            return ((width, height), is_fullscreen)

        except Exception as e:
            self.logger.error(f"Failed to calculate window size: {e}", exc_info=True)
            # Return to screen 50% on error
            try:
                desktop = QApplication.desktop()
                screen_rect = desktop.availableGeometry()
                return (
                    (int(screen_rect.width() * 0.5), int(screen_rect.height() * 0.5)),
                    False,
                )
            except Exception:
                return (self.DEFAULT_WINDOW_SIZE, False)

    def _load_qml(self):
        """Load the QML interface."""
        self.qml_widget = QQuickWidget()
        self.qml_widget.setResizeMode(QQuickWidget.SizeRootObjectToView)
        self.qml_widget.setClearColor(Qt.white)

        # Register the data model to the QML context
        qml_context = self.qml_widget.rootContext()
        qml_context.setContextProperty("displayModel", self.display_model)

        # Load QML file
        qml_file = Path(__file__).parent / "gui_display.qml"
        self.qml_widget.setSource(QUrl.fromLocalFile(str(qml_file)))

        # Set as the central widget of the main window
        layout = QVBoxLayout(self.root)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.qml_widget)

    def _setup_interactions(self):
        """Set up interactions (signals, trays)"""
        self._connect_qml_signals()

    async def _finalize_startup(self):
        """Complete the startup process."""
        await self.update_emotion("neutral")

        # Determine display mode based on configuration
        if getattr(self, "_is_fullscreen", False):
            self.root.showFullScreen()
        else:
            self.root.show()

        self._setup_system_tray()

    # =========================================================================
    # Signal connection
    # =========================================================================

    def _connect_qml_signals(self):
        """Connect QML signals to Python slots."""
        root_object = self.qml_widget.rootObject()
        if not root_object:
            self.logger.warning("QML root object not found, unable to set signal connection")
            return

        # Button event signal mapping
        button_signals = {
            "manualButtonPressed": self._on_manual_button_press,
            "manualButtonReleased": self._on_manual_button_release,
            "autoButtonClicked": self._on_auto_button_click,
            "abortButtonClicked": self._on_abort_button_click,
            "modeButtonClicked": self._on_mode_button_click,
            "sendButtonClicked": self._on_send_button_click,
            "settingsButtonClicked": self._on_settings_button_click,
        }

        # Title bar control signal mapping
        titlebar_signals = {
            "titleMinimize": self._minimize_window,
            "titleClose": self._quit_application,
            "titleDragStart": self._on_title_drag_start,
            "titleDragMoveTo": self._on_title_drag_move,
            "titleDragEnd": self._on_title_drag_end,
        }

        # Batch connection signals
        for signal_name, handler in {**button_signals, **titlebar_signals}.items():
            try:
                getattr(root_object, signal_name).connect(handler)
            except AttributeError:
                self.logger.debug(f"Signal {signal_name} does not exist (may be an optional feature)")

        self.logger.debug("QML signal connection setup completed")

    # =========================================================================
    # Button event handling
    # =========================================================================

    def _on_manual_button_press(self):
        """Manual mode button pressed."""
        self._dispatch_callback("button_press")

    def _on_manual_button_release(self):
        """Manual mode button release."""
        self._dispatch_callback("button_release")

    def _on_auto_button_click(self):
        """Auto mode button click."""
        self._dispatch_callback("auto")

    def _on_abort_button_click(self):
        """Abort button click."""
        self._dispatch_callback("abort")

    def _on_mode_button_click(self):
        """Click the conversation mode switch button."""
        if self._callbacks["mode"] and not self._callbacks["mode"]():
            return

        self.auto_mode = not self.auto_mode
        mode_text = "automatic conversation" if self.auto_mode else "Manual conversation"
        self.display_model.update_mode_text(mode_text)
        self.display_model.set_auto_mode(self.auto_mode)

    def _on_send_button_click(self, text: str):
        """Handles send text button clicks."""
        text = text.strip()
        if not text or not self._callbacks["send_text"]:
            return

        try:
            task = asyncio.create_task(self._callbacks["send_text"](text))
            task.add_done_callback(
                lambda t: t.cancelled()
                or not t.exception()
                or self.logger.error(
                    f"Exception in sending text task: {t.exception()}", exc_info=True
                )
            )
        except Exception as e:
            self.logger.error(f"Error sending text: {e}")

    def _on_settings_button_click(self):
        """Handles settings button clicks."""
        try:
            from src.views.settings import SettingsWindow

            settings_window = SettingsWindow(self.root)
            settings_window.exec_()
        except Exception as e:
            self.logger.error(f"Failed to open settings window: {e}", exc_info=True)

    def _dispatch_callback(self, callback_name: str, *args):
        """Generic callback scheduler."""
        callback = self._callbacks.get(callback_name)
        if callback:
            callback(*args)

    # =========================================================================
    # Window dragging
    # =========================================================================

    def _on_title_drag_start(self, _x, _y):
        """Title bar dragging begins."""
        self._dragging = True
        self._drag_position = QCursor.pos() - self.root.pos()

    def _on_title_drag_move(self, _x, _y):
        """Drag and move the title bar."""
        if self._dragging and self._drag_position:
            self.root.move(QCursor.pos() - self._drag_position)

    def _on_title_drag_end(self):
        """Title bar dragging ends."""
        self._dragging = False
        self._drag_position = None

    # =========================================================================
    # Expression management
    # =========================================================================

    def _get_emotion_asset_path(self, emotion_name: str) -> str:
        """Get the emoticon resource file path and automatically match common suffixes."""
        if emotion_name in self._emotion_cache:
            return self._emotion_cache[emotion_name]

        assets_dir = find_assets_dir()
        if not assets_dir:
            path = "😊"
        else:
            emotion_dir = assets_dir / "emojis"
            # Try to find emoticon files, fallback to neutral if failed
            path = (
                str(self._find_emotion_file(emotion_dir, emotion_name))
                or str(self._find_emotion_file(emotion_dir, "neutral"))
                or "😊"
            )

        self._emotion_cache[emotion_name] = path
        return path

    def _find_emotion_file(self, emotion_dir: Path, name: str) -> Optional[Path]:
        """Search for emoticon files in the specified directory."""
        for ext in self.EMOTION_EXTENSIONS:
            file_path = emotion_dir / f"{name}{ext}"
            if file_path.exists():
                return file_path
        return None

    # =========================================================================
    # System settings
    # =========================================================================

    def _setup_signal_handlers(self):
        """Set signal handler (Ctrl+C)"""
        try:
            signal.signal(
                signal.SIGINT,
                lambda *_: QTimer.singleShot(0, self._quit_application),
            )
        except Exception as e:
            self.logger.warning(f"Failed to set signal handler: {e}")

    def _setup_activation_handler(self):
        """Set the application activation handler (macOS Dock icon click to restore the window)"""
        try:
            import platform

            if platform.system() != "Darwin":
                return

            self.app.applicationStateChanged.connect(self._on_application_state_changed)
            self.logger.debug("App activation handler set (macOS Dock support)")
        except Exception as e:
            self.logger.warning(f"Failed to set application activation handler: {e}")

    def _on_application_state_changed(self, state):
        """Application state change handling (macOS Dock restores window when clicked)"""
        if state == Qt.ApplicationActive and self.root and not self.root.isVisible():
            QTimer.singleShot(0, self._show_main_window)

    def _setup_system_tray(self):
        """Set up the system tray."""
        if os.getenv("XIAOZHI_DISABLE_TRAY") == "1":
            self.logger.warning("System tray disabled via environment variable (XIAOZHI_DISABLE_TRAY=1)")
            return

        try:
            from src.views.components.system_tray import SystemTray

            self.system_tray = SystemTray(self.root)

            # Connect the tray signal (use QTimer to ensure main thread execution)
            tray_signals = {
                "show_window_requested": self._show_main_window,
                "settings_requested": self._on_settings_button_click,
                "quit_requested": self._quit_application,
            }

            for signal_name, handler in tray_signals.items():
                getattr(self.system_tray, signal_name).connect(
                    lambda h=handler: QTimer.singleShot(0, h)
                )

        except Exception as e:
            self.logger.error(f"Failed to initialize system tray component: {e}", exc_info=True)

    # =========================================================================
    # window control
    # =========================================================================

    def _show_main_window(self):
        """Show the main window."""
        if not self.root:
            return

        if self.root.isMinimized():
            self.root.showNormal()
        if not self.root.isVisible():
            self.root.show()
        self.root.activateWindow()
        self.root.raise_()

    def _minimize_window(self):
        """Minimize window."""
        if self.root:
            self.root.showMinimized()

    def _quit_application(self):
        """Exit the application."""
        self.logger.info("Starting to exit the application...")
        self._running = False

        if self.system_tray:
            self.system_tray.hide()

        try:
            from src.application import Application

            app = Application.get_instance()
            if not app:
                QApplication.quit()
                return

            loop = asyncio.get_event_loop()
            if not loop.is_running():
                QApplication.quit()
                return

            # Create a shutdown task and set a timeout
            shutdown_task = asyncio.create_task(app.shutdown())

            def on_shutdown_complete(task):
                if not task.cancelled() and task.exception():
                    self.logger.error(f"Application shutdown exception: {task.exception()}")
                else:
                    self.logger.info("Application closes gracefully")
                QApplication.quit()

            def force_quit():
                if not shutdown_task.done():
                    self.logger.warning("Close timeout, force exit")
                    shutdown_task.cancel()
                QApplication.quit()

            shutdown_task.add_done_callback(on_shutdown_complete)
            QTimer.singleShot(self.QUIT_TIMEOUT_MS, force_quit)

        except Exception as e:
            self.logger.error(f"Failed to close application: {e}")
            QApplication.quit()

    def _closeEvent(self, event):
        """Handle window close event."""
        # If the system tray is available, minimize to the tray
        if self.system_tray and (
            getattr(self.system_tray, "is_available", lambda: False)()
            or getattr(self.system_tray, "is_visible", lambda: False)()
        ):
            self.logger.info("Close window: minimize to tray")
            QTimer.singleShot(0, self.root.hide)
            event.ignore()
        else:
            QTimer.singleShot(0, self._quit_application)
            event.accept()
