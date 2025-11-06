"""The general tool function collection module includes text-to-speech, browser operation, clipboard and other general tool functions."""

import queue
import shutil
import threading
import time
import webbrowser
from typing import Optional

from src.utils.logging_config import get_logger

logger = get_logger(__name__)

# Global audio playback queue and lock
_audio_queue = queue.Queue()
_audio_lock = threading.Lock()
_audio_worker_thread = None
_audio_worker_running = False
_audio_device_warmed_up = False


def _warm_up_audio_device():
    """Preheat audio equipment to prevent first words from being swallowed."""
    global _audio_device_warmed_up
    if _audio_device_warmed_up:
        return

    try:
        import platform
        import subprocess

        system = platform.system()

        if system == "Darwin":
            subprocess.run(
                ["say", "-v", "Ting-Ting", "buzz"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        elif system == "Linux" and shutil.which("espeak"):
            subprocess.run(
                ["espeak", "-v", "zh", "buzz"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        elif system == "Windows":
            import win32com.client

            speaker = win32com.client.Dispatch("SAPI.SpVoice")
            speaker.Speak("buzz")

        _audio_device_warmed_up = True
        logger.info("Audio device warmed up")
    except Exception as e:
        logger.warning(f"Failed to warm up audio device: {e}")


def _audio_queue_worker():
    """Audio queue worker thread that ensures audio plays in order and is not truncated."""

    while _audio_worker_running:
        try:
            text = _audio_queue.get(timeout=1)
            if text is None:
                break

            with _audio_lock:
                logger.info(f"Start playing audio: {text[:50]}...")
                success = _play_system_tts(text)

                if not success:
                    logger.warning("System TTS failed, try alternative solution")
                    import os

                    if os.name == "nt":
                        _play_windows_tts(text, set_chinese_voice=False)
                    else:
                        _play_system_tts(text)

                time.sleep(0.5)  # Pause after playback to prevent the tail sound from being swallowed

            _audio_queue.task_done()

        except queue.Empty:
            continue
        except Exception as e:
            logger.error(f"Audio queue worker thread error: {e}")

    logger.info("Audio queue worker thread stopped")


def _ensure_audio_worker():
    """Make sure the audio worker thread is running."""
    global _audio_worker_thread, _audio_worker_running

    if _audio_worker_thread is None or not _audio_worker_thread.is_alive():
        _warm_up_audio_device()
        _audio_worker_running = True
        _audio_worker_thread = threading.Thread(target=_audio_queue_worker, daemon=True)
        _audio_worker_thread.start()
        logger.info("Audio queue worker thread started")


def open_url(url: str) -> bool:
    try:
        success = webbrowser.open(url)
        if success:
            logger.info(f"Web page successfully opened: {url}")
        else:
            logger.warning(f"Unable to open webpage: {url}")
        return success
    except Exception as e:
        logger.error(f"Error opening web page: {e}")
        return False


def copy_to_clipboard(text: str) -> bool:
    try:
        import pyperclip

        pyperclip.copy(text)
        logger.info(f'文本 "{text}" 已复制到剪贴板')
        return True
    except ImportError:
        logger.warning("pyperclip module not installed, cannot copy to clipboard")
        return False
    except Exception as e:
        logger.error(f"Error copying to clipboard: {e}")
        return False


def _play_windows_tts(text: str, set_chinese_voice: bool = True) -> bool:
    try:
        import win32com.client

        speaker = win32com.client.Dispatch("SAPI.SpVoice")

        if set_chinese_voice:
            try:
                voices = speaker.GetVoices()
                for i in range(voices.Count):
                    if "Chinese" in voices.Item(i).GetDescription():
                        speaker.Voice = voices.Item(i)
                        break
            except Exception as e:
                logger.warning(f"Error setting Chinese tone: {e}")

        try:
            speaker.Rate = -2
        except Exception:
            pass

        enhanced_text = text + "。 。 。"
        speaker.Speak(enhanced_text)
        logger.info("Text played using Windows speech synthesis")
        time.sleep(0.5)
        return True
    except ImportError:
        logger.warning("Windows TTS not available, skipping audio playback")
        return False
    except Exception as e:
        logger.error(f"Windows TTS playback error: {e}")
        return False


def _play_linux_tts(text: str) -> bool:
    import subprocess

    if shutil.which("espeak"):
        try:
            enhanced_text = text + "。 。 。"
            result = subprocess.run(
                ["espeak", "-v", "zh", "-s", "150", "-g", "10", enhanced_text],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=30,
            )
            time.sleep(0.5)
            return result.returncode == 0
        except subprocess.TimeoutExpired:
            logger.warning("espeak playback timeout")
            return False
        except Exception as e:
            logger.error(f"espeak playback error: {e}")
            return False
    else:
        logger.warning("espeak is not available, skip audio playback")
        return False


def _play_macos_tts(text: str) -> bool:
    import subprocess

    if shutil.which("say"):
        try:
            enhanced_text = text + "。 。 。"
            result = subprocess.run(
                ["say", "-r", "180", enhanced_text],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=30,
            )
            time.sleep(0.5)
            return result.returncode == 0
        except subprocess.TimeoutExpired:
            logger.warning("say command playback timeout")
            return False
        except Exception as e:
            logger.error(f"Say command playback error: {e}")
            return False
    else:
        logger.warning("The say command is not available and audio playback is skipped.")
        return False


def _play_system_tts(text: str) -> bool:
    import os
    import platform

    if os.name == "nt":
        return _play_windows_tts(text)
    else:
        system = platform.system()
        if system == "Linux":
            return _play_linux_tts(text)
        elif system == "Darwin":
            return _play_macos_tts(text)
        else:
            logger.warning(f"Unsupported system {system}, skip audio playback")
            return False


def play_audio_nonblocking(text: str) -> None:
    try:
        _ensure_audio_worker()
        _audio_queue.put(text)
        logger.info(f"Audio task added to queue: {text[:50]}...")
    except Exception as e:
        logger.error(f"Error adding audio task to queue: {e}")

        def audio_worker():
            try:
                _warm_up_audio_device()
                _play_system_tts(text)
            except Exception as e:
                logger.error(f"Error playing backup audio: {e}")

        threading.Thread(target=audio_worker, daemon=True).start()


def extract_verification_code(text: str) -> Optional[str]:
    try:
        import re

        # Activate related keyword list
        activation_keywords = [
            "Log in",
            "control Panel",
            "activation",
            "Verification code",
            "Bind device",
            "Add device",
            "enter confirmation code",
            "enter",
            "panel",
            "xiaozhi.me",
            "activation code",
        ]

        # Check if the text contains activation related keywords
        has_activation_keyword = any(keyword in text for keyword in activation_keywords)

        if not has_activation_keyword:
            logger.debug(f"The text does not contain activation keywords, skip verification code extraction: {text}")
            return None

        # More precise verification code matching pattern
        # Matches a 6-digit verification code, possibly separated by spaces
        patterns = [
            r"Verification code[::]\s*(\d{6})",  # Verification code: 123456
            r"Enter verification code [::]\s*(\d{6})",  # Enter verification code: 123456
            r"Enter \s*(\d{6})",  # Enter 123456
            r"Verification code\s*(\d{6})",  # Verification code 123456
            r"Activation code[::]\s*(\d{6})",  # Activation code: 123456
            r"(\d{6})[，,。.]",  # 123456, or 123456.
            r"[，,。.]\s*(\d{6})",  # ，123456
        ]

        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                code = match.group(1)
                logger.info(f"Verification code extracted from text: {code}")
                return code

        # If there is an activation keyword but no exact pattern is matched, try the original pattern
        # but requires specific context around the number
        match = re.search(r"((?:\d\s*){6,})", text)
        if match:
            code = "".join(match.group(1).split())
            # The verification code should be 6 digits
            if len(code) == 6 and code.isdigit():
                logger.info(f"Verification code extracted from text (generic mode): {code}")
                return code

        logger.warning(f"Unable to find verification code from text: {text}")
        return None
    except Exception as e:
        logger.error(f"Error while retrieving verification code: {e}")
        return None


def handle_verification_code(text: str) -> None:
    code = extract_verification_code(text)
    if not code:
        return

    copy_to_clipboard(code)
