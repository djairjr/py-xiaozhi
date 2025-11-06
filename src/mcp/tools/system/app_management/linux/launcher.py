"""Linux system application launcher.

Provide application startup function under Linux platform"""

import os
import subprocess

from src.utils.logging_config import get_logger

logger = get_logger(__name__)


def launch_application(app_name: str) -> bool:
    """Launch the application on Linux.

    Args:
        app_name: application name

    Returns:
        bool: whether the startup was successful"""
    try:
        logger.info(f"[LinuxLauncher] Launch application: {app_name}")

        # Method 1: Use the application name directly
        try:
            subprocess.Popen([app_name])
            logger.info(f"[LinuxLauncher] Successfully started directly: {app_name}")
            return True
        except (OSError, subprocess.SubprocessError):
            logger.debug(f"[LinuxLauncher] Direct launch failed: {app_name}")

        # Method 2: Use which to find the application path
        try:
            result = subprocess.run(["which", app_name], capture_output=True, text=True)
            if result.returncode == 0:
                app_path = result.stdout.strip()
                subprocess.Popen([app_path])
                logger.info(f"[LinuxLauncher] Successfully launched via which: {app_name}")
                return True
        except (OSError, subprocess.SubprocessError):
            logger.debug(f"[LinuxLauncher] which failed to launch: {app_name}")

        # Method 3: Use xdg-open (for desktop environments)
        try:
            subprocess.Popen(["xdg-open", app_name])
            logger.info(f"[LinuxLauncher] Launched successfully using xdg-open: {app_name}")
            return True
        except (OSError, subprocess.SubprocessError):
            logger.debug(f"[LinuxLauncher] xdg-open failed to start: {app_name}")

        # Method 4: Try common application paths
        common_paths = [
            f"/usr/bin/{app_name}",
            f"/usr/local/bin/{app_name}",
            f"/opt/{app_name}/{app_name}",
            f"/snap/bin/{app_name}",
        ]

        for path in common_paths:
            if os.path.exists(path):
                subprocess.Popen([path])
                logger.info(
                    f"[LinuxLauncher] Launched successfully via common path: {app_name} ({path})"
                )
                return True

        # Method 5: Try to launch the .desktop file
        desktop_dirs = [
            "/usr/share/applications",
            "/usr/local/share/applications",
            os.path.expanduser("~/.local/share/applications"),
        ]

        for desktop_dir in desktop_dirs:
            desktop_file = os.path.join(desktop_dir, f"{app_name}.desktop")
            if os.path.exists(desktop_file):
                subprocess.Popen(["gtk-launch", f"{app_name}.desktop"])
                logger.info(f"[LinuxLauncher] Successfully launched through desktop file: {app_name}")
                return True

        logger.warning(f"[LinuxLauncher] All Linux launch methods failed: {app_name}")
        return False

    except Exception as e:
        logger.error(f"[LinuxLauncher] Linux startup failed: {e}")
        return False
