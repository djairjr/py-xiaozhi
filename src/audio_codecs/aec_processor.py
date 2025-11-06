import platform
from collections import deque
from typing import Any, Dict, Optional

import numpy as np
import sounddevice as sd

from src.constants.constants import AudioConfig
from src.utils.logging_config import get_logger

logger = get_logger(__name__)


class AECProcessor:
    """Audio Echo Cancellation Processor AEC specifically designed to process the reference signal (speaker output) and microphone input."""

    def __init__(self):
        # Platform information
        self._platform = platform.system().lower()
        self._is_macos = self._platform == "darwin"
        self._is_linux = self._platform == "linux"
        self._is_windows = self._platform == "windows"

        # WebRTC APM instance (for macOS only)
        self.apm = None
        self.apm_config = None
        self.capture_config = None
        self.render_config = None

        # Reference signal flow (macOS only)
        self.reference_stream = None
        self.reference_device_id = None
        self.reference_sample_rate = None

        # buffer
        self._reference_buffer = deque()
        self._webrtc_frame_size = 160  # WebRTC standard: 16kHz, 10ms = 160 samples
        self._system_frame_size = AudioConfig.INPUT_FRAME_SIZE  # System configured frame size

        # status flag
        self._is_initialized = False
        self._is_closing = False

    async def initialize(self):
        """Initialize the AEC processor."""
        try:
            if self._is_windows or self._is_linux:
                # Windows and Linux platforms use system-level AEC without additional processing
                logger.info(
                    f"{self._platform.capitalize()} Platform uses system-level echo cancellation, AEC processor is enabled"
                )
                self._is_initialized = True
                return
            elif self._is_macos:
                # macOS platform uses WebRTC + BlackHole
                await self._initialize_apm()
                await self._initialize_reference_capture()
            else:
                logger.warning(f"The current platform {self._platform} does not currently support the AEC function.")
                self._is_initialized = True
                return

            self._is_initialized = True
            logger.info("AEC processor initialization completed")

        except Exception as e:
            logger.error(f"AEC processor initialization failed: {e}")
            await self.close()
            raise

    async def _initialize_apm(self):
        """Initialize the WebRTC audio processing module (macOS only)"""
        if not self._is_macos:
            logger.warning("Non-macOS platforms called _initialize_apm, which shouldn't happen")
            return

        try:
            # Lazy import, only loading native libraries when macOS requires them
            from libs.webrtc_apm import WebRTCAudioProcessing, create_default_config

            self.apm = WebRTCAudioProcessing()

            # Create configuration
            self.apm_config = create_default_config()

            # Enable echo cancellation
            self.apm_config.echo.enabled = True
            self.apm_config.echo.mobile_mode = False
            self.apm_config.echo.enforce_high_pass_filtering = True

            # Enable noise suppression
            self.apm_config.noise_suppress.enabled = True
            self.apm_config.noise_suppress.noise_level = 2  # HIGH

            # Enable high pass filter
            self.apm_config.high_pass.enabled = True
            self.apm_config.high_pass.apply_in_full_band = True

            # Application configuration
            result = self.apm.apply_config(self.apm_config)
            if result != 0:
                raise RuntimeError(f"WebRTC APM configuration failed, error code: {result}")

            # Create flow configuration
            sample_rate = AudioConfig.INPUT_SAMPLE_RATE  # 16kHz
            channels = AudioConfig.CHANNELS  # 1

            self.capture_config = self.apm.create_stream_config(sample_rate, channels)
            self.render_config = self.apm.create_stream_config(sample_rate, channels)

            # Set streaming delay
            self.apm.set_stream_delay_ms(40)  # 50ms delay

            logger.info("WebRTC APM initialization completed")

        except Exception as e:
            logger.error(f"WebRTC APM initialization failed: {e}")
            raise

    async def _initialize_reference_capture(self):
        """Initialize reference signal capture (macOS only)"""
        if not self._is_macos:
            return

        try:
            # Find BlackHole 2ch devices
            reference_device = self._find_blackhole_device()
            if reference_device is None:
                logger.warning("BlackHole 2ch device not found, reference signal capture is not available")
                return

            self.reference_device_id = reference_device["id"]
            self.reference_sample_rate = int(reference_device["default_samplerate"])

            # Create a reference signal input stream (fixed use of 10ms frame, matching WebRTC standard)
            webrtc_frame_duration = 0.01  # 10ms, WebRTC standard frame length
            reference_frame_size = int(
                self.reference_sample_rate * webrtc_frame_duration
            )

            self.reference_stream = sd.InputStream(
                device=self.reference_device_id,
                samplerate=self.reference_sample_rate,
                channels=AudioConfig.CHANNELS,
                dtype=np.int16,
                blocksize=reference_frame_size,
                callback=self._reference_callback,
                finished_callback=self._reference_finished_callback,
                latency="low",
            )

            self.reference_stream.start()

            logger.info(
                f"Reference signal capture started: [{self.reference_device_id}] {reference_device['name']}"
            )

        except Exception as e:
            logger.error(f"Reference signal capture initialization failed: {e}")
            # Does not throw an exception, allowing AEC to operate without a reference signal

    def _find_blackhole_device(self) -> Optional[Dict[str, Any]]:
        """Find the BlackHole 2ch virtual appliance."""
        try:
            devices = sd.query_devices()
            for i, device in enumerate(devices):
                device_name = device["name"].lower()
                # Find BlackHole 2ch devices
                if "blackhole" in device_name and "2ch" in device_name:
                    # Make sure it is an input device
                    if device["max_input_channels"] >= 1:
                        device_info = dict(device)
                        device_info["id"] = i
                        logger.info(f"Find the BlackHole device: [{i}] {device['name']}")
                        return device_info

            # If you don't find a specific BlackHole 2ch, try looking for any BlackHole device
            for i, device in enumerate(devices):
                device_name = device["name"].lower()
                if "blackhole" in device_name and device["max_input_channels"] >= 1:
                    device_info = dict(device)
                    device_info["id"] = i
                    logger.info(f"Find the BlackHole device: [{i}] {device['name']}")
                    return device_info

            return None

        except Exception as e:
            logger.error(f"Failed to find BlackHole device: {e}")
            return None

    def _reference_callback(self, indata, frames, time_info, status):
        """Reference signal callback."""
        # frames, time_info is used for sounddevice callback, it is not used here but the signature needs to be retained.
        _ = frames, time_info

        if status and "overflow" not in str(status).lower():
            logger.warning(f"Reference signal flow status: {status}")

        if self._is_closing:
            return

        try:
            audio_data = indata.copy().flatten()

            # Resample to 16kHz (if needed)
            if self.reference_sample_rate != AudioConfig.INPUT_SAMPLE_RATE:
                # Simple downsampling (better resamplers should be used in real applications)
                ratio = AudioConfig.INPUT_SAMPLE_RATE / self.reference_sample_rate
                target_length = int(len(audio_data) * ratio)
                audio_data = np.interp(
                    np.linspace(0, len(audio_data) - 1, target_length),
                    np.arange(len(audio_data)),
                    audio_data,
                ).astype(np.int16)

            # Add to reference buffer
            self._reference_buffer.extend(audio_data)

            # Keep buffer sizes reasonable
            max_buffer_size = self._webrtc_frame_size * 20  # Keep data for about 200ms
            while len(self._reference_buffer) > max_buffer_size:
                self._reference_buffer.popleft()

        except Exception as e:
            logger.error(f"Reference signal callback error: {e}")

    def _reference_finished_callback(self):
        """Reference signal flow end callback."""
        logger.info("Reference signal flow has ended")

    def process_audio(self, capture_audio: np.ndarray) -> np.ndarray:
        """To process audio frames, apply AEC to support different frame lengths such as 10ms/20ms/40ms/60ms, etc., implemented through segmentation processing.

        Args:
            capture_audio: audio data collected by the microphone (16kHz, int16)

        Returns:
            Processed audio data"""
        if not self._is_initialized:
            return capture_audio

        # Windows and Linux platforms return raw audio directly (system-level processing)
        if self._is_windows or self._is_linux:
            return capture_audio

        # macOS platform uses WebRTC AEC processing
        if not self._is_macos or self.apm is None:
            return capture_audio

        try:
            # Check if the input frame size is an integer multiple of the WebRTC frame size
            if len(capture_audio) % self._webrtc_frame_size != 0:
                logger.warning(
                    f"The audio frame size is not an integer multiple of the WebRTC frame: {len(capture_audio)}, WebRTC frame: {self._webrtc_frame_size}"
                )
                return capture_audio

            # Calculate the number of blocks that need to be divided
            num_chunks = len(capture_audio) // self._webrtc_frame_size

            if num_chunks == 1:
                # 10ms frame, processed directly
                return self._process_single_aec_frame(capture_audio)
            else:
                # 20ms/40ms/60ms frame, segmentation processing
                return self._process_chunked_aec_frames(capture_audio, num_chunks)

        except Exception as e:
            logger.error(f"AEC processing failed: {e}")
            return capture_audio

    def _process_single_aec_frame(self, capture_audio: np.ndarray) -> np.ndarray:
        """Processing a single 10ms WebRTC frame (macOS only)"""
        if not self._is_macos:
            return capture_audio

        try:
            # Import ctypes only on macOS
            import ctypes

            # Get reference signal
            reference_audio = self._get_reference_frame(self._webrtc_frame_size)

            # Create ctypes buffer
            capture_buffer = (ctypes.c_short * self._webrtc_frame_size)(*capture_audio)
            reference_buffer = (ctypes.c_short * self._webrtc_frame_size)(
                *reference_audio
            )

            processed_capture = (ctypes.c_short * self._webrtc_frame_size)()
            processed_reference = (ctypes.c_short * self._webrtc_frame_size)()

            # First process the reference signal (render stream)
            render_result = self.apm.process_reverse_stream(
                reference_buffer,
                self.render_config,
                self.render_config,
                processed_reference,
            )

            if render_result != 0:
                logger.warning(f"Reference signal processing failed, error code: {render_result}")

            # Then process the acquisition signal (capture stream)
            capture_result = self.apm.process_stream(
                capture_buffer,
                self.capture_config,
                self.capture_config,
                processed_capture,
            )

            if capture_result != 0:
                logger.warning(f"Acquisition signal processing failed, error code: {capture_result}")
                return capture_audio

            # Convert back to numpy array
            return np.array(processed_capture, dtype=np.int16)

        except Exception as e:
            logger.error(f"AEC frame processing failed: {e}")
            return capture_audio

    def _process_chunked_aec_frames(
        self, capture_audio: np.ndarray, num_chunks: int
    ) -> np.ndarray:
        """Split processing of large frames (20ms/40ms/60ms, etc.)"""
        processed_chunks = []

        for i in range(num_chunks):
            # Extract the current 10ms block
            start_idx = i * self._webrtc_frame_size
            end_idx = (i + 1) * self._webrtc_frame_size
            chunk = capture_audio[start_idx:end_idx]

            # Process this 10ms block
            processed_chunk = self._process_single_aec_frame(chunk)
            processed_chunks.append(processed_chunk)

        # Reassemble all processed blocks
        return np.concatenate(processed_chunks)

    def _get_reference_frame(self, frame_size: int) -> np.ndarray:
        """Get the reference signal frame of the specified size."""
        # If there is no reference signal or insufficient buffer, return silence
        if len(self._reference_buffer) < frame_size:
            return np.zeros(frame_size, dtype=np.int16)

        # Extract a frame from buffer
        frame_data = []
        for _ in range(frame_size):
            frame_data.append(self._reference_buffer.popleft())

        return np.array(frame_data, dtype=np.int16)

    def is_reference_available(self) -> bool:
        """Check if the reference signal is available."""
        if self._is_windows or self._is_linux:
            # Windows and Linux use system-wide AEC, which is always available
            return self._is_initialized

        # macOS needs to check the reference signal flow
        return (
            self.reference_stream is not None
            and self.reference_stream.active
            and len(self._reference_buffer) >= self._webrtc_frame_size
        )

    def get_status(self) -> Dict[str, Any]:
        """Get AEC processor status."""
        status = {
            "initialized": self._is_initialized,
            "platform": self._platform,
            "reference_available": self.is_reference_available(),
        }

        if self._is_windows:
            status.update(
                {"aec_type": "system_level", "description": "Low-level echo cancellation in Windows systems"}
            )
        elif self._is_linux:
            status.update(
                {
                    "aec_type": "system_level",
                    "description": "Linux system-level echo cancellation (PulseAudio)",
                }
            )
        elif self._is_macos:
            status.update(
                {
                    "aec_type": "webrtc_blackhole",
                    "description": "WebRTC + BlackHole reference signal",
                    "reference_device_id": self.reference_device_id,
                    "reference_buffer_size": len(self._reference_buffer),
                    "webrtc_apm_active": self.apm is not None,
                }
            )
        else:
            status.update(
                {
                    "aec_type": "unsupported",
                    "description": f"Platform {self._platform} does not support AEC yet",
                }
            )

        return status

    async def close(self):
        """Turn off the AEC processor."""
        if self._is_closing:
            return

        self._is_closing = True
        logger.info("Starting to shut down AEC processor...")

        try:
            # Clean up WebRTC related resources only on macOS platform
            if self._is_macos:
                # Stop reference signal flow
                if self.reference_stream:
                    try:
                        self.reference_stream.stop()
                        self.reference_stream.close()
                    except Exception as e:
                        logger.warning(f"Failed to close reference signal stream: {e}")
                    finally:
                        self.reference_stream = None

                # Clean WebRTC APM
                if self.apm:
                    try:
                        if self.capture_config:
                            self.apm.destroy_stream_config(self.capture_config)
                        if self.render_config:
                            self.apm.destroy_stream_config(self.render_config)
                    except Exception as e:
                        logger.warning(f"Failed to clean APM configuration: {e}")
                    finally:
                        self.capture_config = None
                        self.render_config = None
                        self.apm = None

            # clear buffer
            self._reference_buffer.clear()

            self._is_initialized = False
            logger.info("AEC processor is turned off")

        except Exception as e:
            logger.error(f"An error occurred while shutting down the AEC processor: {e}")
