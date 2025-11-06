"""Unified application launcher.

Automatically select the corresponding launcher implementation based on the system"""

import asyncio
import platform
from typing import Any, Dict, Optional

from src.utils.logging_config import get_logger

from .utils import find_best_matching_app

logger = get_logger(__name__)


async def launch_application(args: Dict[str, Any]) -> bool:
    """Start the application.

    Args:
        args: Dictionary of arguments containing application names
            - app_name: application name

    Returns:
        bool: whether the startup was successful"""
    try:
        app_name = args["app_name"]
        logger.info(f"[AppLauncher] Trying to launch application: {app_name}")

        # First try to find an exact matching app by scanning
        matched_app = await _find_matching_application(app_name)
        if matched_app:
            logger.info(
                f"[AppLauncher] Find matching application: {matched_app.get('display_name', matched_app.get('name', ''))}"
            )
            # Use different launch methods based on application type
            success = await _launch_matched_app(matched_app, app_name)
        else:
            # If no match is found, use the original method
            logger.info(f"[AppLauncher] No exact match found, using original name: {app_name}")
            success = await _launch_by_name(app_name)

        if success:
            logger.info(f"[AppLauncher] Successfully launched application: {app_name}")
        else:
            logger.warning(f"[AppLauncher] Failed to launch application: {app_name}")

        return success

    except KeyError:
        logger.error("[AppLauncher] Missing app_name parameter")
        return False
    except Exception as e:
        logger.error(f"[AppLauncher] Failed to launch application: {e}", exc_info=True)
        return False


async def _find_matching_application(app_name: str) -> Optional[Dict[str, Any]]:
    """Scan to find matching apps.

    Args:
        app_name: The name of the application to look for

    Returns:
        Matching application information, returns None if not found"""
    try:
        # Use unified matching logic
        matched_app = await find_best_matching_app(app_name, "installed")

        if matched_app:
            logger.info(
                f"[AppLauncher] Find apps through unified matching: {matched_app.get('display_name', matched_app.get('name', ''))}"
            )

        return matched_app

    except Exception as e:
        logger.warning(f"[AppLauncher] Error finding matching application: {e}")
        return None


async def _launch_matched_app(matched_app: Dict[str, Any], original_name: str) -> bool:
    """Launch the matched application.

    Args:
        matched_app: matched application information
        original_name: original application name

    Returns:
        bool: whether the startup was successful"""
    try:
        app_type = matched_app.get("type", "unknown")
        app_path = matched_app.get("path", matched_app.get("name", original_name))

        system = platform.system()

        if system == "Windows":
            # Special handling for Windows systems
            if app_type == "uwp":
                # UWP apps use special launch method
                from .windows.launcher import launch_uwp_app_by_path

                return await asyncio.to_thread(launch_uwp_app_by_path, app_path)
            elif app_type == "shortcut" and app_path.endswith(".lnk"):
                # shortcut file
                from .windows.launcher import launch_shortcut

                return await asyncio.to_thread(launch_shortcut, app_path)

        # Regular application launch
        return await _launch_by_name(app_path)

    except Exception as e:
        logger.error(f"[AppLauncher] Failed to launch matching app: {e}")
        return False


async def _launch_by_name(app_name: str) -> bool:
    """Launch the application based on its name.

    Args:
        app_name: application name or path

    Returns:
        bool: whether the startup was successful"""
    try:
        system = platform.system()

        if system == "Windows":
            from .windows.launcher import launch_application

            return await asyncio.to_thread(launch_application, app_name)
        elif system == "Darwin":  # macOS
            from .mac.launcher import launch_application

            return await asyncio.to_thread(launch_application, app_name)
        elif system == "Linux":
            from .linux.launcher import launch_application

            return await asyncio.to_thread(launch_application, app_name)
        else:
            logger.error(f"[AppLauncher] Unsupported operating system: {system}")
            return False

    except Exception as e:
        logger.error(f"[AppLauncher] Failed to launch application: {e}")
        return False


def get_system_launcher():
    """Get the corresponding launcher module according to the current system.

    Returns:
        Launcher module corresponding to the system"""
    system = platform.system()

    if system == "Darwin":  # macOS
        from .mac import launcher

        return launcher
    elif system == "Windows":  # Windows
        from .windows import launcher

        return launcher
    elif system == "Linux":  # Linux
        from .linux import launcher

        return launcher
    else:
        logger.warning(f"[AppLauncher] Unsupported system: {system}")
        return None
