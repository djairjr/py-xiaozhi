from pathlib import Path

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (
    QCheckBox,
    QFileDialog,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QWidget,
)

from src.utils.config_manager import ConfigManager
from src.utils.logging_config import get_logger
from src.utils.resource_finder import get_project_root, resource_finder

# Import pinyin conversion library
try:
    from pypinyin import lazy_pinyin, Style
    PYPINYIN_AVAILABLE = True
except ImportError:
    PYPINYIN_AVAILABLE = False


class WakeWordWidget(QWidget):
    """Wake word setting component."""

    # Signal definition
    settings_changed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.logger = get_logger(__name__)
        self.config_manager = ConfigManager.get_instance()

        # UI control reference
        self.ui_controls = {}

        # Initial consonant table (for pinyin segmentation)
        self.initials = [
            'b', 'p', 'm', 'f', 'd', 't', 'n', 'l',
            'g', 'k', 'h', 'j', 'q', 'x',
            'zh', 'ch', 'sh', 'r', 'z', 'c', 's', 'y', 'w'
        ]

        # Initialize UI
        self._setup_ui()
        self._connect_events()
        self._load_config_values()

    def _setup_ui(self):
        """Set up the UI interface."""
        try:
            from PyQt5 import uic

            ui_path = Path(__file__).parent / "wake_word_widget.ui"
            uic.loadUi(str(ui_path), self)

            # Get UI control reference
            self._get_ui_controls()

        except Exception as e:
            self.logger.error(f"Failed to set wake word UI: {e}", exc_info=True)
            raise

    def _get_ui_controls(self):
        """Get the UI control reference."""
        self.ui_controls.update(
            {
                "use_wake_word_check": self.findChild(QCheckBox, "use_wake_word_check"),
                "model_path_edit": self.findChild(QLineEdit, "model_path_edit"),
                "model_path_btn": self.findChild(QPushButton, "model_path_btn"),
                "wake_words_edit": self.findChild(QTextEdit, "wake_words_edit"),
            }
        )

    def _connect_events(self):
        """Connection event handling."""
        if self.ui_controls["use_wake_word_check"]:
            self.ui_controls["use_wake_word_check"].toggled.connect(
                self.settings_changed.emit
            )

        if self.ui_controls["model_path_edit"]:
            self.ui_controls["model_path_edit"].textChanged.connect(
                self.settings_changed.emit
            )

        if self.ui_controls["model_path_btn"]:
            self.ui_controls["model_path_btn"].clicked.connect(
                self._on_model_path_browse
            )

        if self.ui_controls["wake_words_edit"]:
            self.ui_controls["wake_words_edit"].textChanged.connect(
                self.settings_changed.emit
            )

    def _load_config_values(self):
        """Load values ​​from configuration files to UI controls."""
        try:
            # Wake word configuration
            use_wake_word = self.config_manager.get_config(
                "WAKE_WORD_OPTIONS.USE_WAKE_WORD", False
            )
            if self.ui_controls["use_wake_word_check"]:
                self.ui_controls["use_wake_word_check"].setChecked(use_wake_word)

            model_path = self.config_manager.get_config(
                "WAKE_WORD_OPTIONS.MODEL_PATH", ""
            )
            self._set_text_value("model_path_edit", model_path)

            # Read wake words from keywords.txt file
            wake_words_text = self._load_keywords_from_file()
            if self.ui_controls["wake_words_edit"]:
                self.ui_controls["wake_words_edit"].setPlainText(wake_words_text)

        except Exception as e:
            self.logger.error(f"Failed to load wake word configuration value: {e}", exc_info=True)

    def _set_text_value(self, control_name: str, value: str):
        """Set the value of the text control."""
        control = self.ui_controls.get(control_name)
        if control and hasattr(control, "setText"):
            control.setText(str(value) if value is not None else "")

    def _get_text_value(self, control_name: str) -> str:
        """Get the value of the text control."""
        control = self.ui_controls.get(control_name)
        if control and hasattr(control, "text"):
            return control.text().strip()
        return ""

    def _on_model_path_browse(self):
        """Browse the model path."""
        try:
            current_path = self._get_text_value("model_path_edit")
            if not current_path:
                # Use resource_finder to find the default models directory
                models_dir = resource_finder.find_models_dir()
                if models_dir:
                    current_path = str(models_dir)
                else:
                    # If not found, use models in the project root directory
                    project_root = resource_finder.get_project_root()
                    current_path = str(project_root / "models")

            selected_path = QFileDialog.getExistingDirectory(
                self, "Select model directory", current_path
            )

            if selected_path:
                # Convert to relative path (if applicable)
                relative_path = self._convert_to_relative_path(selected_path)
                self._set_text_value("model_path_edit", relative_path)
                self.logger.info(
                    f"Selected model path: {selected_path}, stored as: {relative_path}"
                )

        except Exception as e:
            self.logger.error(f"Failed to browse model path: {e}", exc_info=True)
            QMessageBox.warning(self, "mistake", f"An error occurred while browsing model path: {str(e)}")

    def _convert_to_relative_path(self, model_path: str) -> str:
        """Convert an absolute path to a relative path relative to the project root (if on the same drive letter)."""
        try:
            import os

            # Get the project root directory
            project_root = get_project_root()

            # Check if they are on the same drive letter (only available on Windows)
            if os.name == "nt":  # Windows system
                model_path_drive = os.path.splitdrive(model_path)[0]
                project_root_drive = os.path.splitdrive(str(project_root))[0]

                # If they are on the same drive letter, calculate the relative path
                if model_path_drive.lower() == project_root_drive.lower():
                    relative_path = os.path.relpath(model_path, project_root)
                    return relative_path
                else:
                    # If they are not in the same drive letter, use absolute paths.
                    return model_path
            else:
                # Non-Windows systems, directly calculate relative paths
                try:
                    relative_path = os.path.relpath(model_path, project_root)
                    # Use a relative path only if the relative path does not contain ".."+os.sep
                    if not relative_path.startswith(
                        ".." + os.sep
                    ) and not relative_path.startswith("/"):
                        return relative_path
                    else:
                        # Relative paths include upward search, use absolute paths
                        return model_path
                except ValueError:
                    # Unable to calculate relative path (different volumes), use absolute path
                    return model_path
        except Exception as e:
            self.logger.warning(f"Error calculating relative path, using original path: {e}")
            return model_path

    def _load_keywords_from_file(self) -> str:
        """Load wake words from the keywords.txt file and only display the Chinese part."""
        try:
            # Get the configured model path
            model_path = self.config_manager.get_config(
                "WAKE_WORD_OPTIONS.MODEL_PATH", "models"
            )

            # Use resource_finder to search uniformly (consistent with runtime)
            model_dir = resource_finder.find_directory(model_path)

            if model_dir is None:
                self.logger.warning(f"Model directory does not exist: {model_path}")
                return ""

            keywords_file = model_dir / "keywords.txt"

            if not keywords_file.exists():
                self.logger.warning(f"Keywords file does not exist: {keywords_file}")
                return ""

            keywords = []
            with open(keywords_file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and "@" in line and not line.startswith("#"):
                        # Only extract the Chinese part after @ and display it
                        chinese_part = line.split("@", 1)[1].strip()
                        keywords.append(chinese_part)

            return "\n".join(keywords)

        except Exception as e:
            self.logger.error(f"Failed to read keyword file: {e}")
            return ""

    def _split_pinyin(self, pinyin: str) -> list:
        """Separate Pinyin by initials and finals.

        For example:"xiǎo" -> ["x", "iǎo"]
              "mǐ" -> ["m", "ǐ"]
        """
        if not pinyin:
            return []

        # Try to match initial consonants first by length (zh, ch, sh first)
        for initial in sorted(self.initials, key=len, reverse=True):
            if pinyin.startswith(initial):
                final = pinyin[len(initial):]
                if final:
                    return [initial, final]
                else:
                    return [initial]

        # No initial consonant (zero initial consonant)
        return [pinyin]

    def _chinese_to_keyword_format(self, chinese_text: str) -> str:
        """Convert Chinese to keyword format.

        Args:
            chinese_text: Chinese text, such as"小米小米"Returns:
            keyword format, such as"x iǎo m ǐ x iǎo m ǐ @小米小米"
        """
        if not PYPINYIN_AVAILABLE:
            self.logger.error("The pypinyin library is not installed and cannot be automatically converted.")
            return f"# Conversion failed (pypinyin missing) - {chinese_text}"g) - {chinese_text}"

        try:
            # Convert to tonal pinyin
            pinyin_list = lazy_pinyin(chinese_text, style=Style.TONE)

            # Split each pinyin
            split_parts = []
            for pinyin in pinyin_list:
                parts = self._split_pinyin(pinyin)
                split_parts.extend(parts)

            # Splicing result
            pinyin_str = " ".join(split_parts)
            keyword_line = f"{pinyin_str} @{chinese_text}"

            return keyword_line

        except Exception as e:
            self.logger.error(f"Conversion to Pinyin failed: {e}")
            return f"# Conversion failed - {chinese_text}"hinese_text}"

    def _save_keywords_to_file(self, keywords_text: str):
        """Save the wake word to the keywords.txt file and automatically convert Chinese to Pinyin format."""
        try:
            # Check if pypinyin is available
            if not PYPINYIN_AVAILABLE:
                QMessageBox.warning(
                    self,
                    "Missing dependencies",
                    "The automatic pinyin conversion function requires the installation of the pypinyin library\n\n"
                    "Please run: pip install pypinyin",
                )
                return

            # Get the configured model path
            model_path = self.config_manager.get_config(
                "WAKE_WORD_OPTIONS.MODEL_PATH", "models"
            )

            # Use resource_finder to search uniformly (consistent with runtime)
            model_dir = resource_finder.find_directory(model_path)

            if model_dir is None:
                self.logger.error(f"Model directory does not exist: {model_path}")
                QMessageBox.warning(
                    self,
                    "mistake",
                    f"The model directory does not exist: {model_path}\nPlease configure the correct model path first.",
                )
                return

            keywords_file = model_dir / "keywords.txt"

            # Process the input keyword text (one Chinese per line)
            lines = [line.strip() for line in keywords_text.split("\n") if line.strip()]

            processed_lines = []
            for chinese_text in lines:
                # Automatically convert to pinyin format
                keyword_line = self._chinese_to_keyword_format(chinese_text)
                processed_lines.append(keyword_line)

            # write file
            with open(keywords_file, "w", encoding="utf-8") as f:
                f.write("\n".join(processed_lines) + "\n")

            self.logger.info(f"Successfully saved {len(processed_lines)} keywords to {keywords_file}")
            QMessageBox.information(
                self,
                "Saved successfully",
                f"Successfully saved {len(processed_lines)} wake words\n\n"
                f"Automatically converted to pinyin format",
            )

        except Exception as e:
            self.logger.error(f"Failed to save keyword file: {e}")
            QMessageBox.warning(self, "mistake", f"Failed to save keyword: {str(e)}")

    def get_config_data(self) -> dict:
        """Get current configuration data."""
        config_data = {}

        try:
            # Wake word configuration
            if self.ui_controls["use_wake_word_check"]:
                use_wake_word = self.ui_controls["use_wake_word_check"].isChecked()
                config_data["WAKE_WORD_OPTIONS.USE_WAKE_WORD"] = use_wake_word

            model_path = self._get_text_value("model_path_edit")
            if model_path:
                # Convert to relative path (if applicable)
                relative_path = self._convert_to_relative_path(model_path)
                config_data["WAKE_WORD_OPTIONS.MODEL_PATH"] = relative_path

        except Exception as e:
            self.logger.error(f"Failed to obtain wake word configuration data: {e}", exc_info=True)

        return config_data

    def save_keywords(self):
        """Save wake word to file."""
        if self.ui_controls["wake_words_edit"]:
            wake_words_text = self.ui_controls["wake_words_edit"].toPlainText().strip()
            self._save_keywords_to_file(wake_words_text)

    def reset_to_defaults(self):
        """Reset to default values."""
        try:
            # Get default configuration
            default_config = ConfigManager.DEFAULT_CONFIG

            # Wake word configuration
            wake_word_config = default_config["WAKE_WORD_OPTIONS"]
            if self.ui_controls["use_wake_word_check"]:
                self.ui_controls["use_wake_word_check"].setChecked(
                    wake_word_config["USE_WAKE_WORD"]
                )

            self._set_text_value("model_path_edit", wake_word_config["MODEL_PATH"])

            if self.ui_controls["wake_words_edit"]:
                # Reset using default keywords
                default_keywords = self._get_default_keywords()
                self.ui_controls["wake_words_edit"].setPlainText(default_keywords)

            self.logger.info("Wake word configuration has been reset to default")

        except Exception as e:
            self.logger.error(f"Failed to reset wake word configuration: {e}", exc_info=True)

    def _get_default_keywords(self) -> str:
        """Get the default keyword list and only return Chinese."""
        default_keywords = [
            "Xiaoai classmate",
            "hello ask",
            "Xiaoyi Xiaoyi",
            "XiaomiXiaomi",
            "Hello Xiaozhi",
            "jarvis",
        ]
        return "\n".join(default_keywords)
