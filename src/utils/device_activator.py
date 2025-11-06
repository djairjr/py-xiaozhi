import asyncio
import json
from typing import Optional

import aiohttp

from src.utils.common_utils import handle_verification_code
from src.utils.device_fingerprint import DeviceFingerprint
from src.utils.logging_config import get_logger

logger = get_logger(__name__)


class DeviceActivator:
    """Device Activation Manager - fully asynchronous version"""

    def __init__(self, config_manager):
        """Initialize the device activator."""
        self.logger = get_logger(__name__)
        self.config_manager = config_manager
        # Use device_fingerprint instances to manage device identities
        self.device_fingerprint = DeviceFingerprint.get_instance()
        # Make sure the device identity is created
        self._ensure_device_identity()

        # Currently active tasks
        self._activation_task: Optional[asyncio.Task] = None

    def _ensure_device_identity(self):
        """Make sure the device identity has been created."""
        (
            serial_number,
            hmac_key,
            is_activated,
        ) = self.device_fingerprint.ensure_device_identity()
        self.logger.info(
            f"Device identity information: Serial number: {serial_number}, activation status: {'activated' if is_activated else 'not activated'}"
        )

    def cancel_activation(self):
        """Deactivation process."""
        if self._activation_task and not self._activation_task.done():
            self.logger.info("Deactivating task")
            self._activation_task.cancel()

    def has_serial_number(self) -> bool:
        """Check if there is a serial number."""
        return self.device_fingerprint.has_serial_number()

    def get_serial_number(self) -> str:
        """Get the serial number."""
        return self.device_fingerprint.get_serial_number()

    def get_hmac_key(self) -> str:
        """Get the HMAC key."""
        return self.device_fingerprint.get_hmac_key()

    def set_activation_status(self, status: bool) -> bool:
        """Set activation status."""
        return self.device_fingerprint.set_activation_status(status)

    def is_activated(self) -> bool:
        """Check if the device is activated."""
        return self.device_fingerprint.is_activated()

    def generate_hmac(self, challenge: str) -> str:
        """Generate signature using HMAC key."""
        return self.device_fingerprint.generate_hmac(challenge)

    async def process_activation(self, activation_data: dict) -> bool:
        """Handle activation process asynchronously.

        Args:
            activation_data: dictionary containing activation information, which should at least contain challenge and code

        Returns:
            bool: whether activation was successful"""
        try:
            # Record current tasks
            self._activation_task = asyncio.current_task()

            # Check for activation challenge and verification code
            if not activation_data.get("challenge"):
                self.logger.error("Challenge field is missing in activation data")
                return False

            if not activation_data.get("code"):
                self.logger.error("Code field is missing in activation data")
                return False

            challenge = activation_data["challenge"]
            code = activation_data["code"]
            message = activation_data.get("message", "Please enter the verification code at xiaozhi.me")

            # Check serial number
            if not self.has_serial_number():
                self.logger.error("The device does not have a serial number and cannot be activated.")

                # Use device_fingerprint to generate serial numbers and HMAC keys
                (
                    serial_number,
                    hmac_key,
                    _,
                ) = self.device_fingerprint.ensure_device_identity()

                if serial_number and hmac_key:
                    self.logger.info("Device serial number and HMAC key automatically created")
                else:
                    self.logger.error("Failed to create serial number or HMAC key")
                    return False

            # Show activation information to user
            self.logger.info(f"Activation prompt: {message}")
            self.logger.info(f"Verification code: {code}")

            # Construct the verification code prompt text and print it
            text = f".Please log in to the control panel to add a device and enter the verification code: {' '.join(code)}..."
            print("\n==================")
            print(text)
            print("==================\n")
            handle_verification_code(text)

            # Use voice to play verification code
            try:
                # Play speech in a non-blocking thread
                from src.utils.common_utils import play_audio_nonblocking

                play_audio_nonblocking(text)
                self.logger.info("Verification code voice prompt is playing")
            except Exception as e:
                self.logger.error(f"Failed to play verification code voice: {e}")

            # Try to activate the device and pass the verification code information
            return await self.activate(challenge, code)

        except asyncio.CancelledError:
            self.logger.info("Activation process canceled")
            return False

    async def activate(self, challenge: str, code: str = None) -> bool:
        """Execute the activation process asynchronously.

        Args:
            challenge: challenge string sent by the server
            code: Verification code, used to play when retrying

        Returns:
            bool: whether activation was successful"""
        try:
            # Check serial number
            serial_number = self.get_serial_number()
            if not serial_number:
                self.logger.error("The device does not have a serial number and cannot complete the HMAC verification steps.")
                return False

            # Compute HMAC signature
            hmac_signature = self.generate_hmac(challenge)
            if not hmac_signature:
                self.logger.error("Unable to generate HMAC signature, activation failed")
                return False

            # Wrap an external payload in the format expected by the server
            payload = {
                "Payload": {
                    "algorithm": "hmac-sha256",
                    "serial_number": serial_number,
                    "challenge": challenge,
                    "hmac": hmac_signature,
                }
            }

            # Get activation URL
            ota_url = self.config_manager.get_config(
                "SYSTEM_OPTIONS.NETWORK.OTA_VERSION_URL"
            )
            if not ota_url:
                self.logger.error("OTA URL configuration not found")
                return False

            # Make sure the URL ends with a slash
            if not ota_url.endswith("/"):
                ota_url += "/"

            activate_url = f"{ota_url}activate"
            self.logger.info(f"Activation URL: {activate_url}")

            # Set request header
            headers = {
                "Activation-Version": "2",
                "Device-Id": self.config_manager.get_config("SYSTEM_OPTIONS.DEVICE_ID"),
                "Client-Id": self.config_manager.get_config("SYSTEM_OPTIONS.CLIENT_ID"),
                "Content-Type": "application/json",
            }

            # Print debugging information
            self.logger.debug(f"Request headers: {headers}")
            payload_str = json.dumps(payload, indent=2, ensure_ascii=False)
            self.logger.debug(f"Request payload: {payload_str}")

            # Retry logic
            max_retries = 60  # Maximum wait time is 5 minutes
            retry_interval = 5  # Set retry interval of 5 seconds

            error_count = 0
            last_error = None

            # Create an aiohttp session and set a reasonable timeout
            timeout = aiohttp.ClientTimeout(total=10)

            async with aiohttp.ClientSession(timeout=timeout) as session:
                for attempt in range(max_retries):
                    try:
                        self.logger.info(
                            f"Attempt to activate (try {attempt + 1}/{max_retries})..."
                        )

                        # Play verification code every time you retry (starting from the 2nd time)
                        if attempt > 0 and code:
                            try:
                                from src.utils.common_utils import (
                                    play_audio_nonblocking,
                                )

                                text = f".Please log in to the control panel to add a device and enter the verification code: {' '.join(code)}..."
                                play_audio_nonblocking(text)
                                self.logger.info(f"Retry playing verification code: {code}")
                            except Exception as e:
                                self.logger.error(f"Failed to retry playing verification code: {e}")

                        # Send activation request
                        async with session.post(
                            activate_url, headers=headers, json=payload
                        ) as response:
                            # Read response
                            response_text = await response.text()

                            # Print full response
                            self.logger.warning(f"\nActivation response (HTTP {response.status}):")
                            try:
                                response_json = json.loads(response_text)
                                self.logger.warning(json.dumps(response_json, indent=2))
                            except json.JSONDecodeError:
                                self.logger.warning(response_text)

                            # Check response status code
                            if response.status == 200:
                                # Activation successful
                                self.logger.info("Device activation successful!")
                                self.set_activation_status(True)
                                return True

                            elif response.status == 202:
                                # Wait for user to enter verification code
                                self.logger.info("Waiting for the user to enter the verification code, continue waiting...")

                                # Use cancelable wait
                                await asyncio.sleep(retry_interval)

                            else:
                                # Handle other errors but keep retrying
                                error_msg = "unknown error"
                                try:
                                    error_data = json.loads(response_text)
                                    error_msg = error_data.get(
                                        "error", f"Unknown error (status code: {response.status})"
                                    )
                                except json.JSONDecodeError:
                                    error_msg = (
                                        f"The server returned an error (status code: {response.status})"
                                    )

                                # Log errors but do not terminate the process
                                if error_msg != last_error:
                                    self.logger.warning(
                                        f"The server returns: {error_msg}, continue to wait for the verification code to be activated."
                                    )
                                    last_error = error_msg

                                # Count consecutive identical errors
                                if "Device not found" in error_msg:
                                    error_count += 1
                                    if error_count >= 5 and error_count % 5 == 0:
                                        self.logger.warning(
                                            "\nTip: If the error persists, you may need to refresh the page on the website to obtain a new verification code\n"
                                        )

                                # Use cancelable wait
                                await asyncio.sleep(retry_interval)

                    except asyncio.CancelledError:
                        # Respond to a cancellation signal
                        self.logger.info("Activation process canceled")
                        return False

                    except aiohttp.ClientError as e:
                        self.logger.warning(f"Network request failed: {e}, retrying...")
                        await asyncio.sleep(retry_interval)

                    except asyncio.TimeoutError as e:
                        self.logger.warning(f"Request timeout: {e}, retrying...")
                        await asyncio.sleep(retry_interval)

                    except Exception as e:
                        # Get exception details
                        import traceback

                        error_detail = (
                            str(e) if str(e) else f"{type(e).__name__}: Unknown error"
                        )
                        self.logger.warning(
                            f"An error occurred during activation: {error_detail}, retrying..."
                        )
                        # Print complete exception information in debug mode
                        self.logger.debug(f"Complete exception information: {traceback.format_exc()}")
                        await asyncio.sleep(retry_interval)

            # Maximum number of retries reached
            self.logger.error(
                f"Activation failed, maximum retries ({max_retries}) reached, last error: {last_error}"
            )
            return False

        except asyncio.CancelledError:
            self.logger.info("Activation process canceled")
            return False
