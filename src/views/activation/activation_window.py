# -*- coding: utf-8 -*-
"""The device activation window displays the activation process, device information and activation progress."""

from pathlib import Path
from typing import Optional

from PyQt5.QtCore import QSize, Qt, QUrl, pyqtSignal
from PyQt5.QtGui import QPainterPath, QRegion
from PyQt5.QtQuickWidgets import QQuickWidget
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget

from src.core.system_initializer import SystemInitializer
from src.utils.device_activator import DeviceActivator
from src.utils.logging_config import get_logger

from ..base.async_mixins import AsyncMixin, AsyncSignalEmitter
from ..base.base_window import BaseWindow
from .activation_model import ActivationModel

logger = get_logger(__name__)


class ActivationWindow(BaseWindow, AsyncMixin):
    """Device activation window."""

    # Custom signal
    activation_completed = pyqtSignal(bool)  # Activate completion signal
    window_closed = pyqtSignal()  # window close signal

    def __init__(
        self,
        system_initializer: Optional[SystemInitializer] = None,
        parent: Optional = None,
    ):
        # QML related - must be created before super().__init__
        self.qml_widget = None
        self.activation_model = ActivationModel()

        super().__init__(parent)

        # Component instance
        self.system_initializer = system_initializer
        self.device_activator: Optional[DeviceActivator] = None

        # Status management
        self.current_stage = None
        self.activation_data = None
        self.is_activated = False
        self.initialization_started = False
        self.status_message = ""

        # Asynchronous signal transmitter
        self.signal_emitter = AsyncSignalEmitter()
        self._setup_signal_connections()

        # Window drag related
        self.drag_position = None

        # Delayed startup initialization (after the event loop has run)
        self.start_update_timer(100)  # Initialization starts after 100ms

    def _setup_ui(self):
        """Setup UI."""
        # Set up a borderless window
        # Detect display server type for Wayland compatibility
        import os

        is_wayland = (
            os.environ.get("WAYLAND_DISPLAY")
            or os.environ.get("XDG_SESSION_TYPE") == "wayland"
        )

        if is_wayland:
            # Wayland environment: don't use WindowStaysOnTopHint (not supported)
            self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
            self.logger.info("Wayland environment detected, using compatible window flag")
        else:
            # X11 environment: use full features
            self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
            self.logger.info("X11 environment detected, using full window flag")

        self.setAttribute(Qt.WA_TranslucentBackground)

        # Create a central widget
        central_widget = QWidget()
        central_widget.setStyleSheet("background: transparent;")
        self.setCentralWidget(central_widget)

        # Create layout
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)

        # Create QML widget
        self.qml_widget = QQuickWidget()
        self.qml_widget.setResizeMode(QQuickWidget.SizeRootObjectToView)

        # Use WA_AlwaysStackOnTop only in X11 environment (not supported in Wayland)
        if not is_wayland:
            self.qml_widget.setAttribute(Qt.WA_AlwaysStackOnTop)

        self.qml_widget.setClearColor(Qt.transparent)

        # Register the data model to the QML context
        qml_context = self.qml_widget.rootContext()
        qml_context.setContextProperty("activationModel", self.activation_model)

        # Load QML file
        qml_file = Path(__file__).parent / "activation_window.qml"
        self.qml_widget.setSource(QUrl.fromLocalFile(str(qml_file)))

        # Check if QML is loaded successfully
        if self.qml_widget.status() == QQuickWidget.Error:
            self.logger.error("QML loading failed, possible reasons:")
            for error in self.qml_widget.errors():
                self.logger.error(f"  - {error.toString()}")

            # In the Wayland environment, if QML fails to load, the user is prompted to use CLI mode.
            if is_wayland:
                self.logger.warning("QML loading failed in Wayland environment, it is recommended to use CLI mode to activate")
                self.logger.info("Use command: python main.py --mode cli")

        # Add to layout
        layout.addWidget(self.qml_widget)

        # Set adaptive size
        self._setup_adaptive_size()

        # Lazy setting up of connections to ensure QML is fully loaded
        self._setup_qml_connections()

    def _setup_adaptive_size(self):
        """Set adaptive window size."""
        # Get screen size
        screen = QApplication.primaryScreen()
        screen_size = screen.size()
        screen_width = screen_size.width()
        screen_height = screen_size.height()

        self.logger.info(f"Screen resolution detected: {screen_width}x{screen_height}")

        # Choose the appropriate window size based on screen size
        if screen_width <= 480 or screen_height <= 320:
            # Very small screen (such as 3.5 inches 480x320)
            window_width, window_height = 450, 250
            self.setMinimumSize(QSize(450, 250))
            self._apply_compact_styles()
        elif screen_width <= 800 or screen_height <= 480:
            # Small screen (e.g. 7 inches 800x480)
            window_width, window_height = 480, 280
            self.setMinimumSize(QSize(480, 280))
            self._apply_small_screen_styles()
        elif screen_width <= 1024 or screen_height <= 600:
            # medium screen
            window_width, window_height = 520, 300
            self.setMinimumSize(QSize(520, 300))
        else:
            # Large screen (PC monitor)
            window_width, window_height = 550, 320
            self.setMinimumSize(QSize(550, 320))

        # Make sure the window does not exceed the screen size
        max_width = min(window_width, screen_width - 50)
        max_height = min(window_height, screen_height - 50)

        self.resize(max_width, max_height)

        # Center display
        self.move((screen_width - max_width) // 2, (screen_height - max_height) // 2)

        self.logger.info(f"Set window size: {max_width}x{max_height}")

    def _apply_compact_styles(self):
        """Apply compact styles - suitable for extremely small screens"""
        # Adjust font size
        self.setStyleSheet(
            """
            QLabel { font-size: 10px; }
            QPushButton { font-size: 10px; padding: 4px 8px; }
            QTextEdit { font-size: 8px; }
        """
        )

    def _apply_small_screen_styles(self):
        """Apply small screen style."""
        # Adjust font size
        self.setStyleSheet(
            """
            QLabel { font-size: 11px; }
            QPushButton { font-size: 11px; padding: 6px 10px; }
            QTextEdit { font-size: 9px; }
        """
        )

    def _setup_connections(self):
        """Set up signal connections."""
        # Connect data model signals
        self.activation_model.copyCodeClicked.connect(self._on_copy_code_clicked)
        self.activation_model.retryClicked.connect(self._on_retry_clicked)
        self.activation_model.closeClicked.connect(self.close)

        self.logger.debug("Basic signal connection settings completed")

    def _setup_qml_connections(self):
        """Set up QML signal connection."""
        # Connect QML signals to Python slots
        if self.qml_widget and self.qml_widget.rootObject():
            root_object = self.qml_widget.rootObject()
            root_object.copyCodeClicked.connect(self._on_copy_code_clicked)
            root_object.retryClicked.connect(self._on_retry_clicked)
            root_object.closeClicked.connect(self.close)
            self.logger.debug("QML signal connection setup completed")
        else:
            self.logger.warning("QML root object not found, unable to set signal connection")

    def _setup_signal_connections(self):
        """Set up an asynchronous signal connection."""
        self.signal_emitter.status_changed.connect(self._on_status_changed)
        self.signal_emitter.error_occurred.connect(self._on_error_occurred)
        self.signal_emitter.data_ready.connect(self._on_data_ready)

    def _on_timer_update(self):
        """Timer update callback - start initialization"""
        if not self.initialization_started:
            self.initialization_started = True
            self.stop_update_timer()  # Stop timer

            # Only start initialization if there is a system initializer
            if self.system_initializer is not None:
                # The event loop should now be running and async tasks can be created
                try:
                    self.create_task(self._start_initialization(), "initialization")
                except RuntimeError as e:
                    self.logger.error(f"Failed to create initialization task: {e}")
                    # If it still fails, try again
                    self.start_update_timer(500)
            else:
                self.logger.info("No system initializer, skip automatic initialization")

    async def _start_initialization(self):
        """Start the system initialization process."""
        try:
            # If a SystemInitializer instance has been provided, use it directly
            if self.system_initializer:
                self._update_device_info()
                await self._start_activation_process()
            else:
                # Otherwise create a new instance and run initialization
                self.system_initializer = SystemInitializer()

                # Run the initialization process
                init_result = await self.system_initializer.run_initialization()

                if init_result.get("success", False):
                    self._update_device_info()

                    # Show status message
                    self.status_message = init_result.get("status_message", "")
                    if self.status_message:
                        self.signal_emitter.emit_status(self.status_message)

                    # Check if activation is required
                    if init_result.get("need_activation_ui", True):
                        await self._start_activation_process()
                    else:
                        # No activation required, complete directly
                        self.is_activated = True
                        self.activation_completed.emit(True)
                else:
                    error_msg = init_result.get("error", "Initialization failed")
                    self.signal_emitter.emit_error(error_msg)

        except Exception as e:
            self.logger.error(f"Initialization process exception: {e}", exc_info=True)
            self.signal_emitter.emit_error(f"Initialization exception: {e}")

    def _update_device_info(self):
        """Update device information display."""
        if (
            not self.system_initializer
            or not self.system_initializer.device_fingerprint
        ):
            return

        device_fp = self.system_initializer.device_fingerprint

        # Update serial number
        serial_number = device_fp.get_serial_number()
        self.activation_model.serialNumber = serial_number if serial_number else "--"

        # Update MAC address
        mac_address = device_fp.get_mac_address_from_efuse()
        self.activation_model.macAddress = mac_address if mac_address else "--"

        # Get activation status
        activation_status = self.system_initializer.get_activation_status()
        local_activated = activation_status.get("local_activated", False)
        server_activated = activation_status.get("server_activated", False)
        status_consistent = activation_status.get("status_consistent", True)

        # Update activation status display
        self.is_activated = local_activated

        if not status_consistent:
            self.activation_model.set_status_inconsistent(
                local_activated, server_activated
            )
        else:
            if local_activated:
                self.activation_model.set_status_activated()
            else:
                self.activation_model.set_status_not_activated()

        # Initialization activation code display
        self.activation_model.reset_activation_code()

    async def _start_activation_process(self):
        """Start the activation process."""
        try:
            # Get activation data
            activation_data = self.system_initializer.get_activation_data()

            if not activation_data:
                self.signal_emitter.emit_error("Activation data not obtained, please check the network connection")
                return

            self.activation_data = activation_data

            # Show activation information
            self._show_activation_info(activation_data)

            # Initialize device activator
            config_manager = self.system_initializer.get_config_manager()
            self.device_activator = DeviceActivator(config_manager)

            # Start activation process
            self.signal_emitter.emit_status("Begin the device activation process...")
            activation_success = await self.device_activator.process_activation(
                activation_data
            )

            # Check if the cancellation was because the window was closed
            if self.is_shutdown_requested():
                self.signal_emitter.emit_status("Activation process canceled")
                return

            if activation_success:
                self.signal_emitter.emit_status("Device activation successful!")
                self._on_activation_success()
            else:
                self.signal_emitter.emit_status("Device activation failed")
                self.signal_emitter.emit_error("Device activation failed, please try again")

        except Exception as e:
            self.logger.error(f"Activation process exception: {e}", exc_info=True)
            self.signal_emitter.emit_error(f"Activation exception: {e}")

    def _show_activation_info(self, activation_data: dict):
        """Display activation information."""
        code = activation_data.get("code", "------")

        # Update the activation code in device information
        self.activation_model.update_activation_code(code)

        # The information has been displayed on the UI interface, and only brief logs are recorded.
        self.logger.info(f"Get activation verification code: {code}")

    def _on_activation_success(self):
        """Activation processed successfully."""
        # Update status display
        self.activation_model.set_status_activated()

        # Transmission completion signal
        self.activation_completed.emit(True)
        self.is_activated = True

    def _on_status_changed(self, status: str):
        """Status change handling."""
        self.update_status(status)

    def _on_error_occurred(self, error_message: str):
        """Error handling."""
        self.logger.error(f"Error: {error_message}")
        self.update_status(f"Error: {error_message}")

    def _on_data_ready(self, data):
        """Data readiness processing - Update device information."""
        self.logger.debug(f"Received data: {data}")
        if isinstance(data, dict):
            serial = data.get("serial_number")
            mac = data.get("mac_address")
            if serial or mac:
                self.logger.info(f"Update device information through signals: SN={serial}, MAC={mac}")
                self.activation_model.update_device_info(
                    serial_number=serial, mac_address=mac
                )

    def _on_retry_clicked(self):
        """Jump to activation button click - opens the activation web page."""
        self.logger.info("User clicks to jump to activate")

        # Get activation URL from configuration and open
        try:
            from src.utils.common_utils import open_url
            from src.utils.config_manager import ConfigManager

            config = ConfigManager.get_instance()
            ota_url = config.get_config("SYSTEM_OPTIONS.NETWORK.AUTHORIZATION_URL", "")
            if ota_url:
                open_url(ota_url)
                self.update_status("The activation page has been opened, please enter the verification code in the browser")
            else:
                self.logger.error("Activation URL not configured")
                self.update_status("Error: Activation URL not configured")
        except Exception as e:
            self.logger.error(f"Failed to open activation page: {e}")
            self.update_status(f"Failed to open activation page: {e}")

    def _on_copy_code_clicked(self):
        """Click the Copy Verification Code button."""
        if self.activation_data:
            code = self.activation_data.get("code", "")
            if code:
                clipboard = QApplication.clipboard()
                clipboard.setText(code)
                self.update_status(f"Verification code copied to clipboard: {code}")
        else:
            # Get activation code from model
            code = self.activation_model.activationCode
            if code and code != "--":
                clipboard = QApplication.clipboard()
                clipboard.setText(code)
                self.update_status(f"Verification code copied to clipboard: {code}")

    def update_status(self, message: str):
        """Update status information."""
        self.logger.info(message)

        # If there is a status label, update it
        if hasattr(self, "status_label"):
            self.status_label.setText(message)

    def get_activation_result(self) -> dict:
        """Get activation results."""
        device_fingerprint = None
        config_manager = None

        if self.system_initializer:
            device_fingerprint = self.system_initializer.device_fingerprint
            config_manager = self.system_initializer.config_manager

        return {
            "is_activated": self.is_activated,
            "device_fingerprint": device_fingerprint,
            "config_manager": config_manager,
        }

    async def shutdown_async(self):
        """Close asynchronously."""
        self.logger.info("Closing activation window...")

        # Deactivation process (if ongoing)
        if self.device_activator:
            self.device_activator.cancel_activation()
            self.logger.info("Activation cancellation signal sent")

        # Clean up asynchronous tasks first
        await self.cleanup_async_tasks()

        # Then call the parent class to close
        await super().shutdown_async()

    def mousePressEvent(self, event):
        """Mouse press event - used for window dragging."""
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        """Mouse movement event - implement window dragging."""
        if event.buttons() == Qt.LeftButton and self.drag_position:
            self.move(event.globalPos() - self.drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        """Mouse release event."""
        self.drag_position = None

    def _apply_native_rounded_corners(self):
        """Applies native rounded window shape."""
        try:
            # Get window size
            width = self.width()
            height = self.height()

            # Create a rounded path
            radius = 16  # corner radius
            path = QPainterPath()
            path.addRoundedRect(0, 0, width, height, radius, radius)

            # Create a region and apply it to the window
            region = QRegion(path.toFillPolygon().toPolygon())
            self.setMask(region)

            self.logger.info(
                f"Applied native rounded window shape: {width}x{height}, corner radius: {radius}px"
            )

        except Exception as e:
            self.logger.error(f"Failed to apply native fillet shape: {e}")

    def resizeEvent(self, event):
        super().resizeEvent(event)

    def closeEvent(self, event):
        """Window close event handling."""
        self.logger.info("Activation window close event triggers")
        self.window_closed.emit()
        event.accept()
