"""macOS system application launcher.

Provide application startup function under macOS platform"""

import os
import subprocess

from src.utils.logging_config import get_logger

logger = get_logger(__name__)


def launch_application(app_name: str) -> bool:
    """Launch the application on macOS.

    Args:
        app_name: application name

    Returns:
        bool: whether the startup was successful"""
    try:
        logger.info(f"[MacLauncher] Launch application: {app_name}")

        # Method 1: Use the open -a command
        try:
            subprocess.Popen(["open", "-a", app_name])
            logger.info(f"[MacLauncher] Successfully launched using open -a: {app_name}")
            return True
        except (OSError, subprocess.SubprocessError):
            logger.debug(f"[MacLauncher] open -a failed to launch: {app_name}")

        # Method 2: Use the application name directly
        try:
            subprocess.Popen([app_name])
            logger.info(f"[MacLauncher] Successfully launched directly: {app_name}")
            return True
        except (OSError, subprocess.SubprocessError):
            logger.debug(f"[MacLauncher] Direct launch failed: {app_name}")

        # Method 3: Try the Applications directory
        app_path = f"/Applications/{app_name}.app"
        if os.path.exists(app_path):
            subprocess.Popen(["open", app_path])
            logger.info(f"[MacLauncher] Successfully launched through the Applications directory: {app_name}")
            return True

        # Method 4: Start using osascript
        script = f'tell application "{app_name}" to activate'
        subprocess.Popen(["osascript", "-e", script])
        logger.info(f"[MacLauncher] Launched successfully using osascript: {app_name}")
        return True

    except Exception as e:
        logger.error(f"[MacLauncher] macOS launch failed: {e}")
        return False
