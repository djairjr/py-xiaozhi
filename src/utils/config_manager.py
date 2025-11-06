import json
import uuid
from typing import Any, Dict

from src.utils.logging_config import get_logger
from src.utils.resource_finder import resource_finder

logger = get_logger(__name__)


class ConfigManager:
    """Configuration Manager - Singleton Mode"""

    _instance = None

    # Default configuration
    DEFAULT_CONFIG = {
        "SYSTEM_OPTIONS": {
            "CLIENT_ID": None,
            "DEVICE_ID": None,
            "NETWORK": {
                "OTA_VERSION_URL": "https://api.tenclass.net/xiaozhi/ota/",
                "WEBSOCKET_URL": None,
                "WEBSOCKET_ACCESS_TOKEN": None,
                "MQTT_INFO": None,
                "ACTIVATION_VERSION": "v2",  # Optional values: v1, v2
                "AUTHORIZATION_URL": "https://xiaozhi.me/",
            },
        },
        "WAKE_WORD_OPTIONS": {
            "USE_WAKE_WORD": True,
            "MODEL_PATH": "models",
            "NUM_THREADS": 4,
            "PROVIDER": "cpu",
            "MAX_ACTIVE_PATHS": 2,
            "KEYWORDS_SCORE": 1.8,
            "KEYWORDS_THRESHOLD": 0.2,
            "NUM_TRAILING_BLANKS": 1,
        },
        "CAMERA": {
            "camera_index": 0,
            "frame_width": 640,
            "frame_height": 480,
            "fps": 30,
            "Local_VL_url": "https://open.bigmodel.cn/api/paas/v4/",
            "VLapi_key": "",
            "models": "glm-4v-plus",
        },
        "SHORTCUTS": {
            "ENABLED": True,
            "MANUAL_PRESS": {"modifier": "ctrl", "key": "j", "description": "Hold to speak"},
            "AUTO_TOGGLE": {"modifier": "ctrl", "key": "k", "description": "automatic conversation"},
            "ABORT": {"modifier": "ctrl", "key": "q", "description": "interrupt conversation"},
            "MODE_TOGGLE": {"modifier": "ctrl", "key": "m", "description": "Switch mode"},
            "WINDOW_TOGGLE": {
                "modifier": "ctrl",
                "key": "w",
                "description": "Show/hide windows",
            },
        },
        "AEC_OPTIONS": {
            "ENABLED": False,
            "BUFFER_MAX_LENGTH": 200,
            "FRAME_DELAY": 3,
            "FILTER_LENGTH_RATIO": 0.4,
            "ENABLE_PREPROCESS": True,
        },
        "AUDIO_DEVICES": {
            "input_device_id": None,
            "input_device_name": None,
            "output_device_id": None,
            "output_device_name": None,
            "input_sample_rate": None,
            "output_sample_rate": None,
        },
    }

    def __new__(cls):
        """Ensure singleton mode."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        """Initialize the configuration manager."""
        if self._initialized:
            return
        self._initialized = True

        # Initialization configuration file path
        self._init_config_paths()

        # Make sure the necessary directories exist
        self._ensure_required_directories()

        # Load configuration
        self._config = self._load_config()

    def _init_config_paths(self):
        """Initialization configuration file path."""
        # Use resource_finder to find or create configuration directories
        self.config_dir = resource_finder.find_config_dir()
        if not self.config_dir:
            # If the configuration directory cannot be found, create it in the project root directory
            project_root = resource_finder.get_project_root()
            self.config_dir = project_root / "config"
            self.config_dir.mkdir(parents=True, exist_ok=True)
            logger.info(f"Create configuration directory: {self.config_dir.absolute()}")

        self.config_file = self.config_dir / "config.json"

        # Record configuration file path
        logger.info(f"Configuration directory: {self.config_dir.absolute()}")
        logger.info(f"Configuration file: {self.config_file.absolute()}")

    def _ensure_required_directories(self):
        """Make sure the necessary directories exist."""
        project_root = resource_finder.get_project_root()

        # Create models directory
        models_dir = project_root / "models"
        if not models_dir.exists():
            models_dir.mkdir(parents=True, exist_ok=True)
            logger.info(f"Create model directory: {models_dir.absolute()}")

        # Create cache directory
        cache_dir = project_root / "cache"
        if not cache_dir.exists():
            cache_dir.mkdir(parents=True, exist_ok=True)
            logger.info(f"Create cache directory: {cache_dir.absolute()}")

    def _load_config(self) -> Dict[str, Any]:
        """Load the configuration file or create it if it does not exist."""
        try:
            # First try to use resource_finder to find the configuration file
            config_file_path = resource_finder.find_file("config/config.json")

            if config_file_path:
                logger.debug(f"Use resource_finder to find the configuration file: {config_file_path}")
                config = json.loads(config_file_path.read_text(encoding="utf-8"))
                return self._merge_configs(self.DEFAULT_CONFIG, config)

            # If resource_finder does not find it, try using the path in the instance variable
            if self.config_file.exists():
                logger.debug(f"Find the configuration file using the instance path: {self.config_file}")
                config = json.loads(self.config_file.read_text(encoding="utf-8"))
                return self._merge_configs(self.DEFAULT_CONFIG, config)
            else:
                # Create default configuration file
                logger.info("The configuration file does not exist, create a default configuration")
                self._save_config(self.DEFAULT_CONFIG)
                return self.DEFAULT_CONFIG.copy()

        except Exception as e:
            logger.error(f"Configuration loading error: {e}")
            return self.DEFAULT_CONFIG.copy()

    def _save_config(self, config: dict) -> bool:
        """Save configuration to file."""
        try:
            # Make sure the configuration directory exists
            self.config_dir.mkdir(parents=True, exist_ok=True)

            # Save configuration file
            self.config_file.write_text(
                json.dumps(config, indent=2, ensure_ascii=False), encoding="utf-8"
            )
            logger.debug(f"Configuration saved to: {self.config_file}")
            return True

        except Exception as e:
            logger.error(f"Configuration save error: {e}")
            return False

    @staticmethod
    def _merge_configs(default: dict, custom: dict) -> dict:
        """Recursively merge configuration dictionaries."""
        result = default.copy()
        for key, value in custom.items():
            if (
                key in result
                and isinstance(result[key], dict)
                and isinstance(value, dict)
            ):
                result[key] = ConfigManager._merge_configs(result[key], value)
            else:
                result[key] = value
        return result

    def get_config(self, path: str, default: Any = None) -> Any:
        """Get configuration value by path
        path: dot-separated configuration path, such as"SYSTEM_OPTIONS.NETWORK.MQTT_INFO"
        """
        try:
            value = self._config
            for key in path.split("."):
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default

    def update_config(self, path: str, value: Any) -> bool:
        """Update specific configuration items
        path: dot-separated configuration path, such as"SYSTEM_OPTIONS.NETWORK.MQTT_INFO"
        """
        try:
            current = self._config
            *parts, last = path.split(".")
            for part in parts:
                current = current.setdefault(part, {})
            current[last] = value
            return self._save_config(self._config)
        except Exception as e:
            logger.error(f"Configuration update error {path}: {e}")
            return False

    def reload_config(self) -> bool:
        """Reload configuration file."""
        try:
            self._config = self._load_config()
            logger.info("Configuration file has been reloaded")
            return True
        except Exception as e:
            logger.error(f"Configuration reload failed: {e}")
            return False

    def generate_uuid(self) -> str:
        """Generate UUID v4."""
        return str(uuid.uuid4())

    def initialize_client_id(self):
        """Make sure the client ID is present."""
        if not self.get_config("SYSTEM_OPTIONS.CLIENT_ID"):
            client_id = self.generate_uuid()
            success = self.update_config("SYSTEM_OPTIONS.CLIENT_ID", client_id)
            if success:
                logger.info(f"New client ID generated: {client_id}")
            else:
                logger.error("Failed to save new client ID")

    def initialize_device_id_from_fingerprint(self, device_fingerprint):
        """Initialize the device ID from the device fingerprint."""
        if not self.get_config("SYSTEM_OPTIONS.DEVICE_ID"):
            try:
                # Get MAC address as DEVICE_ID from efuse.json
                mac_address = device_fingerprint.get_mac_address_from_efuse()
                if mac_address:
                    success = self.update_config(
                        "SYSTEM_OPTIONS.DEVICE_ID", mac_address
                    )
                    if success:
                        logger.info(f"Get DEVICE_ID from efuse.json: {mac_address}")
                    else:
                        logger.error("Failed to save DEVICE_ID")
                else:
                    logger.error("Unable to get MAC address from efuse.json")
                    # Alternate solution: Obtain directly from device fingerprint
                    fingerprint = device_fingerprint.generate_fingerprint()
                    mac_from_fingerprint = fingerprint.get("mac_address")
                    if mac_from_fingerprint:
                        success = self.update_config(
                            "SYSTEM_OPTIONS.DEVICE_ID", mac_from_fingerprint
                        )
                        if success:
                            logger.info(
                                f"Use the MAC address from the fingerprint as DEVICE_ID:"
                                f"{mac_from_fingerprint}"
                            )
                        else:
                            logger.error("Failed to save alternate DEVICE_ID")
            except Exception as e:
                logger.error(f"Error initializing DEVICE_ID: {e}")

    @classmethod
    def get_instance(cls):
        """Get the configuration manager instance."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
