import os
from pathlib import Path

from PyQt5.QtWidgets import (
    QDialog,
    QMessageBox,
    QPushButton,
    QTabWidget,
)

from src.utils.config_manager import ConfigManager
from src.utils.logging_config import get_logger
from src.views.settings.components.audio import AudioWidget
from src.views.settings.components.camera import CameraWidget
from src.views.settings.components.shortcuts_settings import ShortcutsSettingsWidget
from src.views.settings.components.system_options import SystemOptionsWidget
from src.views.settings.components.wake_word import WakeWordWidget


class SettingsWindow(QDialog):
    """Parameter configuration window."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.logger = get_logger(__name__)
        self.config_manager = ConfigManager.get_instance()

        # component reference
        self.system_options_tab = None
        self.wake_word_tab = None
        self.camera_tab = None
        self.audio_tab = None
        self.shortcuts_tab = None

        # UI controls
        self.ui_controls = {}

        # Initialize UI
        self._setup_ui()
        self._connect_events()

    def _setup_ui(self):
        """Set up the UI interface."""
        try:
            from PyQt5 import uic

            ui_path = Path(__file__).parent / "settings_window.ui"
            uic.loadUi(str(ui_path), self)

            # Get a reference to a UI control
            self._get_ui_controls()

            # Add individual component tabs
            self._add_component_tabs()

        except Exception as e:
            self.logger.error(f"Failed to set up UI: {e}", exc_info=True)
            raise

    def _add_component_tabs(self):
        """Add individual component tabs."""
        try:
            # GetTabWidget
            tab_widget = self.findChild(QTabWidget, "tabWidget")
            if not tab_widget:
                self.logger.error("TabWidget control not found")
                return

            # Clear existing tabs (if any)
            tab_widget.clear()

            # Create and add system options components
            self.system_options_tab = SystemOptionsWidget()
            tab_widget.addTab(self.system_options_tab, "System options")
            self.system_options_tab.settings_changed.connect(self._on_settings_changed)

            # Create and add wake word component
            self.wake_word_tab = WakeWordWidget()
            tab_widget.addTab(self.wake_word_tab, "wake word")
            self.wake_word_tab.settings_changed.connect(self._on_settings_changed)

            # Create and add camera component
            self.camera_tab = CameraWidget()
            tab_widget.addTab(self.camera_tab, "Camera")
            self.camera_tab.settings_changed.connect(self._on_settings_changed)

            # Create and add audio device components
            self.audio_tab = AudioWidget()
            tab_widget.addTab(self.audio_tab, "audio equipment")
            self.audio_tab.settings_changed.connect(self._on_settings_changed)

            # Create and add shortcut key setting components
            self.shortcuts_tab = ShortcutsSettingsWidget()
            tab_widget.addTab(self.shortcuts_tab, "shortcut key")
            self.shortcuts_tab.settings_changed.connect(self._on_settings_changed)

            self.logger.debug("All component tabs added successfully")

        except Exception as e:
            self.logger.error(f"Failed to add component tab: {e}", exc_info=True)

    def _on_settings_changed(self):
        """Set change callback."""
        # You can add some hints or other logic here

    def _get_ui_controls(self):
        """Get the UI control reference."""
        # Just need to get the main button control
        self.ui_controls.update(
            {
                "save_btn": self.findChild(QPushButton, "save_btn"),
                "cancel_btn": self.findChild(QPushButton, "cancel_btn"),
                "reset_btn": self.findChild(QPushButton, "reset_btn"),
            }
        )

    def _connect_events(self):
        """Connection event handling."""
        if self.ui_controls["save_btn"]:
            self.ui_controls["save_btn"].clicked.connect(self._on_save_clicked)

        if self.ui_controls["cancel_btn"]:
            self.ui_controls["cancel_btn"].clicked.connect(self.reject)

        if self.ui_controls["reset_btn"]:
            self.ui_controls["reset_btn"].clicked.connect(self._on_reset_clicked)

    # Configuration loading is now handled by individual components themselves and does not need to be handled in the main window

    # Removed control operation methods that are no longer needed and are now handled by individual components

    def _on_save_clicked(self):
        """
        保存按钮点击事件.
        """
        try:
            # Collect all configuration data
            success = self._save_all_config()

            if success:
                # Displays successful saving and prompts to restart
                reply = QMessageBox.question(
                    self,
                    "Configuration saved successfully",
                    "The configuration has been saved successfully! \n\nIn order for the configuration to take effect, it is recommended to restart the software. \nWould you like to restart now?",
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.Yes,
                )

                if reply == QMessageBox.Yes:
                    self._restart_application()
                else:
                    self.accept()
            else:
                QMessageBox.warning(self, "mistake", "Failed to save configuration, please check the entered values.")

        except Exception as e:
            self.logger.error(f"Failed to save configuration: {e}", exc_info=True)
            QMessageBox.critical(self, "mistake", f"An error occurred while saving the configuration: {str(e)}")

    def _save_all_config(self) -> bool:
        """Save all configurations."""
        try:
            # Collect configuration data from various components
            all_config_data = {}

            # System option configuration
            if self.system_options_tab:
                system_config = self.system_options_tab.get_config_data()
                all_config_data.update(system_config)

            # Wake word configuration
            if self.wake_word_tab:
                wake_word_config = self.wake_word_tab.get_config_data()
                all_config_data.update(wake_word_config)
                # Save wake word file
                self.wake_word_tab.save_keywords()

            # Camera configuration
            if self.camera_tab:
                camera_config = self.camera_tab.get_config_data()
                all_config_data.update(camera_config)

            # Audio device configuration
            if self.audio_tab:
                audio_config = self.audio_tab.get_config_data()
                all_config_data.update(audio_config)

            # Shortcut key configuration
            if self.shortcuts_tab:
                # The shortcut key component has its own saving method
                self.shortcuts_tab.apply_settings()

            # Batch update configuration
            for config_path, value in all_config_data.items():
                self.config_manager.update_config(config_path, value)

            self.logger.info("Configuration saved successfully")
            return True

        except Exception as e:
            self.logger.error(f"Error saving configuration: {e}", exc_info=True)
            return False

    def _on_reset_clicked(self):
        """Reset button click event."""
        reply = QMessageBox.question(
            self,
            "Confirm reset",
            "Are you sure you want to reset all configurations to default? \nThis will clear all current settings.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if reply == QMessageBox.Yes:
            self._reset_to_defaults()

    def _reset_to_defaults(self):
        """Reset to default values."""
        try:
            # Reset individual components to default values
            if self.system_options_tab:
                self.system_options_tab.reset_to_defaults()

            if self.wake_word_tab:
                self.wake_word_tab.reset_to_defaults()

            if self.camera_tab:
                self.camera_tab.reset_to_defaults()

            if self.audio_tab:
                self.audio_tab.reset_to_defaults()

            if self.shortcuts_tab:
                self.shortcuts_tab.reset_to_defaults()

            self.logger.info("All component configurations have been reset to default values")

        except Exception as e:
            self.logger.error(f"Failed to reset configuration: {e}", exc_info=True)
            QMessageBox.critical(self, "mistake", f"An error occurred while resetting the configuration: {str(e)}")

    def _restart_application(self):
        """Restart the application."""
        try:
            self.logger.info("User chooses to restart the application")

            # Close settings window
            self.accept()

            # Restart the program directly
            self._direct_restart()

        except Exception as e:
            self.logger.error(f"Failed to restart application: {e}", exc_info=True)
            QMessageBox.warning(
                self, "Restart failed", "Automatic restart failed, please restart the software manually to make the configuration take effect."
            )

    def _direct_restart(self):
        """Restart the program directly."""
        try:
            import sys

            from PyQt5.QtWidgets import QApplication

            # Get the path and parameters of the currently executed program
            python = sys.executable
            script = sys.argv[0]
            args = sys.argv[1:]

            self.logger.info(f"Restart command: {python} {script} {' '.join(args)}")

            # Close current application
            QApplication.quit()

            # Start a new instance
            if getattr(sys, "frozen", False):
                # Packaging environment
                os.execv(sys.executable, [sys.executable] + args)
            else:
                # development environment
                os.execv(python, [python, script] + args)

        except Exception as e:
            self.logger.error(f"Direct restart failed: {e}", exc_info=True)

    def closeEvent(self, event):
        """Window close event."""
        self.logger.debug("Settings window is closed")
        super().closeEvent(event)
