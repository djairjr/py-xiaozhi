"""Unified application scanner portal.

Automatically select the corresponding scanner implementation based on the current system"""

import asyncio
import json
from typing import Any, Dict

from src.utils.logging_config import get_logger

from .utils import get_system_scanner

logger = get_logger(__name__)


async def scan_installed_applications(args: Dict[str, Any]) -> str:
    """Scans all installed applications on the system.

    Args:
        args: dictionary containing scan parameters
            - force_refresh: whether to force rescan (optional, default False)

    Returns:
        str: List of applications in JSON format"""
    try:
        force_refresh = args.get("force_refresh", False)
        logger.info(f"[AppScanner] Start scanning installed applications, force refresh: {force_refresh}")

        # Get the scanner corresponding to the system
        scanner = get_system_scanner()
        if not scanner:
            error_msg = "Unsupported operating system"
            logger.error(f"[AppScanner] {error_msg}")
            return json.dumps(
                {
                    "success": False,
                    "total_count": 0,
                    "applications": [],
                    "message": error_msg,
                },
                ensure_ascii=False,
            )

        # Use a thread pool to perform scans to avoid blocking the event loop
        apps = await asyncio.to_thread(scanner.scan_installed_applications)

        result = {
            "success": True,
            "total_count": len(apps),
            "applications": apps,
            "message": f"Successfully scanned {len(apps)} installed applications",
        }

        logger.info(f"[AppScanner] Scan completed, found {len(apps)} applications")
        return json.dumps(result, ensure_ascii=False, indent=2)

    except Exception as e:
        error_msg = f"Scan application failed: {str(e)}"
        logger.error(f"[AppScanner] {error_msg}", exc_info=True)
        return json.dumps(
            {
                "success": False,
                "total_count": 0,
                "applications": [],
                "message": error_msg,
            },
            ensure_ascii=False,
        )


async def list_running_applications(args: Dict[str, Any]) -> str:
    """List the applications running on the system.

    Args:
        args: dictionary containing filter parameters
            - filter_name: Apply name filter (optional)

    Returns:
        str: List of running applications in JSON format"""
    try:
        filter_name = args.get("filter_name", "")
        logger.info(f"[AppScanner] Start listing running applications, filter condition: {filter_name}")

        # Get the scanner corresponding to the system
        scanner = get_system_scanner()
        if not scanner:
            error_msg = "Unsupported operating system"
            logger.error(f"[AppScanner] {error_msg}")
            return json.dumps(
                {
                    "success": False,
                    "total_count": 0,
                    "applications": [],
                    "message": error_msg,
                },
                ensure_ascii=False,
            )

        # Use a thread pool to perform scans to avoid blocking the event loop
        apps = await asyncio.to_thread(scanner.scan_running_applications)

        # Apply filters
        if filter_name:
            filter_lower = filter_name.lower()
            filtered_apps = []
            for app in apps:
                if (
                    filter_lower in app.get("name", "").lower()
                    or filter_lower in app.get("display_name", "").lower()
                    or filter_lower in app.get("command", "").lower()
                ):
                    filtered_apps.append(app)
            apps = filtered_apps

        result = {
            "success": True,
            "total_count": len(apps),
            "applications": apps,
            "message": f"Found {len(apps)} running applications",
        }

        logger.info(f"[AppScanner] Listing complete, {len(apps)} running applications found")
        return json.dumps(result, ensure_ascii=False, indent=2)

    except Exception as e:
        error_msg = f"List of failed applications running: {str(e)}"
        logger.error(f"[AppScanner] {error_msg}", exc_info=True)
        return json.dumps(
            {
                "success": False,
                "total_count": 0,
                "applications": [],
                "message": error_msg,
            },
            ensure_ascii=False,
        )
