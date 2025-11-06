import asyncio
import json
import socket
import ssl

import aiohttp

from src.constants.system import SystemConstants
from src.utils.config_manager import ConfigManager
from src.utils.device_fingerprint import DeviceFingerprint
from src.utils.logging_config import get_logger


class Ota:
    _instance = None
    _lock = asyncio.Lock()

    def __init__(self):
        self.logger = get_logger(__name__)
        self.config = ConfigManager.get_instance()
        self.device_fingerprint = DeviceFingerprint.get_instance()
        self.mac_addr = None
        self.ota_version_url = None
        self.local_ip = None
        self.system_info = None

    @classmethod
    async def get_instance(cls):
        if cls._instance is None:
            async with cls._lock:
                if cls._instance is None:
                    instance = cls()
                    await instance.init()
                    cls._instance = instance
        return cls._instance

    async def init(self):
        """Initialize the OTA instance."""
        self.local_ip = await self.get_local_ip()
        # Get device ID (MAC address) from configuration
        self.mac_addr = self.config.get_config("SYSTEM_OPTIONS.DEVICE_ID")
        # Get OTA URL
        self.ota_version_url = self.config.get_config(
            "SYSTEM_OPTIONS.NETWORK.OTA_VERSION_URL"
        )

    async def get_local_ip(self):
        """Get the local IP address asynchronously."""
        try:
            loop = asyncio.get_running_loop()
            return await loop.run_in_executor(None, self._sync_get_ip)
        except Exception as e:
            self.logger.error(f"Failed to obtain local IP: {e}")
            return "127.0.0.1"

    def _sync_get_ip(self):
        """Get IP address synchronously."""
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]

    def build_payload(self):
        """Construct the payload of the OTA request."""
        # Get hmac_key from efuse.json as elf_sha256
        hmac_key = self.device_fingerprint.get_hmac_key()
        elf_sha256 = hmac_key if hmac_key else "unknown"

        return {
            "application": {
                "version": SystemConstants.APP_VERSION,
                "elf_sha256": elf_sha256,
            },
            "board": {
                "type": SystemConstants.BOARD_TYPE,
                "name": SystemConstants.APP_NAME,
                "ip": self.local_ip,
                "mac": self.mac_addr,
            },
        }

    def build_headers(self):
        """Construct headers for OTA requests."""
        app_version = SystemConstants.APP_VERSION
        board_type = SystemConstants.BOARD_TYPE
        app_name = SystemConstants.APP_NAME

        # Basic head
        headers = {
            "Device-Id": self.mac_addr,
            "Client-Id": self.config.get_config("SYSTEM_OPTIONS.CLIENT_ID"),
            "Content-Type": "application/json",
            "User-Agent": f"{board_type}/{app_name}-{app_version}",
            "Accept-Language": "zh-CN",
        }

        # Determine whether to add the Activation-Version header based on the activation version
        activation_version = self.config.get_config(
            "SYSTEM_OPTIONS.NETWORK.ACTIVATION_VERSION", "v1"
        )

        # Only the v2 protocol adds the Activation-Version header
        if activation_version == "v2":
            headers["Activation-Version"] = app_version
            self.logger.debug(f"v2 protocol: Add Activation-Version header: {app_version}")
        else:
            self.logger.debug("v1 protocol: Do not add Activation-Version header")

        return headers

    async def get_ota_config(self):
        """Obtain the configuration information of the OTA server (MQTT, WebSocket, etc.)"""
        if not self.mac_addr:
            self.logger.error("Device ID (MAC address) is not configured")
            raise ValueError("Device ID is not configured")

        if not self.ota_version_url:
            self.logger.error("OTA URL not configured")
            raise ValueError("OTA URL not configured")

        headers = self.build_headers()
        payload = self.build_payload()

        try:
            # Disable SSL certificate verification in favor of self-signed certificates
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE

            # Use aiohttp to send requests asynchronously
            timeout = aiohttp.ClientTimeout(total=10)
            connector = aiohttp.TCPConnector(ssl=ssl_context)
            async with aiohttp.ClientSession(
                timeout=timeout, connector=connector
            ) as session:
                async with session.post(
                    self.ota_version_url, headers=headers, json=payload
                ) as response:
                    # Check HTTP status code
                    if response.status != 200:
                        self.logger.error(f"OTA server error: HTTP {response.status}")
                        raise ValueError(f"The OTA server returns error status code: {response.status}")

                    # Parse JSON data
                    response_data = await response.json()

                    # Debug information: Print full OTA response
                    self.logger.debug(
                        f"OTA server returns data:"
                        f"{json.dumps(response_data, indent=4, ensure_ascii=False)}"
                    )

                    return response_data

        except asyncio.TimeoutError:
            self.logger.error("OTA request timed out, please check network or server status")
            raise ValueError("OTA request timed out! Please try again later.")

        except aiohttp.ClientError as e:
            self.logger.error(f"OTA request failed: {e}")
            raise ValueError("Unable to connect to OTA server, please check the network connection!")

    async def update_mqtt_config(self, response_data):
        """Update MQTT configuration information."""
        if "mqtt" in response_data:
            self.logger.info("Discover MQTT configuration information")
            mqtt_info = response_data["mqtt"]
            if mqtt_info:
                # Update configuration
                success = self.config.update_config(
                    "SYSTEM_OPTIONS.NETWORK.MQTT_INFO", mqtt_info
                )
                if success:
                    self.logger.info("MQTT configuration updated")
                    return mqtt_info
                else:
                    self.logger.error("MQTT configuration update failed")
            else:
                self.logger.warning("MQTT configuration is empty")
        else:
            self.logger.info("No MQTT configuration information found")

        return None

    async def update_websocket_config(self, response_data):
        """Update WebSocket configuration information."""
        if "websocket" in response_data:
            self.logger.info("Discover WebSocket configuration information")
            websocket_info = response_data["websocket"]

            # Update WebSocket URL
            if "url" in websocket_info:
                self.config.update_config(
                    "SYSTEM_OPTIONS.NETWORK.WEBSOCKET_URL", websocket_info["url"]
                )
                self.logger.info(f"WebSocket URL updated: {websocket_info['url']}")

            # Update WebSocket Token
            token_value = websocket_info.get("token", "test-token") or "test-token"
            self.config.update_config(
                "SYSTEM_OPTIONS.NETWORK.WEBSOCKET_ACCESS_TOKEN", token_value
            )
            self.logger.info("WebSocket Token has been updated")

            return websocket_info
        else:
            self.logger.info("WebSocket configuration information not found")

        return None

    async def fetch_and_update_config(self):
        """Get and update all configuration information."""
        try:
            # Get OTA configuration
            response_data = await self.get_ota_config()

            # Update MQTT configuration
            mqtt_config = await self.update_mqtt_config(response_data)

            # Update WebSocket configuration
            websocket_config = await self.update_websocket_config(response_data)

            # Return complete response data for use in the activation process
            return {
                "response_data": response_data,
                "mqtt_config": mqtt_config,
                "websocket_config": websocket_config,
            }

        except Exception as e:
            self.logger.error(f"Failed to get and update configuration: {e}")
            raise
