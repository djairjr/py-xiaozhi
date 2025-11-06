"""WebRTC Echo Cancellation (AEC) demo script.

This script is used to demonstrate the echo cancellation feature of the WebRTC APM library:
1. Play the specified audio file (as a reference signal)
2. Simultaneously record microphone input (including echo and ambient sounds)
3. Apply WebRTC echo cancellation processing
4. Save the original recording and the processed recording for comparison

Usage:
    python webrtc_aec_demo.py [audio file path]

Example:
    python webrtc_aec_demo.py Ju Jingyi.wav"""

import ctypes
import os
import sys
import threading
import time
import wave
from ctypes import POINTER, Structure, byref, c_bool, c_float, c_int, c_short, c_void_p

import numpy as np
import pyaudio
import pygame
import soundfile as sf
from pygame import mixer

# Get the absolute path of the DLL file
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
dll_path = os.path.join(
    project_root, "libs", "webrtc_apm", "win", "x86_64", "libwebrtc_apm.dll"
)

# Load DLL
try:
    apm_lib = ctypes.CDLL(dll_path)
    print(f"Successfully loaded WebRTC APM library: {dll_path}")
except Exception as e:
    print(f"Failed to load WebRTC APM library: {e}")
    sys.exit(1)


# Define structure and enumeration types
class DownmixMethod(ctypes.c_int):
    AverageChannels = 0
    UseFirstChannel = 1


class NoiseSuppressionLevel(ctypes.c_int):
    Low = 0
    Moderate = 1
    High = 2
    VeryHigh = 3


class GainControllerMode(ctypes.c_int):
    AdaptiveAnalog = 0
    AdaptiveDigital = 1
    FixedDigital = 2


class ClippingPredictorMode(ctypes.c_int):
    ClippingEventPrediction = 0
    AdaptiveStepClippingPeakPrediction = 1
    FixedStepClippingPeakPrediction = 2


# Define Pipeline structure
class Pipeline(Structure):
    _fields_ = [
        ("MaximumInternalProcessingRate", c_int),
        ("MultiChannelRender", c_bool),
        ("MultiChannelCapture", c_bool),
        ("CaptureDownmixMethod", c_int),
    ]


# Define PreAmplifier structure
class PreAmplifier(Structure):
    _fields_ = [("Enabled", c_bool), ("FixedGainFactor", c_float)]


# Define the AnalogMicGainEmulation structure
class AnalogMicGainEmulation(Structure):
    _fields_ = [("Enabled", c_bool), ("InitialLevel", c_int)]


# Define the CaptureLevelAdjustment structure
class CaptureLevelAdjustment(Structure):
    _fields_ = [
        ("Enabled", c_bool),
        ("PreGainFactor", c_float),
        ("PostGainFactor", c_float),
        ("MicGainEmulation", AnalogMicGainEmulation),
    ]


# Define the HighPassFilter structure
class HighPassFilter(Structure):
    _fields_ = [("Enabled", c_bool), ("ApplyInFullBand", c_bool)]


# Define the EchoCanceler structure
class EchoCanceller(Structure):
    _fields_ = [
        ("Enabled", c_bool),
        ("MobileMode", c_bool),
        ("ExportLinearAecOutput", c_bool),
        ("EnforceHighPassFiltering", c_bool),
    ]


# Define NoiseSuppression structure
class NoiseSuppression(Structure):
    _fields_ = [
        ("Enabled", c_bool),
        ("NoiseLevel", c_int),
        ("AnalyzeLinearAecOutputWhenAvailable", c_bool),
    ]


# Define TransientSuppression structure
class TransientSuppression(Structure):
    _fields_ = [("Enabled", c_bool)]


# Define ClippingPredictor structure
class ClippingPredictor(Structure):
    _fields_ = [
        ("Enabled", c_bool),
        ("PredictorMode", c_int),
        ("WindowLength", c_int),
        ("ReferenceWindowLength", c_int),
        ("ReferenceWindowDelay", c_int),
        ("ClippingThreshold", c_float),
        ("CrestFactorMargin", c_float),
        ("UsePredictedStep", c_bool),
    ]


# Define AnalogGainController structure
class AnalogGainController(Structure):
    _fields_ = [
        ("Enabled", c_bool),
        ("StartupMinVolume", c_int),
        ("ClippedLevelMin", c_int),
        ("EnableDigitalAdaptive", c_bool),
        ("ClippedLevelStep", c_int),
        ("ClippedRatioThreshold", c_float),
        ("ClippedWaitFrames", c_int),
        ("Predictor", ClippingPredictor),
    ]


# Define GainController1 structure
class GainController1(Structure):
    _fields_ = [
        ("Enabled", c_bool),
        ("ControllerMode", c_int),
        ("TargetLevelDbfs", c_int),
        ("CompressionGainDb", c_int),
        ("EnableLimiter", c_bool),
        ("AnalogController", AnalogGainController),
    ]


# Define the InputVolumeController structure
class InputVolumeController(Structure):
    _fields_ = [("Enabled", c_bool)]


# Define AdaptiveDigital structure
class AdaptiveDigital(Structure):
    _fields_ = [
        ("Enabled", c_bool),
        ("HeadroomDb", c_float),
        ("MaxGainDb", c_float),
        ("InitialGainDb", c_float),
        ("MaxGainChangeDbPerSecond", c_float),
        ("MaxOutputNoiseLevelDbfs", c_float),
    ]


# Define FixedDigital structure
class FixedDigital(Structure):
    _fields_ = [("GainDb", c_float)]


# Define GainController2 structure
class GainController2(Structure):
    _fields_ = [
        ("Enabled", c_bool),
        ("VolumeController", InputVolumeController),
        ("AdaptiveController", AdaptiveDigital),
        ("FixedController", FixedDigital),
    ]


# Define the complete Config structure
class Config(Structure):
    _fields_ = [
        ("PipelineConfig", Pipeline),
        ("PreAmp", PreAmplifier),
        ("LevelAdjustment", CaptureLevelAdjustment),
        ("HighPass", HighPassFilter),
        ("Echo", EchoCanceller),
        ("NoiseSuppress", NoiseSuppression),
        ("TransientSuppress", TransientSuppression),
        ("GainControl1", GainController1),
        ("GainControl2", GainController2),
    ]


# Define DLL function prototype
apm_lib.WebRTC_APM_Create.restype = c_void_p
apm_lib.WebRTC_APM_Create.argtypes = []

apm_lib.WebRTC_APM_Destroy.restype = None
apm_lib.WebRTC_APM_Destroy.argtypes = [c_void_p]

apm_lib.WebRTC_APM_CreateStreamConfig.restype = c_void_p
apm_lib.WebRTC_APM_CreateStreamConfig.argtypes = [c_int, c_int]

apm_lib.WebRTC_APM_DestroyStreamConfig.restype = None
apm_lib.WebRTC_APM_DestroyStreamConfig.argtypes = [c_void_p]

apm_lib.WebRTC_APM_ApplyConfig.restype = c_int
apm_lib.WebRTC_APM_ApplyConfig.argtypes = [c_void_p, POINTER(Config)]

apm_lib.WebRTC_APM_ProcessReverseStream.restype = c_int
apm_lib.WebRTC_APM_ProcessReverseStream.argtypes = [
    c_void_p,
    POINTER(c_short),
    c_void_p,
    c_void_p,
    POINTER(c_short),
]

apm_lib.WebRTC_APM_ProcessStream.restype = c_int
apm_lib.WebRTC_APM_ProcessStream.argtypes = [
    c_void_p,
    POINTER(c_short),
    c_void_p,
    c_void_p,
    POINTER(c_short),
]

apm_lib.WebRTC_APM_SetStreamDelayMs.restype = None
apm_lib.WebRTC_APM_SetStreamDelayMs.argtypes = [c_void_p, c_int]


def create_apm_config():
    """Create WebRTC APM configuration - optimized to preserve natural speech and reduce error code-11 issues"""
    config = Config()

    # Set Pipeline Configuration - Use standard sample rate to avoid resampling issues
    config.PipelineConfig.MaximumInternalProcessingRate = 16000  # WebRTC optimization frequency
    config.PipelineConfig.MultiChannelRender = False
    config.PipelineConfig.MultiChannelCapture = False
    config.PipelineConfig.CaptureDownmixMethod = DownmixMethod.AverageChannels

    # Set PreAmplifier configuration - reduce pre-amp interference
    config.PreAmp.Enabled = False  # Turn off pre-amplification to avoid distortion
    config.PreAmp.FixedGainFactor = 1.0  # No gain

    # Set LevelAdjustment Configuration - Simplified Level Adjustment
    config.LevelAdjustment.Enabled = False  # Disable level adjustment to reduce processing conflicts
    config.LevelAdjustment.PreGainFactor = 1.0
    config.LevelAdjustment.PostGainFactor = 1.0
    config.LevelAdjustment.MicGainEmulation.Enabled = False
    config.LevelAdjustment.MicGainEmulation.InitialLevel = 100  # Lower initial level to avoid oversaturation

    # Set HighPassFilter configuration - use standard high-pass filtering
    config.HighPass.Enabled = True  # Enable high-pass filter to remove low-frequency noise
    config.HighPass.ApplyInFullBand = True  # Application in the whole frequency band, better compatibility

    # Setting up EchoCanceler configuration - Optimizing echo cancellation
    config.Echo.Enabled = True  # Enable echo cancellation
    config.Echo.MobileMode = False  # Use standard mode instead of mobile mode for better results
    config.Echo.ExportLinearAecOutput = False
    config.Echo.EnforceHighPassFiltering = True  # Enable forced high-pass filtering to help eliminate low-frequency echo

    # Set NoiseSuppression configuration - medium intensity noise suppression
    config.NoiseSuppress.Enabled = True
    config.NoiseSuppress.NoiseLevel = NoiseSuppressionLevel.Moderate  # medium level suppression
    config.NoiseSuppress.AnalyzeLinearAecOutputWhenAvailable = True

    # Set TransientSuppression configuration
    config.TransientSuppress.Enabled = False  # Turn off transient suppression to avoid cutting speech

    # Set GainController1 configuration - light gain control
    config.GainControl1.Enabled = True  # Enable gain control
    config.GainControl1.ControllerMode = GainControllerMode.AdaptiveDigital
    config.GainControl1.TargetLevelDbfs = 3  # Lower target level (more aggressive control)
    config.GainControl1.CompressionGainDb = 9  # Moderate compression gain
    config.GainControl1.EnableLimiter = True  # Enable limiter

    # AnalogGainController
    config.GainControl1.AnalogController.Enabled = False  # Turn off analog gain control
    config.GainControl1.AnalogController.StartupMinVolume = 0
    config.GainControl1.AnalogController.ClippedLevelMin = 70
    config.GainControl1.AnalogController.EnableDigitalAdaptive = False
    config.GainControl1.AnalogController.ClippedLevelStep = 15
    config.GainControl1.AnalogController.ClippedRatioThreshold = 0.1
    config.GainControl1.AnalogController.ClippedWaitFrames = 300

    # ClippingPredictor
    predictor = config.GainControl1.AnalogController.Predictor
    predictor.Enabled = False
    predictor.PredictorMode = ClippingPredictorMode.ClippingEventPrediction
    predictor.WindowLength = 5
    predictor.ReferenceWindowLength = 5
    predictor.ReferenceWindowDelay = 5
    predictor.ClippingThreshold = -1.0
    predictor.CrestFactorMargin = 3.0
    predictor.UsePredictedStep = True

    # Set GainController2 configuration - disabled to avoid conflicts
    config.GainControl2.Enabled = False
    config.GainControl2.VolumeController.Enabled = False
    config.GainControl2.AdaptiveController.Enabled = False
    config.GainControl2.AdaptiveController.HeadroomDb = 5.0
    config.GainControl2.AdaptiveController.MaxGainDb = 30.0
    config.GainControl2.AdaptiveController.InitialGainDb = 15.0
    config.GainControl2.AdaptiveController.MaxGainChangeDbPerSecond = 6.0
    config.GainControl2.AdaptiveController.MaxOutputNoiseLevelDbfs = -50.0
    config.GainControl2.FixedController.GainDb = 0.0

    return config


# Reference audio buffer (used to store speaker output)
reference_buffer = []
reference_lock = threading.Lock()


def record_playback_audio(chunk_size, sample_rate, channels):
    """Record audio output from speakers (more accurate reference signal)"""
    global reference_buffer

    # Note: This is an ideal implementation, but PyAudio under Windows usually cannot record speaker output directly.
    # In actual applications, other methods need to be used to capture system audio output
    try:
        p = pyaudio.PyAudio()

        # Try creating a stream recorded from the default output device (supported on some systems)
        # NOTE: This will not work on most systems, here is just an example
        loopback_stream = p.open(
            format=pyaudio.paInt16,
            channels=channels,
            rate=sample_rate,
            input=True,
            frames_per_buffer=chunk_size,
            input_device_index=None,  # Try using the default output device as the input source
        )

        # Start recording
        while True:
            try:
                data = loopback_stream.read(chunk_size, exception_on_overflow=False)
                with reference_lock:
                    reference_buffer.append(data)
            except OSError:
                break

            # Keep buffer sizes reasonable
            with reference_lock:
                if len(reference_buffer) > 100:  # Keep buffering for about 2 seconds
                    reference_buffer = reference_buffer[-100:]
    except Exception as e:
        print(f"Unable to record system audio: {e}")
    finally:
        try:
            if "loopback_stream" in locals() and loopback_stream:
                loopback_stream.stop_stream()
                loopback_stream.close()
            if "p" in locals() and p:
                p.terminate()
        except Exception:
            pass


def aec_demo(audio_file):
    """WebRTC echo cancellation demo main function."""
    # Check if the audio file exists
    if not os.path.exists(audio_file):
        print(f"Error: Audio file {audio_file} not found")
        return

    # Audio Parameter Settings - Optimized audio parameters using WebRTC
    SAMPLE_RATE = 16000  # Sampling rate 16kHz (WebRTC AEC optimized sampling rate)
    CHANNELS = 1  # mono
    CHUNK = 160  # Number of samples per frame (10ms @ 16kHz, standard frame size for WebRTC)
    FORMAT = pyaudio.paInt16  # 16-bit PCM format

    # Initialize PyAudio
    p = pyaudio.PyAudio()

    # Lists all available audio device information for reference
    print("\nAvailable audio devices:")
    for i in range(p.get_device_count()):
        dev_info = p.get_device_info_by_index(i)
        print(f"Device {i}: {dev_info['name']}")
        print(f"- Input channels: {dev_info['maxInputChannels']}")
        print(f"- Output channels: {dev_info['maxOutputChannels']}")
        print(f"- Default sample rate: {dev_info['defaultSampleRate']}")
    print("")

    # Open microphone input stream
    input_stream = p.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=SAMPLE_RATE,
        input=True,
        frames_per_buffer=CHUNK,
    )

    # Initialize pygame for playing audio
    pygame.init()
    mixer.init(frequency=SAMPLE_RATE, size=-16, channels=CHANNELS, buffer=CHUNK * 4)

    # Load reference audio file
    print(f"Load audio file: {audio_file}")

    # Read reference audio file and convert sample rate/number of channels
    # Note: The soundfile library is used here to load audio files to support multiple formats and resample
    try:
        print("Loading reference audio...")
        # Read raw audio using soundfile library
        ref_audio_data, orig_sr = sf.read(audio_file, dtype="int16")
        print(
            f"Original audio: sample rate={orig_sr}, number of channels="
            f"{ref_audio_data.shape[1] if len(ref_audio_data.shape) > 1 else 1}"
        )

        # Convert to mono (if stereo)
        if len(ref_audio_data.shape) > 1 and ref_audio_data.shape[1] > 1:
            ref_audio_data = ref_audio_data.mean(axis=1).astype(np.int16)

        # Convert sample rate (if needed)
        if orig_sr != SAMPLE_RATE:
            print(f"Resample reference audio from {orig_sr}Hz to {SAMPLE_RATE}Hz...")
            # Resampling using librosa or scipy
            from scipy import signal

            ref_audio_data = signal.resample(
                ref_audio_data, int(len(ref_audio_data) * SAMPLE_RATE / orig_sr)
            ).astype(np.int16)

        # Save as temporary wav file for pygame to play
        temp_wav_path = os.path.join(current_dir, "temp_reference.wav")
        with wave.open(temp_wav_path, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)  # 2 bytes (16 bits)
            wf.setframerate(SAMPLE_RATE)
            wf.writeframes(ref_audio_data.tobytes())

        # Split reference audio into CHUNK-sized frames
        ref_audio_frames = []
        for i in range(0, len(ref_audio_data), CHUNK):
            if i + CHUNK <= len(ref_audio_data):
                ref_audio_frames.append(ref_audio_data[i : i + CHUNK])
            else:
                # The last frame is less than the CHUNK size, padding with zeros
                last_frame = np.zeros(CHUNK, dtype=np.int16)
                last_frame[: len(ref_audio_data) - i] = ref_audio_data[i:]
                ref_audio_frames.append(last_frame)

        print(f"The reference audio preparation is completed, with a total of {len(ref_audio_frames)} frames")

        # Load the processed temporary WAV file
        mixer.music.load(temp_wav_path)
    except Exception as e:
        print(f"Error loading reference audio: {e}")
        sys.exit(1)

    # Create a WebRTC APM instance
    apm = apm_lib.WebRTC_APM_Create()

    # Apply APM configuration
    config = create_apm_config()
    result = apm_lib.WebRTC_APM_ApplyConfig(apm, byref(config))
    if result != 0:
        print(f"Warning: APM configuration application failed, error code: {result}")

    # Create flow configuration
    stream_config = apm_lib.WebRTC_APM_CreateStreamConfig(SAMPLE_RATE, CHANNELS)

    # Set a smaller delay time to more accurately match the reference signal and microphone signal
    apm_lib.WebRTC_APM_SetStreamDelayMs(apm, 50)

    # Create recording buffer
    original_frames = []
    processed_frames = []
    reference_frames = []

    # Wait for a while for the audio system to be ready
    time.sleep(0.5)

    print("Start recording and processing...")
    print("Play reference audio...")

    mixer.music.play()

    # Recording duration (based on audio file length)
    try:
        sound_length = mixer.Sound(temp_wav_path).get_length()
        recording_time = sound_length if sound_length > 0 else 10
    except Exception:
        recording_time = 10  # If the length cannot be obtained, the default is 10 seconds.

    recording_time += 1  # Extra 1 second to ensure all audio is captured

    start_time = time.time()
    current_ref_frame_index = 0
    try:
        while time.time() - start_time < recording_time:
            # Read a frame of data from the microphone
            input_data = input_stream.read(CHUNK, exception_on_overflow=False)

            # Save original recording
            original_frames.append(input_data)

            # Convert input data to short array
            input_array = np.frombuffer(input_data, dtype=np.int16)
            input_ptr = input_array.ctypes.data_as(POINTER(c_short))

            # Get the current reference audio frame
            if current_ref_frame_index < len(ref_audio_frames):
                ref_array = ref_audio_frames[current_ref_frame_index]
                reference_frames.append(ref_array.tobytes())
                current_ref_frame_index += 1
            else:
                # If the reference audio has finished playing, use a silent frame
                ref_array = np.zeros(CHUNK, dtype=np.int16)
                reference_frames.append(ref_array.tobytes())

            ref_ptr = ref_array.ctypes.data_as(POINTER(c_short))

            # Create output buffer
            output_array = np.zeros(CHUNK, dtype=np.int16)
            output_ptr = output_array.ctypes.data_as(POINTER(c_short))

            # Important: Process the reference signal (speaker output) first
            # Creates an output buffer for the reference signal (required although not used)
            ref_output_array = np.zeros(CHUNK, dtype=np.int16)
            ref_output_ptr = ref_output_array.ctypes.data_as(POINTER(c_short))

            result_reverse = apm_lib.WebRTC_APM_ProcessReverseStream(
                apm, ref_ptr, stream_config, stream_config, ref_output_ptr
            )

            if result_reverse != 0:
                print(f"\rWarning: Reference signal processing failed, error code: {result_reverse}")

            # The microphone signal is then processed, applying echo cancellation
            result = apm_lib.WebRTC_APM_ProcessStream(
                apm, input_ptr, stream_config, stream_config, output_ptr
            )

            if result != 0:
                print(f"\rWarning: Processing failed, error code: {result}")

            # Save processed audio frames
            processed_frames.append(output_array.tobytes())

            # Calculate and display progress
            progress = (time.time() - start_time) / recording_time * 100
            sys.stdout.write(f"\rProcessing progress: {progress:.1f}%")
            sys.stdout.flush()

    except KeyboardInterrupt:
        print("\nRecording interrupted by user")
    finally:
        print("\nRecording and processing completed")

        # Stop playing
        mixer.music.stop()

        # Turn off audio stream
        input_stream.stop_stream()
        input_stream.close()

        # Release APM resources
        apm_lib.WebRTC_APM_DestroyStreamConfig(stream_config)
        apm_lib.WebRTC_APM_Destroy(apm)

        # Close PyAudio
        p.terminate()

        # Save original recording
        original_output_path = os.path.join(current_dir, "original_recording.wav")
        save_wav(original_output_path, original_frames, SAMPLE_RATE, CHANNELS)

        # Save the processed recording
        processed_output_path = os.path.join(current_dir, "processed_recording.wav")
        save_wav(processed_output_path, processed_frames, SAMPLE_RATE, CHANNELS)

        # Save reference audio (played audio)
        reference_output_path = os.path.join(current_dir, "reference_playback.wav")
        save_wav(reference_output_path, reference_frames, SAMPLE_RATE, CHANNELS)

        # Delete temporary files
        if os.path.exists(temp_wav_path):
            try:
                os.remove(temp_wav_path)
            except Exception:
                pass

        print(f"The original recording has been saved to: {original_output_path}")
        print(f"The processed recording has been saved to: {processed_output_path}")
        print(f"Reference audio has been saved to: {reference_output_path}")

        # Exit pygame
        pygame.quit()


def save_wav(file_path, frames, sample_rate, channels):
    """Save audio frames as WAV files."""
    with wave.open(file_path, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(2)  # 2 bytes (16 bits)
        wf.setframerate(sample_rate)
        if isinstance(frames[0], bytes):
            wf.writeframes(b"".join(frames))
        else:
            wf.writeframes(b"".join([f for f in frames if isinstance(f, bytes)]))


if __name__ == "__main__":
    # Get command line parameters
    if len(sys.argv) > 1:
        audio_file = sys.argv[1]
    else:
        # By default, Ju Jingyi.wav in the scripts directory is used.
        audio_file = os.path.join(current_dir, "Ju Jingyi.wav")

        # If the default file does not exist, try the MP3 version
        if not os.path.exists(audio_file):
            audio_file = os.path.join(current_dir, "Ju Jingyi.mp3")
            if not os.path.exists(audio_file):
                print("Error: Default audio file not found, please specify the path to the audio file to play")
                print("Usage: python webrtc_aec_demo.py [audio file path]")
                sys.exit(1)

    # Run the demo
    aec_demo(audio_file)
