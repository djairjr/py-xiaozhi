"""macOS application scanner.

Application scanning and management specifically for macOS systems"""

import platform
import subprocess
from pathlib import Path
from typing import Dict, List

from src.utils.logging_config import get_logger

logger = get_logger(__name__)


def scan_installed_applications() -> List[Dict[str, str]]:
    """Scan installed applications in macOS systems.

    Returns:
        List[Dict[str, str]]: application list"""
    if platform.system() != "Darwin":
        return []

    apps = []

    # Scan the /Applications directory
    applications_dir = Path("/Applications")
    if applications_dir.exists():
        for app_path in applications_dir.glob("*.app"):
            app_name = app_path.stem
            clean_name = _clean_app_name(app_name)
            apps.append(
                {
                    "name": clean_name,
                    "display_name": app_name,
                    "path": str(app_path),
                    "type": "application",
                }
            )

    # Scan user application directory
    user_apps_dir = Path.home() / "Applications"
    if user_apps_dir.exists():
        for app_path in user_apps_dir.glob("*.app"):
            app_name = app_path.stem
            clean_name = _clean_app_name(app_name)
            apps.append(
                {
                    "name": clean_name,
                    "display_name": app_name,
                    "path": str(app_path),
                    "type": "user_application",
                }
            )

    # Add commonly used system applications
    system_apps = [
        {
            "name": "Calculator",
            "display_name": "calculator",
            "path": "Calculator",
            "type": "system",
        },
        {
            "name": "TextEdit",
            "display_name": "Text editing",
            "path": "TextEdit",
            "type": "system",
        },
        {
            "name": "Preview",
            "display_name": "Preview",
            "path": "Preview",
            "type": "system",
        },
        {
            "name": "Safari",
            "display_name": "Safari browser",
            "path": "Safari",
            "type": "system",
        },
        {"name": "Finder", "display_name": "find", "path": "Finder", "type": "system"},
        {
            "name": "Terminal",
            "display_name": "terminal",
            "path": "Terminal",
            "type": "system",
        },
        {
            "name": "System Preferences",
            "display_name": "System Preferences",
            "path": "System Preferences",
            "type": "system",
        },
    ]
    apps.extend(system_apps)

    logger.info(f"[MacScanner] Scan completed, found {len(apps)} applications")
    return apps


def scan_running_applications() -> List[Dict[str, str]]:
    """Scan running applications in macOS systems.

    Returns:
        List[Dict[str, str]]: List of running applications"""
    if platform.system() != "Darwin":
        return []

    apps = []

    try:
        # Use ps command to get process information
        result = subprocess.run(
            ["ps", "-eo", "pid,ppid,comm,command"],
            capture_output=True,
            text=True,
            timeout=10,
        )

        if result.returncode == 0:
            lines = result.stdout.strip().split("\n")[1:]  # skip title row

            for line in lines:
                parts = line.strip().split(None, 3)
                if len(parts) >= 4:
                    pid, ppid, comm, command = parts

                    # Filter out unnecessary processes
                    if _should_include_process(comm, command):
                        display_name = _extract_app_name(comm, command)
                        clean_name = _clean_app_name(display_name)

                        apps.append(
                            {
                                "pid": int(pid),
                                "ppid": int(ppid),
                                "name": clean_name,
                                "display_name": display_name,
                                "command": command,
                                "type": "application",
                            }
                        )

        logger.info(f"[MacScanner] Found {len(apps)} running applications")
        return apps

    except Exception as e:
        logger.error(f"[MacScanner] Failed to scan running application: {e}")
        return []


def _should_include_process(comm: str, command: str) -> bool:
    """Determine whether the process should be included.

    Args:
        comm: process name
        command: complete command

    Returns:
        bool: whether to include"""
    # Exclude system processes and services
    system_processes = {
        # System core process
        "kernel_task",
        "launchd",
        "kextd",
        "UserEventAgent",
        "cfprefsd",
        "loginwindow",
        "WindowServer",
        "SystemUIServer",
        "Dock",
        "Finder",
        "ControlCenter",
        "NotificationCenter",
        "WallpaperAgent",
        "Spotlight",
        "WiFiAgent",
        "CoreLocationAgent",
        "bluetoothd",
        "wirelessproxd",
        # System services
        "com.apple.",
        "suhelperd",
        "softwareupdated",
        "cloudphotod",
        "identityservicesd",
        "imagent",
        "sharingd",
        "remindd",
        "contactsd",
        "accountsd",
        "CallHistorySyncHelper",
        "CallHistoryPluginHelper",
        # Drivers and extensions
        "AppleSpell",
        "coreaudiod",
        "audio",
        "webrtc",
        "chrome_crashpad_handler",
        "crashpad_handler",
        "fsnotifier",
        "mdworker",
        "mds",
        "spotlight",
        # Other system components
        "automountd",
        "autofsd",
        "aslmanager",
        "syslogd",
        "ntpd",
        "mDNSResponder",
        "distnoted",
        "notifyd",
        "powerd",
        "thermalmonitord",
        "watchdogd",
    }

    # Check if it is a system process
    comm_lower = comm.lower()
    command_lower = command.lower()

    # Exclude empty names or system paths
    if not comm or comm_lower in system_processes:
        return False

    # Exclude processes under system path
    if any(
        path in command_lower
        for path in [
            "/system/library/",
            "/library/apple/",
            "/usr/libexec/",
            "/system/applications/utilities/",
            "/private/var/",
            "com.apple.",
            ".xpc/",
            ".framework/",
            ".appex/",
            "helper (gpu)",
            "helper (renderer)",
            "helper (plugin)",
            "crashpad_handler",
            "fsnotifier",
        ]
    ):
        return False

    # Exclude obvious system services
    if any(
        keyword in command_lower
        for keyword in [
            "xpcservice",
            "daemon",
            "agent",
            "service",
            "monitor",
            "updater",
            "sync",
            "backup",
            "cache",
            "log",
        ]
    ):
        return False

    # Contains only user applications
    user_app_indicators = ["/applications/", "/users/", "~/", ".app/contents/macos/"]

    return any(indicator in command_lower for indicator in user_app_indicators)


def _extract_app_name(comm: str, command: str) -> str:
    """Extract application name from process information.

    Args:
        comm: process name
        command: complete command

    Returns:
        str: application name"""
    # Try to extract the .app name from the command path
    if ".app/Contents/MacOS/" in command:
        try:
            app_path = command.split(".app/Contents/MacOS/")[0] + ".app"
            app_name = Path(app_path).name.replace(".app", "")
            return app_name
        except (IndexError, AttributeError):
            pass

    # Try to extract from /Applications/ path
    if "/Applications/" in command:
        try:
            parts = command.split("/Applications/")[1].split("/")[0]
            if parts.endswith(".app"):
                return parts.replace(".app", "")
        except (IndexError, AttributeError):
            pass

    # Use process name
    return comm if comm else "Unknown"


def _clean_app_name(name: str) -> str:
    """Clean application names, removing version numbers and special characters.

    Args:
        name: original name

    Returns:
        str: cleaned name"""
    if not name:
        return ""

    # Remove common version number patterns
    import re

    # Remove version number (e.g. "App 1.0", "App v2.1", "App (2023)")
    name = re.sub(r"\s+v?\d+[\.\d]*", "", name)
    name = re.sub(r"\s*\(\d+\)", "", name)
    name = re.sub(r"\s*\[.*?\]", "", name)

    # Remove extra spaces
    name = " ".join(name.split())

    return name.strip()
