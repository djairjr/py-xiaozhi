# -*- coding: utf-8 -*-
"""GUI display window data model - for QML data binding."""

from PyQt5.QtCore import QObject, pyqtProperty, pyqtSignal


class GuiDisplayModel(QObject):
    """Data model for the GUI main window, used for data binding between Python and QML."""

    # attribute change signal
    statusTextChanged = pyqtSignal()
    emotionPathChanged = pyqtSignal()
    ttsTextChanged = pyqtSignal()
    buttonTextChanged = pyqtSignal()
    modeTextChanged = pyqtSignal()
    autoModeChanged = pyqtSignal()

    # User operation signal
    manualButtonPressed = pyqtSignal()
    manualButtonReleased = pyqtSignal()
    autoButtonClicked = pyqtSignal()
    abortButtonClicked = pyqtSignal()
    modeButtonClicked = pyqtSignal()
    sendButtonClicked = pyqtSignal(str)  # carries the entered text
    settingsButtonClicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        # private properties
        self._status_text = "Status: Not connected"
        self._emotion_path = ""  # Expression resource path (GIF/picture) or emoji character
        self._tts_text = "Standby"
        self._button_text = "Start a conversation"  # Auto mode button text
        self._mode_text = "Manual conversation"  # Mode switch button text
        self._auto_mode = False  # Whether automatic mode
        self._is_connected = False

    # status text attribute
    @pyqtProperty(str, notify=statusTextChanged)
    def statusText(self):
        return self._status_text

    @statusText.setter
    def statusText(self, value):
        if self._status_text != value:
            self._status_text = value
            self.statusTextChanged.emit()

    # Expression path properties
    @pyqtProperty(str, notify=emotionPathChanged)
    def emotionPath(self):
        return self._emotion_path

    @emotionPath.setter
    def emotionPath(self, value):
        if self._emotion_path != value:
            self._emotion_path = value
            self.emotionPathChanged.emit()

    # TTS text attribute
    @pyqtProperty(str, notify=ttsTextChanged)
    def ttsText(self):
        return self._tts_text

    @ttsText.setter
    def ttsText(self, value):
        if self._tts_text != value:
            self._tts_text = value
            self.ttsTextChanged.emit()

    # Auto mode button text property
    @pyqtProperty(str, notify=buttonTextChanged)
    def buttonText(self):
        return self._button_text

    @buttonText.setter
    def buttonText(self, value):
        if self._button_text != value:
            self._button_text = value
            self.buttonTextChanged.emit()

    # Mode switch button text property
    @pyqtProperty(str, notify=modeTextChanged)
    def modeText(self):
        return self._mode_text

    @modeText.setter
    def modeText(self, value):
        if self._mode_text != value:
            self._mode_text = value
            self.modeTextChanged.emit()

    # Automatic mode flag attribute
    @pyqtProperty(bool, notify=autoModeChanged)
    def autoMode(self):
        return self._auto_mode

    @autoMode.setter
    def autoMode(self, value):
        if self._auto_mode != value:
            self._auto_mode = value
            self.autoModeChanged.emit()

    # Convenience method
    def update_status(self, status: str, connected: bool):
        """Update status text and connection status."""
        self.statusText = f"Status: {status}"
        self._is_connected = connected

    def update_text(self, text: str):
        """Update TTS text."""
        self.ttsText = text

    def update_emotion(self, emotion_path: str):
        """Update emoticon paths."""
        self.emotionPath = emotion_path

    def update_button_text(self, text: str):
        """Update auto mode button text."""
        self.buttonText = text

    def update_mode_text(self, text: str):
        """Update modal button text."""
        self.modeText = text

    def set_auto_mode(self, is_auto: bool):
        """Set automatic mode."""
        self.autoMode = is_auto
        if is_auto:
            self.modeText = "automatic conversation"
        else:
            self.modeText = "Manual conversation"
