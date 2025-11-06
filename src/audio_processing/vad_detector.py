import logging
import threading
import time

import numpy as np
import pyaudio
import webrtcvad

from src.constants.constants import AbortReason, DeviceState

# Configuration log
logger = logging.getLogger("VADDetector")


class VADDetector:
    """WebRTC VAD based voice activity detector to detect user interruptions."""

    def __init__(self, audio_codec, protocol, app_instance, loop):
        """Initialize the VAD detector.

        Parameters:
            audio_codec: audio codec instance
            protocol: communication protocol instance
            app_instance: application instance
            loop: event loop"""
        self.audio_codec = audio_codec
        self.protocol = protocol
        self.app = app_instance
        self.loop = loop

        # VAD settings
        self.vad = webrtcvad.Vad()
        self.vad.set_mode(3)  # Set maximum sensitivity

        # Parameter settings
        self.sample_rate = 16000
        self.frame_duration = 20  # millisecond
        self.frame_size = int(self.sample_rate * self.frame_duration / 1000)
        self.speech_window = 5  # How many consecutive frames of speech are detected before interrupting is triggered?
        self.energy_threshold = 300  # energy threshold

        # state variables
        self.running = False
        self.paused = False
        self.thread = None
        self.speech_count = 0
        self.silence_count = 0
        self.triggered = False

        # Create separate PyAudio instances and streams to avoid conflicts with the main audio stream
        self.pa = None
        self.stream = None

    def start(self):
        """Start the VAD detector."""
        if self.thread and self.thread.is_alive():
            logger.warning("VAD detector is already running")
            return

        self.running = True
        self.paused = False

        # Initialize PyAudio and streams
        self._initialize_audio_stream()

        # Start detection thread
        self.thread = threading.Thread(target=self._detection_loop, daemon=True)
        self.thread.start()
        logger.info("VAD detector is started")

    def stop(self):
        """Stop the VAD detector."""
        self.running = False

        # Turn off audio stream
        self._close_audio_stream()

        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=1.0)

        logger.info("VAD detector has stopped")

    def pause(self):
        """Pause VAD detection."""
        self.paused = True
        logger.info("VAD detector has been paused")

    def resume(self):
        """Restore VAD detection."""
        self.paused = False
        # reset state
        self.speech_count = 0
        self.silence_count = 0
        self.triggered = False
        logger.info("VAD detector has been restored")

    def is_running(self):
        """Check if the VAD detector is running."""
        return self.running and not self.paused

    def _initialize_audio_stream(self):
        """Initialize a separate audio stream."""
        try:
            # Create a PyAudio instance
            self.pa = pyaudio.PyAudio()

            # Get the default input device
            device_index = None
            for i in range(self.pa.get_device_count()):
                device_info = self.pa.get_device_info_by_index(i)
                if device_info["maxInputChannels"] > 0:
                    device_index = i
                    break

            if device_index is None:
                logger.error("No available input device found")
                return False

            # Create input stream
            self.stream = self.pa.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=self.sample_rate,
                input=True,
                input_device_index=device_index,
                frames_per_buffer=self.frame_size,
                start=True,
            )

            logger.info(f"VAD detector audio stream initialized, using device index: {device_index}")
            return True

        except Exception as e:
            logger.error(f"Failed to initialize VAD audio stream: {e}")
            return False

    def _close_audio_stream(self):
        """Close the audio stream."""
        try:
            if self.stream:
                self.stream.stop_stream()
                self.stream.close()
                self.stream = None

            if self.pa:
                self.pa.terminate()
                self.pa = None

            logger.info("VAD detector audio stream is turned off")
        except Exception as e:
            logger.error(f"Failed to close VAD audio stream: {e}")

    def _detection_loop(self):
        """VAD detection main loop."""
        logger.info("VAD detection cycle started")

        while self.running:
            # Skip if paused or audio stream not initialized
            if self.paused or not self.stream:
                time.sleep(0.1)
                continue

            try:
                # Only detect when speaking
                if self.app.device_state == DeviceState.SPEAKING:
                    # Read audio frames
                    frame = self._read_audio_frame()
                    if not frame:
                        time.sleep(0.01)
                        continue

                    # Check if it is voice
                    is_speech = self._detect_speech(frame)

                    # If speech is detected and the trigger condition is met, handle the interruption
                    if is_speech:
                        self._handle_speech_frame(frame)
                    else:
                        self._handle_silence_frame(frame)
                else:
                    # Not in speaking state, reset state
                    self._reset_state()

            except Exception as e:
                logger.error(f"VAD detection loop error: {e}")

            time.sleep(0.01)  # Small latency, reduced CPU usage

        logger.info("VAD detection cycle has ended")

    def _read_audio_frame(self):
        """Read a frame of audio data."""
        try:
            if not self.stream or not self.stream.is_active():
                return None

            # Read audio data
            data = self.stream.read(self.frame_size, exception_on_overflow=False)
            return data
        except Exception as e:
            logger.error(f"Failed to read audio frame: {e}")
            return None

    def _detect_speech(self, frame):
        """Check whether it is speech."""
        try:
            # Make sure the frame length is correct
            if len(frame) != self.frame_size * 2:  # 16-bit audio, 2 bytes per sample
                return False

            # Use VAD detection
            is_speech = self.vad.is_speech(frame, self.sample_rate)

            # Calculate audio energy
            audio_data = np.frombuffer(frame, dtype=np.int16)
            energy = np.mean(np.abs(audio_data))

            # Combined VAD and energy threshold
            is_valid_speech = is_speech and energy > self.energy_threshold

            if is_valid_speech:
                logger.debug(
                    f"Speech detected [energy: {energy:.2f}] [continuous speech frames: {self.speech_count+1}]"
                )

            return is_valid_speech
        except Exception as e:
            logger.error(f"Failed to detect voice: {e}")
            return False

    def _handle_speech_frame(self, frame):
        """Process speech frames."""
        self.speech_count += 1
        self.silence_count = 0

        # Enough continuous speech frames are detected to trigger an interrupt
        if self.speech_count >= self.speech_window and not self.triggered:
            self.triggered = True
            logger.info("Continuous speech is detected and interrupt is triggered!")
            self._trigger_interrupt()

            # Pause yourself immediately to prevent repeated triggering
            self.paused = True
            logger.info("The VAD detector has been automatically paused to prevent repeated triggering")

            # reset state
            self.speech_count = 0
            self.silence_count = 0
            self.triggered = False

    def _handle_silence_frame(self, frame):
        """Handle silent frames."""
        self.silence_count += 1
        self.speech_count = 0

    def _reset_state(self):
        """Reset status."""
        self.speech_count = 0
        self.silence_count = 0
        self.triggered = False

    def _trigger_interrupt(self):
        """Trigger interrupt."""
        # Notify the application to terminate the current speech output
        self.app.schedule(
            lambda: self.app.abort_speaking(AbortReason.WAKE_WORD_DETECTED)
        )
