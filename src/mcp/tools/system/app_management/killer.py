"""Unified application closer.

Automatically select the corresponding closer implementation based on the system"""

import asyncio
import json
import platform
from typing import Any, Dict, List

from src.utils.logging_config import get_logger

from .utils import AppMatcher

logger = get_logger(__name__)


async def kill_application(args: Dict[str, Any]) -> bool:
    """Close the application.

    Args:
        args: Dictionary of arguments containing application names
            - app_name: application name
            - force: whether to force shutdown (optional, default False)

    Returns:
        bool: whether the shutdown was successful"""
    try:
        app_name = args["app_name"]
        force = args.get("force", False)
        logger.info(f"[AppKiller] Try to close application: {app_name}, force close: {force}")

        # First try to find the running application by scanning
        running_apps = await _find_running_applications(app_name)

        if not running_apps:
            logger.warning(f"[AppKiller] Running application not found: {app_name}")
            return False

        # Select shutdown strategy by system
        system = platform.system()
        if system == "Windows":
            # Windows uses complex grouping shutdown strategy
            success = await asyncio.to_thread(
                _kill_windows_app_group, running_apps, app_name, force
            )
        else:
            # macOS and Linux use simple one-by-one shutdown strategy
            success_count = 0
            for app in running_apps:
                success = await asyncio.to_thread(_kill_app_sync, app, force, system)
                if success:
                    success_count += 1
                    logger.info(
                        f"[AppKiller] Successfully closed application: {app['name']} (PID: {app.get('pid', 'N/A')})"
                    )
                else:
                    logger.warning(
                        f"[AppKiller] Failed to close application: {app['name']} (PID: {app.get('pid', 'N/A')})"
                    )

            success = success_count > 0
            logger.info(
                f"[AppKiller] The shutdown operation is completed and {success_count}/{len(running_apps)} processes are successfully closed."
            )

        return success

    except Exception as e:
        logger.error(f"[AppKiller] Error closing application: {e}", exc_info=True)
        return False


async def list_running_applications(args: Dict[str, Any]) -> str:
    """List all running applications.

    Args:
        args: dictionary containing listed arguments
            - filter_name: filter application name (optional)

    Returns:
        str: List of running applications in JSON format"""
    try:
        filter_name = args.get("filter_name", "")
        logger.info(f"[AppKiller] Start listing running applications, filter condition: {filter_name}")

        # Use a thread pool to perform scans to avoid blocking the event loop
        apps = await asyncio.to_thread(_list_running_apps_sync, filter_name)

        result = {
            "success": True,
            "total_count": len(apps),
            "applications": apps,
            "message": f"Found {len(apps)} running applications",
        }

        logger.info(f"[AppKiller] Listing complete, {len(apps)} running applications found")
        return json.dumps(result, ensure_ascii=False, indent=2)

    except Exception as e:
        error_msg = f"List of running application failures: {str(e)}"
        logger.error(f"[AppKiller] {error_msg}", exc_info=True)
        return json.dumps(
            {
                "success": False,
                "total_count": 0,
                "applications": [],
                "message": error_msg,
            },
            ensure_ascii=False,
        )


async def _find_running_applications(app_name: str) -> List[Dict[str, Any]]:
    """Find matching applications that are running.

    Args:
        app_name: The name of the application to look for

    Returns:
        List of matching running applications"""
    try:
        # Get all running applications
        all_apps = await asyncio.to_thread(_list_running_apps_sync, "")

        # Find the best match using the unified matcher
        matched_apps = []

        for app in all_apps:
            score = AppMatcher.match_application(app_name, app)
            if score >= 50:  # Matching threshold
                matched_apps.append(app)

        # Sort by match
        matched_apps.sort(
            key=lambda x: AppMatcher.match_application(app_name, x), reverse=True
        )

        logger.info(f"[AppKiller] Found {len(matched_apps)} matching running apps")
        return matched_apps

    except Exception as e:
        logger.warning(f"[AppKiller] Error finding running applications: {e}")
        return []


def _list_running_apps_sync(filter_name: str = "") -> List[Dict[str, Any]]:
    """Synchronously list running applications.

    Args:
        filter_name: filter application name

    Returns:
        List of running applications"""
    system = platform.system()

    if system == "Darwin":  # macOS
        from .mac.killer import list_running_applications

        return list_running_applications(filter_name)
    elif system == "Windows":  # Windows
        from .windows.killer import list_running_applications

        return list_running_applications(filter_name)
    elif system == "Linux":  # Linux
        from .linux.killer import list_running_applications

        return list_running_applications(filter_name)
    else:
        logger.warning(f"[AppKiller] Unsupported operating system: {system}")
        return []


def _kill_app_sync(app: Dict[str, Any], force: bool, system: str) -> bool:
    """Close the application synchronously.

    Args:
        app: application information
        force: whether to force close
        system: operating system type

    Returns:
        bool: whether the shutdown was successful"""
    try:
        pid = app.get("pid")
        if not pid:
            return False

        if system == "Windows":
            from .windows.killer import kill_application

            return kill_application(pid, force)
        elif system == "Darwin":  # macOS
            from .mac.killer import kill_application

            return kill_application(pid, force)
        elif system == "Linux":  # Linux
            from .linux.killer import kill_application

            return kill_application(pid, force)
        else:
            logger.error(f"[AppKiller] Unsupported operating system: {system}")
            return False

    except Exception as e:
        logger.error(f"[AppKiller] Synchronous closing of application failed: {e}")
        return False


def _kill_windows_app_group(
    apps: List[Dict[str, Any]], app_name: str, force: bool
) -> bool:
    """Group closing strategy for Windows systems.

    Args:
        apps: List of matching application processes
        app_name: application name
        force: whether to force close

    Returns:
        bool: whether the shutdown was successful"""
    try:
        from .windows.killer import kill_application_group

        return kill_application_group(apps, app_name, force)
    except Exception as e:
        logger.error(f"[AppKiller] Windows group closing failed: {e}")
        return False


def get_system_killer():
    """Get the corresponding closer module based on the current system.

    Returns:
        Closer module corresponding to the system"""
    system = platform.system()

    if system == "Darwin":  # macOS
        from .mac import killer

        return killer
    elif system == "Windows":  # Windows
        from .windows import killer

        return killer
    elif system == "Linux":  # Linux
        from .linux import killer

        return killer
    else:
        logger.warning(f"[AppKiller] Unsupported system: {system}")
        return None
