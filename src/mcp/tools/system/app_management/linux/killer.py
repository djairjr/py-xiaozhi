"""Linux system application closer.

Provide application shutdown function under Linux platform"""

import subprocess
from typing import Any, Dict, List

from src.utils.logging_config import get_logger

logger = get_logger(__name__)


def list_running_applications(filter_name: str = "") -> List[Dict[str, Any]]:
    """List running applications on Linux."""
    apps = []

    try:
        # Use ps command to get process information
        result = subprocess.run(
            ["ps", "-eo", "pid,ppid,comm,command", "--no-headers"],
            capture_output=True,
            text=True,
            timeout=10,
        )

        if result.returncode == 0:
            lines = result.stdout.strip().split("\n")

            for line in lines:
                parts = line.strip().split(None, 3)
                if len(parts) >= 4:
                    pid, ppid, comm, command = parts

                    # Filter GUI applications
                    is_gui_app = (
                        not command.startswith("/usr/bin/")
                        and not command.startswith("/bin/")
                        and not command.startswith("[")  # kernel thread
                        and len(comm) > 2
                    )

                    if is_gui_app:
                        app_name = comm

                        # Apply filters
                        if not filter_name or filter_name.lower() in app_name.lower():
                            apps.append(
                                {
                                    "pid": int(pid),
                                    "ppid": int(ppid),
                                    "name": app_name,
                                    "display_name": app_name,
                                    "command": command,
                                    "type": "application",
                                }
                            )

    except (subprocess.TimeoutExpired, subprocess.SubprocessError) as e:
        logger.warning(f"[LinuxKiller] Linux process scan failed: {e}")

    return apps


def kill_application(pid: int, force: bool) -> bool:
    """Close application on Linux."""
    try:
        logger.info(
            f"[LinuxKiller] Try to close Linux application, PID: {pid}, force close: {force}"
        )

        if force:
            # Force close (SIGKILL)
            result = subprocess.run(
                ["kill", "-9", str(pid)], capture_output=True, timeout=5
            )
        else:
            # Normal shutdown (SIGTERM)
            result = subprocess.run(
                ["kill", "-15", str(pid)], capture_output=True, timeout=5
            )

        success = result.returncode == 0

        if success:
            logger.info(f"[LinuxKiller] Successfully closed application, PID: {pid}")
        else:
            logger.warning(f"[LinuxKiller] Failed to close application, PID: {pid}")

        return success

    except (subprocess.TimeoutExpired, subprocess.SubprocessError) as e:
        logger.error(f"[LinuxKiller] Linux failed to close application: {e}")
        return False
