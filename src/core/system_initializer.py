#!/usr/bin/env python3
"""The four-stage initialization process test script shows the coordination of the three stages of device identity preparation, configuration management, and OTA configuration acquisition. The activation process is implemented by the user themselves."""

import asyncio
import json
from pathlib import Path
from typing import Dict

from src.constants.system import InitializationStage
from src.core.ota import Ota
from src.utils.config_manager import ConfigManager
from src.utils.device_fingerprint import DeviceFingerprint
from src.utils.logging_config import get_logger

logger = get_logger(__name__)


class SystemInitializer:
    """System Initializer - Coordinates Four Phases"""

    def __init__(self):
        self.device_fingerprint = None
        self.config_manager = None
        self.ota = None
        self.current_stage = None
        self.activation_data = None
        self.activation_status = {
            "local_activated": False,  # local activation status
            "server_activated": False,  # Server activation status
            "status_consistent": True,  # Is the status consistent?
        }

    async def run_initialization(self) -> Dict:
        """Run the complete initialization process.

        Returns:
            Dict: initialization result, including activation status and whether the interface needs to be activated"""
        logger.info("Start the system initialization process")

        try:
            # Phase One: Device Identity Preparation
            await self.stage_1_device_fingerprint()

            # Phase 2: Configuration management initialization
            await self.stage_2_config_management()

            # The third stage: OTA obtains configuration
            await self.stage_3_ota_config()

            # Get activation version configuration
            activation_version = self.config_manager.get_config(
                "SYSTEM_OPTIONS.NETWORK.ACTIVATION_VERSION", "v1"
            )

            logger.info(f"Activation version: {activation_version}")

            # Determine whether activation process is required based on the activation version
            if activation_version == "v1":
                # v1 protocol: Return success directly after completing the first three stages.
                logger.info("v1 protocol: the first three phases are completed, no activation process is required")
                return {
                    "success": True,
                    "local_activated": True,
                    "server_activated": True,
                    "status_consistent": True,
                    "need_activation_ui": False,
                    "status_message": "v1 protocol initialization completed",
                    "activation_version": activation_version,
                }
            else:
                # v2 protocol: Need to analyze activation status
                logger.info("v2 protocol: analyze activation status")
                activation_result = self.analyze_activation_status()
                activation_result["activation_version"] = activation_version

                # Determine whether the process needs to be activated based on the analysis results
                if activation_result["need_activation_ui"]:
                    logger.info("Need to display activation interface")
                else:
                    logger.info("No need to display the activation interface, the device has been activated")

                return activation_result

        except Exception as e:
            logger.error(f"System initialization failed: {e}")
            return {"success": False, "error": str(e), "need_activation_ui": False}

    async def stage_1_device_fingerprint(self):
        """Phase One: Device Identity Preparation."""
        self.current_stage = InitializationStage.DEVICE_FINGERPRINT
        logger.info(f"start{self.current_stage.value}")

        # Initialize device fingerprint
        self.device_fingerprint = DeviceFingerprint.get_instance()

        # Ensure device identity information is complete
        (
            serial_number,
            hmac_key,
            is_activated,
        ) = self.device_fingerprint.ensure_device_identity()

        # Record local activation status
        self.activation_status["local_activated"] = is_activated

        # Get the MAC address and make sure it is in lower case
        mac_address = self.device_fingerprint.get_mac_address_from_efuse()

        logger.info(f"Device serial number: {serial_number}")
        logger.info(f"MAC address: {mac_address}")
        logger.info(f"HMAC key: {hmac_key[:8] if hmac_key else None}...")
        logger.info(f"Local activation status: {'activated' if is_activated else 'not activated'}")

        # Verify that the efuse.json file is complete
        efuse_file = Path("config/efuse.json")
        if efuse_file.exists():
            logger.info(f"efuse.json file location: {efuse_file.absolute()}")
            with open(efuse_file, "r", encoding="utf-8") as f:
                efuse_data = json.load(f)
            logger.debug(
                f"efuse.json content:"
                f"{json.dumps(efuse_data, indent=2, ensure_ascii=False)}"
            )
        else:
            logger.warning("efuse.json file does not exist")

        logger.info(f"Complete {self.current_stage.value}")

    async def stage_2_config_management(self):
        """Phase 2: Configuration management initialization."""
        self.current_stage = InitializationStage.CONFIG_MANAGEMENT
        logger.info(f"start{self.current_stage.value}")

        # Initialize configuration manager
        self.config_manager = ConfigManager.get_instance()

        # Make sure CLIENT_ID exists
        self.config_manager.initialize_client_id()

        # Initialize DEVICE_ID from device fingerprint
        self.config_manager.initialize_device_id_from_fingerprint(
            self.device_fingerprint
        )

        # Verify key configuration
        client_id = self.config_manager.get_config("SYSTEM_OPTIONS.CLIENT_ID")
        device_id = self.config_manager.get_config("SYSTEM_OPTIONS.DEVICE_ID")

        logger.info(f"Client ID: {client_id}")
        logger.info(f"Device ID: {device_id}")

        logger.info(f"Complete {self.current_stage.value}")

    async def stage_3_ota_config(self):
        """The third stage: OTA obtains the configuration."""
        self.current_stage = InitializationStage.OTA_CONFIG
        logger.info(f"start{self.current_stage.value}")

        # Initialize OTA
        self.ota = await Ota.get_instance()

        # Get and update configuration
        try:
            config_result = await self.ota.fetch_and_update_config()

            logger.info("OTA configuration acquisition results:")
            mqtt_status = "Obtained" if config_result["mqtt_config"] else "Not obtained"
            logger.info(f"- MQTT configuration: {mqtt_status}")

            ws_status = "Obtained" if config_result["websocket_config"] else "Not obtained"
            logger.info(f"- WebSocket configuration: {ws_status}")

            # Display a summary of the obtained configuration information
            response_data = config_result["response_data"]
            # Detailed configuration information is only displayed in debug mode
            logger.debug(
                f"OTA response data: {json.dumps(response_data, indent=2, ensure_ascii=False)}"
            )

            if "websocket" in response_data:
                ws_info = response_data["websocket"]
                logger.info(f"WebSocket URL: {ws_info.get('url', 'N/A')}")

            # Check if there is activation information
            if "activation" in response_data:
                logger.info("Activation information detected, the device needs to be activated")
                self.activation_data = response_data["activation"]
                # The server thinks the device is not activated
                self.activation_status["server_activated"] = False
            else:
                logger.info("No activation information detected, the device may have been activated")
                self.activation_data = None
                # The server thinks the device is activated
                self.activation_status["server_activated"] = True

        except Exception as e:
            logger.error(f"OTA configuration acquisition failed: {e}")
            raise

        logger.info(f"Complete {self.current_stage.value}")

    def analyze_activation_status(self) -> Dict:
        """Analyze the activation status and decide the subsequent process.

        Returns:
            Dict: analysis results, including whether the interface needs to be activated and other information"""
        local_activated = self.activation_status["local_activated"]
        server_activated = self.activation_status["server_activated"]

        # Check whether the status is consistent
        status_consistent = local_activated == server_activated
        self.activation_status["status_consistent"] = status_consistent

        result = {
            "success": True,
            "local_activated": local_activated,
            "server_activated": server_activated,
            "status_consistent": status_consistent,
            "need_activation_ui": False,
            "status_message": "",
        }

        # Case 1: Not activated locally, server returns activation data - normal activation process
        if not local_activated and not server_activated:
            result["need_activation_ui"] = True
            result["status_message"] = "Device needs activation"

        # Case 2: Locally activated, server has no activation data - normal activated state
        elif local_activated and server_activated:
            result["need_activation_ui"] = False
            result["status_message"] = "Device is activated"

        # Situation 3: Not activated locally, but no activation data on the server - status inconsistent, automatically repaired
        elif not local_activated and server_activated:
            logger.warning(
                "Inconsistent status: It is not activated locally, but the server thinks it is activated and automatically repairs the local status."
            )
            # Automatically update local status to activated
            self.device_fingerprint.set_activation_status(True)
            result["need_activation_ui"] = False
            result["status_message"] = "Activation status has been automatically repaired"
            result["local_activated"] = True  # Update status in results

        # Situation 4: Local activation, but server returns activation data - status inconsistent, try to repair automatically
        elif local_activated and not server_activated:
            logger.warning("Inconsistent status: It is activated locally, but the server thinks it is not activated. Try to repair it automatically.")

            # Check if there is activation data
            if self.activation_data and isinstance(self.activation_data, dict):
                # If you have an activation code, you need to reactivate it
                if "code" in self.activation_data:
                    logger.info("The server returned an activation code and needs to be reactivated.")
                    result["need_activation_ui"] = True
                    result["status_message"] = "Activation status is inconsistent and needs to be reactivated"
                else:
                    # There is no activation code. It may be that the server status has not been updated. Try to continue using it.
                    logger.info("The server did not return the activation code and the local activation status remained.")
                    result["need_activation_ui"] = False
                    result["status_message"] = "Keep locally active"
            else:
                # There is no activation data, it may be a network problem, keep the local status
                logger.info("Activation data not obtained, keep local activation status")
                result["need_activation_ui"] = False
                result["status_message"] = "Keep locally active"
                # Force update status consistency to avoid repeated activation
                result["status_consistent"] = True
                self.activation_status["status_consistent"] = True
                self.activation_status["server_activated"] = True

        return result

    def get_activation_data(self):
        """Get activation data (for use by the activation module)"""
        return getattr(self, "activation_data", None)

    def get_device_fingerprint(self):
        """Get device fingerprint instance."""
        return self.device_fingerprint

    def get_config_manager(self):
        """Get the configuration manager instance."""
        return self.config_manager

    def get_activation_status(self) -> Dict:
        """Get activation status information."""
        return self.activation_status

    async def handle_activation_process(self, mode: str = "gui") -> Dict:
        """Handle the activation process and create activation interfaces as needed.

        Args:
            mode: interface mode,"gui"or"cli"Returns:
            Dict: activation result"""
        # Run the initialization process first
        init_result = await self.run_initialization()

        # If there is no need to activate the interface, return the result directly
        if not init_result.get("need_activation_ui", False):
            return {
                "is_activated": True,
                "device_fingerprint": self.device_fingerprint,
                "config_manager": self.config_manager,
            }

        # The interface needs to be activated and created according to the mode
        if mode == "gui":
            return await self._run_gui_activation()
        else:
            return await self._run_cli_activation()

    async def _run_gui_activation(self) -> Dict:
        """Run the GUI activation process.

        Returns:
            Dict: activation result"""
        try:
            from src.views.activation.activation_window import ActivationWindow

            # Create activation window
            activation_window = ActivationWindow(self)

            # Create a Future to wait for activation to complete
            activation_future = asyncio.Future()

            # Set activation completion callback
            def on_activation_completed(success: bool):
                if not activation_future.done():
                    activation_future.set_result(success)

            # Set window close callback
            def on_window_closed():
                if not activation_future.done():
                    activation_future.set_result(False)

            # Connect signal
            activation_window.activation_completed.connect(on_activation_completed)
            activation_window.window_closed.connect(on_window_closed)

            # Show activation window
            activation_window.show()

            # Wait for activation to complete
            activation_success = await activation_future

            # close window
            activation_window.close()

            return {
                "is_activated": activation_success,
                "device_fingerprint": self.device_fingerprint,
                "config_manager": self.config_manager,
            }

        except Exception as e:
            logger.error(f"GUI activation process exception: {e}", exc_info=True)
            return {"is_activated": False, "error": str(e)}

    async def _run_cli_activation(self) -> Dict:
        """Run the CLI activation process.

        Returns:
            Dict: activation result"""
        try:
            from src.views.activation.cli_activation import CLIActivation

            # Create CLI activation handler
            cli_activation = CLIActivation(self)

            # Run the activation process
            activation_success = await cli_activation.run_activation_process()

            return {
                "is_activated": activation_success,
                "device_fingerprint": self.device_fingerprint,
                "config_manager": self.config_manager,
            }

        except Exception as e:
            logger.error(f"CLI activation process exception: {e}", exc_info=True)
            return {"is_activated": False, "error": str(e)}
