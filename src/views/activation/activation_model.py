# -*- coding: utf-8 -*-
"""Activate window data model - for QML data binding"""

from PyQt5.QtCore import QObject, pyqtProperty, pyqtSignal


class ActivationModel(QObject):
    """Data model for active windows, used for data binding between Python and QML."""

    # attribute change signal
    serialNumberChanged = pyqtSignal()
    macAddressChanged = pyqtSignal()
    activationStatusChanged = pyqtSignal()
    activationCodeChanged = pyqtSignal()
    statusColorChanged = pyqtSignal()

    # User operation signal
    copyCodeClicked = pyqtSignal()
    retryClicked = pyqtSignal()
    closeClicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        # private properties
        self._serial_number = "--"
        self._mac_address = "--"
        self._activation_status = "Checking..."
        self._activation_code = "--"
        self._status_color = "#6c757d"

    # Serial number attribute
    @pyqtProperty(str, notify=serialNumberChanged)
    def serialNumber(self):
        return self._serial_number

    @serialNumber.setter
    def serialNumber(self, value):
        if self._serial_number != value:
            self._serial_number = value
            self.serialNumberChanged.emit()

    # MAC address properties
    @pyqtProperty(str, notify=macAddressChanged)
    def macAddress(self):
        return self._mac_address

    @macAddress.setter
    def macAddress(self, value):
        if self._mac_address != value:
            self._mac_address = value
            self.macAddressChanged.emit()

    # activation state attribute
    @pyqtProperty(str, notify=activationStatusChanged)
    def activationStatus(self):
        return self._activation_status

    @activationStatus.setter
    def activationStatus(self, value):
        if self._activation_status != value:
            self._activation_status = value
            self.activationStatusChanged.emit()

    # Activation code properties
    @pyqtProperty(str, notify=activationCodeChanged)
    def activationCode(self):
        return self._activation_code

    @activationCode.setter
    def activationCode(self, value):
        if self._activation_code != value:
            self._activation_code = value
            self.activationCodeChanged.emit()

    # Status color attribute
    @pyqtProperty(str, notify=statusColorChanged)
    def statusColor(self):
        return self._status_color

    @statusColor.setter
    def statusColor(self, value):
        if self._status_color != value:
            self._status_color = value
            self.statusColorChanged.emit()

    # Convenience method
    def update_device_info(self, serial_number=None, mac_address=None):
        """Update device information."""
        if serial_number is not None:
            self.serialNumber = serial_number
        if mac_address is not None:
            self.macAddress = mac_address

    def update_activation_status(self, status, color="#6c757d"):
        """Update activation status."""
        self.activationStatus = status
        self.statusColor = color

    def update_activation_code(self, code):
        """Update activation code."""
        self.activationCode = code

    def reset_activation_code(self):
        """Reset activation code."""
        self.activationCode = "--"

    def set_status_activated(self):
        """Set to activated state."""
        self.update_activation_status("Activated", "#28a745")
        self.reset_activation_code()

    def set_status_not_activated(self):
        """Set to inactive state."""
        self.update_activation_status("Not activated", "#dc3545")

    def set_status_inconsistent(self, local_activated=False, server_activated=False):
        """The setting status is inconsistent."""
        if local_activated and not server_activated:
            self.update_activation_status("Inconsistent status (requires reactivation)", "#ff9900")
        else:
            self.update_activation_status("Inconsistent status (fixed)", "#28a745")
