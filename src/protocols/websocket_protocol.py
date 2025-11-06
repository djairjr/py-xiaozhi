import asyncio
import json
import ssl
import time

import websockets

from src.constants.constants import AudioConfig
from src.protocols.protocol import Protocol
from src.utils.config_manager import ConfigManager
from src.utils.logging_config import get_logger

ssl_context = ssl._create_unverified_context()

logger = get_logger(__name__)


class WebsocketProtocol(Protocol):
    def __init__(self):
        super().__init__()
        # Get configuration manager instance
        self.config = ConfigManager.get_instance()
        self.websocket = None
        self.connected = False
        self.hello_received = None  # Set to None when initializing
        # Message processing task reference for easy cancellation on shutdown
        self._message_task = None

        # Connect health status monitoring
        self._last_ping_time = None
        self._last_pong_time = None
        self._ping_interval = 30.0  # Heartbeat interval (seconds)
        self._ping_timeout = 10.0  # ping timeout (seconds)
        self._heartbeat_task = None
        self._connection_monitor_task = None

        # connection status flag
        self._is_closing = False
        self._reconnect_attempts = 0
        self._max_reconnect_attempts = 0  # Do not reconnect by default
        self._auto_reconnect_enabled = False  # Automatic reconnection is turned off by default

        self.WEBSOCKET_URL = self.config.get_config(
            "SYSTEM_OPTIONS.NETWORK.WEBSOCKET_URL"
        )
        access_token = self.config.get_config(
            "SYSTEM_OPTIONS.NETWORK.WEBSOCKET_ACCESS_TOKEN"
        )
        device_id = self.config.get_config("SYSTEM_OPTIONS.DEVICE_ID")
        client_id = self.config.get_config("SYSTEM_OPTIONS.CLIENT_ID")

        self.HEADERS = {
            "Authorization": f"Bearer {access_token}",
            "Protocol-Version": "1",
            "Device-Id": device_id,  # Get device MAC address
            "Client-Id": client_id,
        }

    async def connect(self) -> bool:
        """Connect to the WebSocket server."""
        if self._is_closing:
            logger.warning("The connection is being closed, cancel new connection attempt")
            return False

        try:
            # Create an Event when connecting, making sure you are in the correct event loop
            self.hello_received = asyncio.Event()

            # Determine if SSL should be used
            current_ssl_context = None
            if self.WEBSOCKET_URL.startswith("wss://"):
                current_ssl_context = ssl_context

            # Establish a WebSocket connection (compatible with different Python versions)
            try:
                # New way of writing (in Python 3.11+)
                self.websocket = await websockets.connect(
                    uri=self.WEBSOCKET_URL,
                    ssl=current_ssl_context,
                    additional_headers=self.HEADERS,
                    ping_interval=20,  # Use websockets own heartbeat, 20 second interval
                    ping_timeout=20,  # ping timeout 20 seconds
                    close_timeout=10,  # Close timeout 10 seconds
                    max_size=10 * 1024 * 1024,  # Maximum message 10MB
                    compression=None,  # Disable compression to improve stability
                )
            except TypeError:
                # Old way of writing (in older Python versions)
                self.websocket = await websockets.connect(
                    self.WEBSOCKET_URL,
                    ssl=current_ssl_context,
                    extra_headers=self.HEADERS,
                    ping_interval=20,  # Use websockets for your own heartbeat
                    ping_timeout=20,  # ping timeout 20 seconds
                    close_timeout=10,  # Close timeout 10 seconds
                    max_size=10 * 1024 * 1024,  # Maximum message 10MB
                    compression=None,  # Disable compression
                )

            # Start message processing loop (save task reference, can be canceled when closing)
            self._message_task = asyncio.create_task(self._message_handler())

            # Comment out the custom heartbeat and use the built-in heartbeat mechanism of websockets
            # self._start_heartbeat()

            # Start connection monitoring
            self._start_connection_monitor()

            # Send client hello message
            hello_message = {
                "type": "hello",
                "version": 1,
                "features": {
                    "mcp": True,
                },
                "transport": "websocket",
                "audio_params": {
                    "format": "opus",
                    "sample_rate": AudioConfig.INPUT_SAMPLE_RATE,
                    "channels": AudioConfig.CHANNELS,
                    "frame_duration": AudioConfig.FRAME_DURATION,
                },
            }
            await self.send_text(json.dumps(hello_message))

            # Wait for server hello response
            try:
                await asyncio.wait_for(self.hello_received.wait(), timeout=10.0)
                self.connected = True
                self._reconnect_attempts = 0  # Reset reconnection count
                logger.info("Connected to WebSocket server")

                # Notify connection status changes
                if self._on_connection_state_changed:
                    self._on_connection_state_changed(True, "Connection successful")

                return True
            except asyncio.TimeoutError:
                logger.error("Timeout waiting for server hello response")
                await self._cleanup_connection()
                if self._on_network_error:
                    self._on_network_error("Timeout waiting for response")
                return False

        except Exception as e:
            logger.error(f"WebSocket connection failed: {e}")
            await self._cleanup_connection()
            if self._on_network_error:
                self._on_network_error(f"Unable to connect to service: {str(e)}")
            return False

    def _start_heartbeat(self):
        """Start the heartbeat detection task."""
        if self._heartbeat_task is None or self._heartbeat_task.done():
            self._heartbeat_task = asyncio.create_task(self._heartbeat_loop())

    def _start_connection_monitor(self):
        """Start the connection monitoring task."""
        if (
            self._connection_monitor_task is None
            or self._connection_monitor_task.done()
        ):
            self._connection_monitor_task = asyncio.create_task(
                self._connection_monitor()
            )

    async def _heartbeat_loop(self):
        """Heartbeat detection loop."""
        try:
            while self.websocket and not self._is_closing:
                await asyncio.sleep(self._ping_interval)

                if self.websocket and not self._is_closing:
                    try:
                        self._last_ping_time = time.time()
                        # Send ping and wait for pong response
                        pong_waiter = await self.websocket.ping()
                        logger.debug("Send heartbeat ping")

                        # Wait for pong response
                        try:
                            await asyncio.wait_for(
                                pong_waiter, timeout=self._ping_timeout
                            )
                            self._last_pong_time = time.time()
                            logger.debug("Heartbeat pong response received")
                        except asyncio.TimeoutError:
                            logger.warning("Heartbeat pong response timeout")
                            await self._handle_connection_loss("Heartbeat pong timeout")
                            break

                    except Exception as e:
                        logger.error(f"Failed to send heartbeat: {e}")
                        await self._handle_connection_loss("Heartbeat sending failed")
                        break
        except asyncio.CancelledError:
            logger.debug("Heartbeat task canceled")
        except Exception as e:
            logger.error(f"Abnormal heartbeat circulation: {e}")

    async def _connection_monitor(self):
        """Connection health status monitoring."""
        try:
            while self.websocket and not self._is_closing:
                await asyncio.sleep(5)  # Check every 5 seconds

                # Check connection status
                if self.websocket:
                    if self.websocket.close_code is not None:
                        logger.warning("Detected WebSocket connection closed")
                        await self._handle_connection_loss("connection closed")
                        break

        except asyncio.CancelledError:
            logger.debug("The connection monitoring task was canceled")
        except Exception as e:
            logger.error(f"Connection monitoring exception: {e}")

    async def _handle_connection_loss(self, reason: str):
        """Handle connection loss."""
        logger.warning(f"Connection lost: {reason}")

        # Update connection status
        was_connected = self.connected
        self.connected = False

        # Notify connection status changes
        if self._on_connection_state_changed and was_connected:
            try:
                self._on_connection_state_changed(False, reason)
            except Exception as e:
                logger.error(f"Failed to call connection status change callback: {e}")

        # clean connection
        await self._cleanup_connection()

        # Notification audio channel closed
        if self._on_audio_channel_closed:
            try:
                await self._on_audio_channel_closed()
            except Exception as e:
                logger.error(f"Failed to call audio channel close callback: {e}")

        # Only attempt to reconnect if auto-reconnect is enabled and not manually turned off
        if (
            not self._is_closing
            and self._auto_reconnect_enabled
            and self._reconnect_attempts < self._max_reconnect_attempts
        ):
            await self._attempt_reconnect(reason)
        else:
            # Notify network errors
            if self._on_network_error:
                if (
                    self._auto_reconnect_enabled
                    and self._reconnect_attempts >= self._max_reconnect_attempts
                ):
                    self._on_network_error(f"Connection lost and reconnection failed: {reason}")
                else:
                    self._on_network_error(f"Connection lost: {reason}")

    async def _attempt_reconnect(self, original_reason: str):
        """Try to reconnect automatically."""
        self._reconnect_attempts += 1

        # Notification to start reconnection
        if self._on_reconnecting:
            try:
                self._on_reconnecting(
                    self._reconnect_attempts, self._max_reconnect_attempts
                )
            except Exception as e:
                logger.error(f"Failed to call reconnection callback: {e}")

        logger.info(
            f"Attempt automatic reconnection ({self._reconnect_attempts}/{self._max_reconnect_attempts})"
        )

        # Wait for a while and then reconnect.
        await asyncio.sleep(min(self._reconnect_attempts * 2, 30))  # Exponential backoff, maximum 30 seconds

        try:
            success = await self.connect()
            if success:
                logger.info("Automatic reconnection successful")
                # Notify connection status changes
                if self._on_connection_state_changed:
                    self._on_connection_state_changed(True, "Reconnection successful")
            else:
                logger.warning(
                    f"Automatic reconnection failed ({self._reconnect_attempts}/{self._max_reconnect_attempts})"
                )
                # If you can try again, don’t report an error immediately.
                if self._reconnect_attempts >= self._max_reconnect_attempts:
                    if self._on_network_error:
                        self._on_network_error(
                            f"Reconnection failed, the maximum number of reconnections has been reached: {original_reason}"
                        )
        except Exception as e:
            logger.error(f"An error occurred during reconnection: {e}")
            if self._reconnect_attempts >= self._max_reconnect_attempts:
                if self._on_network_error:
                    self._on_network_error(f"Reconnect exception: {str(e)}")

    def enable_auto_reconnect(self, enabled: bool = True, max_attempts: int = 5):
        """Enable or disable automatic reconnection.

        Args:
            enabled: Whether to enable automatic reconnection
            max_attempts: Maximum number of reconnection attempts"""
        self._auto_reconnect_enabled = enabled
        if enabled:
            self._max_reconnect_attempts = max_attempts
            logger.info(f"Enable automatic reconnection, maximum number of attempts: {max_attempts}")
        else:
            self._max_reconnect_attempts = 0
            logger.info("Disable automatic reconnection")

    def get_connection_info(self) -> dict:
        """Get connection information.

        Returns:
            dict: A dictionary containing information such as connection status, reconnection times, etc."""
        return {
            "connected": self.connected,
            "websocket_closed": (
                self.websocket.close_code is not None if self.websocket else True
            ),
            "is_closing": self._is_closing,
            "auto_reconnect_enabled": self._auto_reconnect_enabled,
            "reconnect_attempts": self._reconnect_attempts,
            "max_reconnect_attempts": self._max_reconnect_attempts,
            "last_ping_time": self._last_ping_time,
            "last_pong_time": self._last_pong_time,
            "websocket_url": self.WEBSOCKET_URL,
        }

    async def _message_handler(self):
        """Handle received WebSocket messages."""
        try:
            async for message in self.websocket:
                if self._is_closing:
                    break

                try:
                    if isinstance(message, str):
                        try:
                            data = json.loads(message)
                            msg_type = data.get("type")
                            if msg_type == "hello":
                                # Handling server hello messages
                                await self._handle_server_hello(data)
                            else:
                                if self._on_incoming_json:
                                    self._on_incoming_json(data)
                        except json.JSONDecodeError as e:
                            logger.error(f"Invalid JSON message: {message}, error: {e}")
                    elif isinstance(message, bytes):
                        # Binary message, possibly audio
                        if self._on_incoming_audio:
                            self._on_incoming_audio(message)
                except Exception as e:
                    # Handle errors for a single message, but continue processing other messages
                    logger.error(f"Error while processing message: {e}", exc_info=True)
                    continue

        except asyncio.CancelledError:
            logger.debug("The message processing task was canceled")
            return
        except websockets.ConnectionClosed as e:
            if not self._is_closing:
                logger.info(f"WebSocket connection closed: {e}")
                await self._handle_connection_loss(f"Connection closed: {e.code} {e.reason}")
        except websockets.ConnectionClosedError as e:
            if not self._is_closing:
                logger.info(f"WebSocket connection error closed: {e}")
                await self._handle_connection_loss(f"Connection error: {e.code} {e.reason}")
        except websockets.InvalidState as e:
            logger.error(f"Invalid WebSocket status: {e}")
            await self._handle_connection_loss("Abnormal connection status")
        except ConnectionResetError:
            logger.warning("connection reset")
            await self._handle_connection_loss("connection reset")
        except OSError as e:
            logger.error(f"Network I/O error: {e}")
            await self._handle_connection_loss("Network I/O error")
        except Exception as e:
            logger.error(f"Message processing loop exception: {e}", exc_info=True)
            await self._handle_connection_loss(f"Message processing exception: {str(e)}")

    async def send_audio(self, data: bytes):
        """Send audio data."""
        if not self.is_audio_channel_opened():
            return

        try:
            await self.websocket.send(data)
        except websockets.ConnectionClosed as e:
            logger.warning(f"Connection closed while sending audio: {e}")
            await self._handle_connection_loss(f"Failed to send audio: {e.code} {e.reason}")
        except websockets.ConnectionClosedError as e:
            logger.warning(f"Connection error while sending audio: {e}")
            await self._handle_connection_loss(f"Sending audio error: {e.code} {e.reason}")
        except Exception as e:
            logger.error(f"Failed to send audio data: {e}")
            # Don't call the network error callback here, let the connection handler handle it
            await self._handle_connection_loss(f"Send audio exception: {str(e)}")

    async def send_text(self, message: str):
        """Send a text message."""
        if not self.websocket or self._is_closing:
            logger.warning("WebSocket is not connected or is closing, unable to send message")
            return

        try:
            await self.websocket.send(message)
        except websockets.ConnectionClosed as e:
            logger.warning(f"Connection closed while sending text: {e}")
            await self._handle_connection_loss(f"Failed to send text: {e.code} {e.reason}")
        except websockets.ConnectionClosedError as e:
            logger.warning(f"Connection error while sending text: {e}")
            await self._handle_connection_loss(f"Error sending text: {e.code} {e.reason}")
        except Exception as e:
            logger.error(f"Failed to send text message: {e}")
            await self._handle_connection_loss(f"Exception when sending text: {str(e)}")

    def is_audio_channel_opened(self) -> bool:
        """Check if the audio channel is open.

        More accurate checking of connection status, including the actual status of WebSocket"""
        if not self.websocket or not self.connected or self._is_closing:
            return False

        # Check the actual status of WebSocket
        try:
            return self.websocket.close_code is None
        except Exception:
            return False

    async def open_audio_channel(self) -> bool:
        """Establish a WebSocket connection.

        Create a new WebSocket connection if not already connected
        Returns:
            bool: whether the connection is successful"""
        if not self.is_audio_channel_opened():
            return await self.connect()
        return True

    async def _handle_server_hello(self, data: dict):
        """Handle the server's hello message."""
        try:
            # Verify transfer method
            transport = data.get("transport")
            if not transport or transport != "websocket":
                logger.error(f"Unsupported transport: {transport}")
                return

            # Set hello to receive events
            self.hello_received.set()

            # Notification audio channel is open
            if self._on_audio_channel_opened:
                await self._on_audio_channel_opened()

            logger.info("Server hello message successfully processed")

        except Exception as e:
            logger.error(f"Error processing server hello message: {e}")
            if self._on_network_error:
                self._on_network_error(f"Failed to process server response: {str(e)}")

    async def _cleanup_connection(self):
        """Clean up connection related resources."""
        self.connected = False

        # Cancel the message processing task to prevent the event loop from still waiting after exiting.
        if self._message_task and not self._message_task.done():
            self._message_task.cancel()
            try:
                await self._message_task
            except asyncio.CancelledError:
                pass
            except Exception as e:
                logger.debug(f"Exception when waiting for message task cancellation: {e}")
        self._message_task = None

        # Cancel heartbeat task
        if self._heartbeat_task and not self._heartbeat_task.done():
            self._heartbeat_task.cancel()
            try:
                await self._heartbeat_task
            except asyncio.CancelledError:
                pass

        # Cancel the connection monitoring task
        if self._connection_monitor_task and not self._connection_monitor_task.done():
            self._connection_monitor_task.cancel()
            try:
                await self._connection_monitor_task
            except asyncio.CancelledError:
                pass

        # Close WebSocket connection
        if self.websocket and self.websocket.close_code is None:
            try:
                await self.websocket.close()
            except Exception as e:
                logger.error(f"Error closing WebSocket connection: {e}")

        self.websocket = None
        self._last_ping_time = None
        self._last_pong_time = None

    async def close_audio_channel(self):
        """Close the audio channel."""
        self._is_closing = True

        try:
            await self._cleanup_connection()

            if self._on_audio_channel_closed:
                await self._on_audio_channel_closed()

        except Exception as e:
            logger.error(f"Failed to close audio channel: {e}")
        finally:
            self._is_closing = False
