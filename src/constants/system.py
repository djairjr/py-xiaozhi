# System constant definition
from enum import Enum


class InitializationStage(Enum):
    """Initialization phase enumeration."""

    DEVICE_FINGERPRINT = "Phase One: Device Identity Preparation"
    CONFIG_MANAGEMENT = "Phase 2: Configuration management initialization"
    OTA_CONFIG = "The third stage: OTA obtains configuration"
    ACTIVATION = "Phase 4: Activation Process"


class SystemConstants:
    """System constants."""

    # Application information
    APP_NAME = "py-xiaozhi"
    APP_VERSION = "2.0.0"
    BOARD_TYPE = "bread-compact-wifi"

    # Default timeout setting
    DEFAULT_TIMEOUT = 10
    ACTIVATION_MAX_RETRIES = 60
    ACTIVATION_RETRY_INTERVAL = 5

    # file name constant
    CONFIG_FILE = "config.json"
    EFUSE_FILE = "efuse.json"
