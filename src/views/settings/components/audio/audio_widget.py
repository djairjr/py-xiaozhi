import threading
import time
from pathlib import Path

import numpy as np
import sounddevice as sd
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (
    QComboBox,
    QLabel,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QWidget,
)

from src.utils.config_manager import ConfigManager
from src.utils.logging_config import get_logger


class AudioWidget(QWidget):
    """Audio device settings component."""

    # Signal definition
    settings_changed = pyqtSignal()
    status_message = pyqtSignal(str)
    reset_input_ui = pyqtSignal()
    reset_output_ui = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.logger = get_logger(__name__)
        self.config_manager = ConfigManager.get_instance()

        # UI control reference
        self.ui_controls = {}

        # Device data
        self.input_devices = []
        self.output_devices = []

        # test status
        self.testing_input = False
        self.testing_output = False

        # Initialize UI
        self._setup_ui()
        self._connect_events()
        self._scan_devices()
        self._load_config_values()

        # Connect thread-safe UI update signals
        try:
            self.status_message.connect(self._on_status_message)
            self.reset_input_ui.connect(self._reset_input_test_ui)
            self.reset_output_ui.connect(self._reset_output_test_ui)
        except Exception:
            pass

    def _setup_ui(self):
        """Set up the UI interface."""
        try:
            from PyQt5 import uic

            ui_path = Path(__file__).parent / "audio_widget.ui"
            uic.loadUi(str(ui_path), self)

            # Get UI control reference
            self._get_ui_controls()

        except Exception as e:
            self.logger.error(f"Failed to set up audio UI: {e}", exc_info=True)
            raise

    def _get_ui_controls(self):
        """Get the UI control reference."""
        self.ui_controls.update(
            {
                "input_device_combo": self.findChild(QComboBox, "input_device_combo"),
                "output_device_combo": self.findChild(QComboBox, "output_device_combo"),
                "input_info_label": self.findChild(QLabel, "input_info_label"),
                "output_info_label": self.findChild(QLabel, "output_info_label"),
                "test_input_btn": self.findChild(QPushButton, "test_input_btn"),
                "test_output_btn": self.findChild(QPushButton, "test_output_btn"),
                "scan_devices_btn": self.findChild(QPushButton, "scan_devices_btn"),
                "status_text": self.findChild(QTextEdit, "status_text"),
            }
        )

    def _connect_events(self):
        """Connection event handling."""
        # Device selection changes
        if self.ui_controls["input_device_combo"]:
            self.ui_controls["input_device_combo"].currentTextChanged.connect(
                self._on_input_device_changed
            )

        if self.ui_controls["output_device_combo"]:
            self.ui_controls["output_device_combo"].currentTextChanged.connect(
                self._on_output_device_changed
            )

        # button click
        if self.ui_controls["test_input_btn"]:
            self.ui_controls["test_input_btn"].clicked.connect(self._test_input_device)

        if self.ui_controls["test_output_btn"]:
            self.ui_controls["test_output_btn"].clicked.connect(
                self._test_output_device
            )

        if self.ui_controls["scan_devices_btn"]:
            self.ui_controls["scan_devices_btn"].clicked.connect(self._scan_devices)

    def _on_input_device_changed(self):
        """Input device change event."""
        self.settings_changed.emit()
        self._update_device_info()

    def _on_output_device_changed(self):
        """Output device change events."""
        self.settings_changed.emit()
        self._update_device_info()

    def _update_device_info(self):
        """Update device information display."""
        try:
            # Update input device information
            input_device_id = self.ui_controls["input_device_combo"].currentData()
            if input_device_id is not None:
                input_device = next(
                    (d for d in self.input_devices if d["id"] == input_device_id), None
                )
                if input_device:
                    info_text = f"Sampling rate: {int(input_device['sample_rate'])}Hz, Channel: {input_device['channels']}"
                    self.ui_controls["input_info_label"].setText(info_text)
                else:
                    self.ui_controls["input_info_label"].setText("Failed to obtain device information")
            else:
                self.ui_controls["input_info_label"].setText("No device selected")

            # Update output device information
            output_device_id = self.ui_controls["output_device_combo"].currentData()
            if output_device_id is not None:
                output_device = next(
                    (d for d in self.output_devices if d["id"] == output_device_id),
                    None,
                )
                if output_device:
                    info_text = f"Sampling rate: {int(output_device['sample_rate'])}Hz, Channel: {output_device['channels']}"
                    self.ui_controls["output_info_label"].setText(info_text)
                else:
                    self.ui_controls["output_info_label"].setText("Failed to obtain device information")
            else:
                self.ui_controls["output_info_label"].setText("No device selected")

        except Exception as e:
            self.logger.error(f"Failed to update device information: {e}", exc_info=True)

    def _scan_devices(self):
        """Scan for audio devices."""
        try:
            self._append_status("Scanning audio devices...")

            # Clear existing device list
            self.input_devices.clear()
            self.output_devices.clear()

            # Get system default device
            default_input = sd.default.device[0] if sd.default.device else None
            default_output = sd.default.device[1] if sd.default.device else None

            # Scan all devices
            devices = sd.query_devices()
            for i, dev_info in enumerate(devices):
                device_name = dev_info["name"]

                # Add input device
                if dev_info["max_input_channels"] > 0:
                    default_mark = "(default)" if i == default_input else ""
                    self.input_devices.append(
                        {
                            "id": i,
                            "name": device_name + default_mark,
                            "raw_name": device_name,
                            "channels": dev_info["max_input_channels"],
                            "sample_rate": dev_info["default_samplerate"],
                        }
                    )

                # Add output device
                if dev_info["max_output_channels"] > 0:
                    default_mark = "(default)" if i == default_output else ""
                    self.output_devices.append(
                        {
                            "id": i,
                            "name": device_name + default_mark,
                            "raw_name": device_name,
                            "channels": dev_info["max_output_channels"],
                            "sample_rate": dev_info["default_samplerate"],
                        }
                    )

            # Update drop down box
            self._update_device_combos()

            # Automatically select default device
            self._select_default_devices()

            self._append_status(
                f"Scan completed: {len(self.input_devices)} input devices, {len(self.output_devices)} output devices found"
            )

        except Exception as e:
            self.logger.error(f"Scan for audio device failed: {e}", exc_info=True)
            self._append_status(f"Scanning device failed: {str(e)}")

    def _update_device_combos(self):
        """Update device dropdown box."""
        try:
            # Save current selection
            current_input = self.ui_controls["input_device_combo"].currentData()
            current_output = self.ui_controls["output_device_combo"].currentData()

            # Empty and repopulate input devices
            self.ui_controls["input_device_combo"].clear()
            for device in self.input_devices:
                self.ui_controls["input_device_combo"].addItem(
                    device["name"], device["id"]
                )

            # Empty and repopulate the output device
            self.ui_controls["output_device_combo"].clear()
            for device in self.output_devices:
                self.ui_controls["output_device_combo"].addItem(
                    device["name"], device["id"]
                )

            # Try to restore previous selection
            if current_input is not None:
                index = self.ui_controls["input_device_combo"].findData(current_input)
                if index >= 0:
                    self.ui_controls["input_device_combo"].setCurrentIndex(index)

            if current_output is not None:
                index = self.ui_controls["output_device_combo"].findData(current_output)
                if index >= 0:
                    self.ui_controls["output_device_combo"].setCurrentIndex(index)

        except Exception as e:
            self.logger.error(f"Failed to update device dropdown: {e}", exc_info=True)

    def _select_default_devices(self):
        """Automatically select the default device (consistent with the logic of audio_codec.py)."""
        try:
            # Prioritize the device in the configuration, if not, select the system default device
            config_input_id = self.config_manager.get_config(
                "AUDIO_DEVICES.input_device_id"
            )
            config_output_id = self.config_manager.get_config(
                "AUDIO_DEVICES.output_device_id"
            )

            # Select input device
            if config_input_id is not None:
                # Use devices in configuration
                index = self.ui_controls["input_device_combo"].findData(config_input_id)
                if index >= 0:
                    self.ui_controls["input_device_combo"].setCurrentIndex(index)
            else:
                # Automatically select default input devices (those marked "default")"标记的）
                for i in range(self.ui_controls["input_device_combo"].count()):
                    if "default" in self.ui_controls["input_device_combo"].itemText(i):
                        self.ui_controls["input_device_combo"].setCurrentIndex(i)
                        break

            # Select output device
            if config_output_id is not None:
                # Use devices in configuration
                index = self.ui_controls["output_device_combo"].findData(
                    config_output_id
                )
                if index >= 0:
                    self.ui_controls["output_device_combo"].setCurrentIndex(index)
            else:
                # Automatically select the default output device (the one marked "Default")"标记的）
                for i in range(self.ui_controls["output_device_combo"].count()):
                    if "default" in self.ui_controls["output_device_combo"].itemText(i):
                        self.ui_controls["output_device_combo"].setCurrentIndex(i)
                        break

            # Update device information display
            self._update_device_info()

        except Exception as e:
            self.logger.error(f"Failed to select default device: {e}", exc_info=True)

    def _test_input_device(self):
        """Test input devices."""
        if self.testing_input:
            return

        try:
            device_id = self.ui_controls["input_device_combo"].currentData()
            if device_id is None:
                QMessageBox.warning(self, "hint", "Please select an input device first")
                return

            self.testing_input = True
            self.ui_controls["test_input_btn"].setEnabled(False)
            self.ui_controls["test_input_btn"].setText("Recording...")

            # Execute tests in a thread
            test_thread = threading.Thread(
                target=self._do_input_test, args=(device_id,)
            )
            test_thread.daemon = True
            test_thread.start()

        except Exception as e:
            self.logger.error(f"Test input device failed: {e}", exc_info=True)
            self._append_status(f"Input device test failed: {str(e)}")
            self._reset_input_test_ui()

    def _do_input_test(self, device_id):
        """Perform input device testing."""
        try:
            # Get device information and sampling rate
            input_device = next(
                (d for d in self.input_devices if d["id"] == device_id), None
            )
            if not input_device:
                self._append_status_threadsafe("Error: Unable to get device information")
                return

            sample_rate = int(input_device["sample_rate"])
            duration = 3  # Recording duration 3 seconds

            self._append_status_threadsafe(
                f"Start recording test (device: {device_id}, sampling rate: {sample_rate}Hz)"
            )
            self._append_status_threadsafe("Please speak into the microphone, such as counting numbers: 1, 2, 3...")

            # Countdown reminder
            for i in range(3, 0, -1):
                self._append_status_threadsafe(f"Recording will start in {i} seconds...")
                time.sleep(1)

            self._append_status_threadsafe("Recording, please speak... (3 seconds)")

            # recording
            recording = sd.rec(
                int(duration * sample_rate),
                samplerate=sample_rate,
                channels=1,
                device=device_id,
                dtype=np.float32,
            )
            sd.wait()

            self._append_status_threadsafe("Recording completed, analyzing...")

            # Analyze recording quality
            max_amplitude = np.max(np.abs(recording))
            rms = np.sqrt(np.mean(recording**2))

            # Detect if there is voice activity
            frame_length = int(0.1 * sample_rate)  # 100ms frame
            frames = []
            for i in range(0, len(recording) - frame_length, frame_length):
                frame_rms = np.sqrt(np.mean(recording[i : i + frame_length] ** 2))
                frames.append(frame_rms)

            active_frames = sum(1 for f in frames if f > 0.01)  # active frames
            activity_ratio = active_frames / len(frames) if frames else 0

            # Test result analysis
            if max_amplitude < 0.001:
                self._append_status_threadsafe("[Failed] No audio signal detected")
                self._append_status_threadsafe(
                    "Please check: 1) Microphone connection 2) System volume 3) Microphone permissions"
                )
            elif max_amplitude > 0.8:
                self._append_status_threadsafe("[Warning] Audio signal overload")
                self._append_status_threadsafe("It is recommended to reduce microphone gain or volume settings")
            elif activity_ratio < 0.1:
                self._append_status_threadsafe("[WARNING] Audio detected but low voice activity")
                self._append_status_threadsafe(
                    "Make sure you speak into the microphone, or check the microphone sensitivity"
                )
            else:
                self._append_status_threadsafe("[Success] Recording test passed")
                self._append_status_threadsafe(
                    f"Sound quality data: maximum volume={max_amplitude:.1%}, average volume={rms:.1%}, activity={activity_ratio:.1%}"
                )
                self._append_status_threadsafe("Microphone works fine")

        except Exception as e:
            self.logger.error(f"Recording test failed: {e}", exc_info=True)
            self._append_status_threadsafe(f"[Error] Recording test failed: {str(e)}")
            if "Permission denied" in str(e) or "access" in str(e).lower():
                self._append_status_threadsafe(
                    "It may be a permission issue, please check the system microphone permission settings"
                )
        finally:
            # Reset UI state (switch back to main thread)
            self._reset_input_ui_threadsafe()

    def _test_output_device(self):
        """Test output devices."""
        if self.testing_output:
            return

        try:
            device_id = self.ui_controls["output_device_combo"].currentData()
            if device_id is None:
                QMessageBox.warning(self, "hint", "Please select the output device first")
                return

            self.testing_output = True
            self.ui_controls["test_output_btn"].setEnabled(False)
            self.ui_controls["test_output_btn"].setText("Playing...")

            # Execute tests in a thread
            test_thread = threading.Thread(
                target=self._do_output_test, args=(device_id,)
            )
            test_thread.daemon = True
            test_thread.start()

        except Exception as e:
            self.logger.error(f"Test output device failed: {e}", exc_info=True)
            self._append_status(f"Output device test failed: {str(e)}")
            self._reset_output_test_ui()

    def _do_output_test(self, device_id):
        """Perform output device testing."""
        try:
            # Get device information and sampling rate
            output_device = next(
                (d for d in self.output_devices if d["id"] == device_id), None
            )
            if not output_device:
                self._append_status_threadsafe("Error: Unable to get device information")
                return

            sample_rate = int(output_device["sample_rate"])
            duration = 2.0  # Play time
            frequency = 440  # 440Hz A sound

            self._append_status_threadsafe(
                f"Start playback test (device: {device_id}, sampling rate: {sample_rate}Hz)"
            )
            self._append_status_threadsafe("Please have your headphones/speakers ready, the test sound will be played soon...")

            # Countdown reminder
            for i in range(3, 0, -1):
                self._append_status_threadsafe(f"Start playing in {i} seconds...")
                time.sleep(1)

            self._append_status_threadsafe(
                f"Playing {frequency}Hz test tone ({duration} seconds)..."
            )

            # Generate test audio (sine wave)
            t = np.linspace(0, duration, int(sample_rate * duration))
            # Add fade effects to avoid popping sounds
            fade_samples = int(0.1 * sample_rate)  # 0.1 second fade in and fade out
            audio = 0.3 * np.sin(2 * np.pi * frequency * t)

            # Apply fade
            audio[:fade_samples] *= np.linspace(0, 1, fade_samples)
            audio[-fade_samples:] *= np.linspace(1, 0, fade_samples)

            # Play audio
            sd.play(audio, samplerate=sample_rate, device=device_id)
            sd.wait()

            self._append_status_threadsafe("Playback completed")
            self._append_status_threadsafe(
                "Test instructions: If you hear a clear test tone, it means the speaker/headphones are working properly"
            )
            self._append_status_threadsafe(
                "If you don't hear sound, check your volume settings or choose a different output device"
            )

        except Exception as e:
            self.logger.error(f"Playback test failed: {e}", exc_info=True)
            self._append_status_threadsafe(f"[Error] Playback test failed: {str(e)}")
        finally:
            # Reset UI state (switch back to main thread)
            self._reset_output_ui_threadsafe()

    def _reset_input_test_ui(self):
        """Reset input test UI state."""
        self.testing_input = False
        self.ui_controls["test_input_btn"].setEnabled(True)
        self.ui_controls["test_input_btn"].setText("Test recording")

    def _reset_input_ui_threadsafe(self):
        try:
            self.reset_input_ui.emit()
        except Exception as e:
            self.logger.error(f"Thread-safe reset input test UI failed: {e}")

    def _reset_output_test_ui(self):
        """Reset the output test UI state."""
        self.testing_output = False
        self.ui_controls["test_output_btn"].setEnabled(True)
        self.ui_controls["test_output_btn"].setText("Test play")

    def _reset_output_ui_threadsafe(self):
        try:
            self.reset_output_ui.emit()
        except Exception as e:
            self.logger.error(f"Thread-safe reset output test UI failed: {e}")

    def _append_status(self, message):
        """Add status information."""
        try:
            if self.ui_controls["status_text"]:
                current_time = time.strftime("%H:%M:%S")
                formatted_message = f"[{current_time}] {message}"
                self.ui_controls["status_text"].append(formatted_message)
                # scroll to bottom
                self.ui_controls["status_text"].verticalScrollBar().setValue(
                    self.ui_controls["status_text"].verticalScrollBar().maximum()
                )
        except Exception as e:
            self.logger.error(f"Failed to add status information: {e}", exc_info=True)

    def _append_status_threadsafe(self, message):
        """A background thread safely appends the status text to the QTextEdit (switch back to the main thread via a signal)."""
        try:
            if not self.ui_controls.get("status_text"):
                return
            current_time = time.strftime("%H:%M:%S")
            formatted_message = f"[{current_time}] {message}"
            self.status_message.emit(formatted_message)
        except Exception as e:
            self.logger.error(f"Thread-safe append state failed: {e}", exc_info=True)

    def _on_status_message(self, formatted_message: str):
        try:
            if not self.ui_controls.get("status_text"):
                return
            self.ui_controls["status_text"].append(formatted_message)
            # scroll to bottom
            self.ui_controls["status_text"].verticalScrollBar().setValue(
                self.ui_controls["status_text"].verticalScrollBar().maximum()
            )
        except Exception as e:
            self.logger.error(f"Status text append failed: {e}")

    def _load_config_values(self):
        """Load values ​​from configuration files to UI controls."""
        try:
            # Get audio device configuration
            audio_config = self.config_manager.get_config("AUDIO_DEVICES", {})

            # Set up input devices
            input_device_id = audio_config.get("input_device_id")
            if input_device_id is not None:
                index = self.ui_controls["input_device_combo"].findData(input_device_id)
                if index >= 0:
                    self.ui_controls["input_device_combo"].setCurrentIndex(index)

            # Set up output device
            output_device_id = audio_config.get("output_device_id")
            if output_device_id is not None:
                index = self.ui_controls["output_device_combo"].findData(
                    output_device_id
                )
                if index >= 0:
                    self.ui_controls["output_device_combo"].setCurrentIndex(index)

            # Device information is automatically updated when device selection changes, no manual settings required

        except Exception as e:
            self.logger.error(f"Failed to load audio device configuration values: {e}", exc_info=True)

    def get_config_data(self) -> dict:
        """Get current configuration data."""
        config_data = {}

        try:
            audio_config = {}

            # Enter device configuration
            input_device_id = self.ui_controls["input_device_combo"].currentData()
            if input_device_id is not None:
                audio_config["input_device_id"] = input_device_id
                audio_config["input_device_name"] = self.ui_controls[
                    "input_device_combo"
                ].currentText()

            # Output device configuration
            output_device_id = self.ui_controls["output_device_combo"].currentData()
            if output_device_id is not None:
                audio_config["output_device_id"] = output_device_id
                audio_config["output_device_name"] = self.ui_controls[
                    "output_device_combo"
                ].currentText()

            # The sampling rate information of the device is automatically determined by the device and does not require user configuration.
            # Save the device's default sample rate for subsequent use
            input_device = next(
                (d for d in self.input_devices if d["id"] == input_device_id), None
            )
            if input_device:
                audio_config["input_sample_rate"] = int(input_device["sample_rate"])

            output_device = next(
                (d for d in self.output_devices if d["id"] == output_device_id), None
            )
            if output_device:
                audio_config["output_sample_rate"] = int(output_device["sample_rate"])

            if audio_config:
                config_data["AUDIO_DEVICES"] = audio_config

        except Exception as e:
            self.logger.error(f"Failed to obtain audio device configuration data: {e}", exc_info=True)

        return config_data

    def reset_to_defaults(self):
        """Reset to default values."""
        try:
            # Rescan device
            self._scan_devices()

            # The sampling rate information will be automatically displayed after the device is scanned, no manual setting is required.

            # Clear status display
            if self.ui_controls["status_text"]:
                self.ui_controls["status_text"].clear()

            self._append_status("Reset to default settings")
            self.logger.info("Audio device configuration has been reset to defaults")

        except Exception as e:
            self.logger.error(f"Failed to reset audio device configuration: {e}", exc_info=True)
