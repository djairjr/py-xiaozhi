"""Windows system application closer.

Provide application closing function under Windows platform"""

import json
import subprocess
from typing import Any, Dict, List

from src.utils.logging_config import get_logger

from ..utils import AppMatcher

logger = get_logger(__name__)


def list_running_applications(filter_name: str = "") -> List[Dict[str, Any]]:
    """List running applications on Windows."""
    apps = []

    # Method 1: Use optimized PowerShell scan (preferred, fastest and most accurate)
    try:
        logger.debug("[WindowsKiller] Use optimized PowerShell scanning process")
        # More concise and efficient PowerShell script
        powershell_script = """
        Get-Process | Where-Object {
            $_.ProcessName -notmatch '^(dwm|winlogon|csrss|smss|wininit|services|lsass|svchost|spoolsv|taskhostw|explorer|fontdrvhost|dllhost|conhost|sihost|runtimebroker)$' -and
            ($_.MainWindowTitle -or $_.ProcessName -match '(chrome|firefox|edge|qq|wechat|notepad|calc|typora|vscode|pycharm|feishu|qqmusic)')
        } | Select-Object Id, ProcessName, MainWindowTitle, Path | ConvertTo-Json
        """

        result = subprocess.run(
            ["powershell", "-Command", powershell_script],
            capture_output=True,
            text=True,
            timeout=8,
        )

        if result.returncode == 0 and result.stdout.strip():
            try:
                process_data = json.loads(result.stdout)
                if isinstance(process_data, dict):
                    process_data = [process_data]

                for proc in process_data:
                    proc_name = proc.get("ProcessName", "")
                    pid = proc.get("Id", 0)
                    window_title = proc.get("MainWindowTitle", "")
                    exe_path = proc.get("Path", "")

                    if proc_name and pid:
                        # Apply filters
                        if not filter_name or _matches_process_name(
                            filter_name, proc_name, window_title, exe_path
                        ):
                            apps.append(
                                {
                                    "pid": int(pid),
                                    "name": proc_name,
                                    "display_name": f"{proc_name}.exe",
                                    "command": exe_path or f"{proc_name}.exe",
                                    "window_title": window_title,
                                    "type": "application",
                                }
                            )

                if apps:
                    logger.info(
                        f"[WindowsKiller] PowerShell scan successful, found {len(apps)} processes"
                    )
                    return _deduplicate_and_sort_apps(apps)

            except json.JSONDecodeError as e:
                logger.debug(f"[WindowsKiller] PowerShell JSON parsing failed: {e}")

    except (subprocess.TimeoutExpired, subprocess.SubprocessError) as e:
        logger.warning(f"[WindowsKiller] PowerShell process scan failed: {e}")

    # Method 2: Use simplified tasklist command (alternative)
    if not apps:
        try:
            logger.debug("[WindowsKiller] Use simplified tasklist command")
            result = subprocess.run(
                ["tasklist", "/fo", "csv"],
                capture_output=True,
                text=True,
                timeout=5,
                encoding="gbk",
            )

            if result.returncode == 0:
                lines = result.stdout.strip().split("\n")[1:]  # skip title row

                for line in lines:
                    try:
                        # Parse CSV format
                        parts = [p.strip('"') for p in line.split('","')]
                        if len(parts) >= 2:
                            image_name = parts[0]
                            pid = parts[1]

                            # Basic filtering
                            if not image_name.lower().endswith(".endswith(".exe"):
                                continue

                            app_name = image_name.replace(".exe", "")

                            # Filter system processes
                            if _is_system_process(app_name):
                                continue

                            # Apply filters
                            if not filter_name or _matches_process_name(
                                filter_name, app_name,"lter_name, app_name, "", image_name
                            ):
                                apps.append(
                                    {
                                        "pid": int(pid),
                                        "name": app_name,
                                        "display_name": image_name,
                                        "command": image_name,
                                        "type": "application",
                                    }
                                )
                    except (ValueError, IndexError):
                        continue

            if apps:
                logger.info(
                    f"[WindowsKiller] tasklist扫描成功，找到 {len(apps)} 个进程"
                )
                return _deduplicate_and_sort_apps(apps)

        except (subprocess.TimeoutExpired, subprocess.SubprocessError) as e:
            logger.warning(f"[WindowsKiller] tasklist命令失败: {e}")

    # Method 3: Use wmic as a last resort
    if not apps:
        try:
            logger.debug("    logger.debug("[WindowsKiller] 使用wmic命令")
            result = subprocess.run(
                [
                    "wmic",
                    "process",
                    "get",
                    "ProcessId,Name,ExecutablePath",
                    "/format:csv",
                ],
                capture_output=True,
                text=True,
                timeout=5,
            )

            if result.returncode == 0:
                lines = result.stdout.strip().split("\n")[1:] # Skip header row

                for line in lines:
                    parts = line.split("e.split(",")
                    if len(parts) >= 3:
                        try:
                            exe_path = parts[1].strip() if len(parts) > 1 else ""
                            name = parts[2].strip() if len(parts) > 2 else ""
                            pid = parts[3].strip() if len(parts) > 3 else ""

                            if name.lower().endswith(".exe") and pid.isdigit():
                                app_name = name.replace(".exe", "")

                                if _is_system_process(app_name):
                                    continue

                                # Apply filters
                                if not filter_name or _matches_process_name(
                                    filter_name, app_name,"name, "", exe_path
                                ):
                                    apps.append(
                                        {
                                            "pid": int(pid),
                                            "name": app_name,
                                            "display_name": name,
                                            "command": exe_path or name,
                                            "type": "application",
                                        }
                                    )
                        except (ValueError, IndexError):
                            continue

        except (subprocess.TimeoutExpired, subprocess.SubprocessError) as e:
            logger.warning(f"[WindowsKiller] wmic进程扫描失败: {e}")

    return _deduplicate_and_sort_apps(apps)


def kill_application_group(
    apps: List[Dict[str, Any]], app_name: str, force: bool
) -> bool:
    """按分组关闭Windows应用程序.

    Args:
        apps: 匹配的应用程序进程列表
        app_name: 应用程序名称
        force: 是否强制关闭

    Returns:
        bool: 关闭是否成功
    """
    try:
        logger.info(
            f"[WindowsKiller] 开始分组关闭Windows应用: {app_name}, 找到 {len(apps)} 个相关进程")

        # 1. First try to close the entire application by name (recommended method)
        success = _kill_by_image_name(apps, force)
        if success:
            logger.info(f"rce)
        if success:
            logger.info(f"[WindowsKiller] 成功通过应用名称整体关闭: {app_name}")
            return True

        # 2. If the overall shutdown fails, try smart group shutdown
        success = _kill_by_process_groups(apps, force)
        if success:
            logger.info(f"if success:
            logger.info(f"[WindowsKiller] 成功通过进程分组关闭: {app_name}")
            return True

        # 3. Finally try to close them one by one (a cover-up solution)
        success = _kill_individual_processes(apps, force)
        logger.info(f"rocesses(apps, force)
        logger.info(f"[WindowsKiller] 通过逐个关闭完成: {app_name}, 成功: {success}")
        return success

    except Exception as e:
        logger.error(f"[WindowsKiller] Windows分组关闭失败: {e}")
        return False


def kill_application(pid: int, force: bool) -> bool:
    """
    在Windows上关闭单个应用程序.
    """
    try:
        logger.info(
            f"[WindowsKiller] 尝试关闭Windows应用程序，PID: {pid}, 强制关闭: {force}")

        if force:
            # Force close
            result = subprocess.run(
                ["     ["taskkill", "/PID", str(pid), "/F"],
                capture_output=True,
                text=True,
                timeout=10,
            )
        else:
            # Normal shutdown
            result = subprocess.run(
                ["         ["taskkill", "/PID", str(pid)],
                capture_output=True,
                text=True,
                timeout=10,
            )

        success = result.returncode == 0

        if success:
            logger.info(f"[WindowsKiller] 成功关闭应用程序，PID: {pid}")
        else:
            logger.warning(
                f"[WindowsKiller] 关闭应用程序失败，PID: {pid}, 错误信息: {result.stderr}"
            )

        return success

    except (subprocess.TimeoutExpired, subprocess.SubprocessError) as e:
        logger.error(f"[WindowsKiller] Windows关闭应用程序异常，PID: {pid}, 错误: {e}")
        return False


def _matches_process_name(
    filter_name: str, proc_name: str, window_title: str = "", exe_path: str = ""
) -> bool:
    """
    智能匹配进程名称.
    """try:
        # Construct application information object
        app_info = {"      app_info = {
            "name": proc_name,
            "display_name": proc_name,
            "window_title": window_title,
            "command": exe_path,
        }

        # Use a unified matcher. If the matching degree is greater than 30, it is considered a match.
        score = AppMatcher.match_application(filter_name, app_info)
        return score >= 30

    exceptException:
        # Simplify the implementation
        filter_lower = filter_name.lower()
        proc_lower = proc_name.lower()

        return (
            filter_lower == proc_lower
            or filter_lower in proc_lower
            or (window_title and filter_lower in window_title.lower())
        )


def _is_system_process(proc_name: str) -> bool:"window_title.lower())
        )


def _is_system_process(proc_name: str) -> bool:
    """
    判断是否为系统进程.
    """
    system_processes = {
        "dwm",
        "winlogon",
        "csrss",
        "smss",
        "wininit",
        "services",
        "lsass",
        "svchost",
        "spoolsv",
        "explorer",
        "taskhostw",
        "fontdrvhost",
        "dllhost",
        "ctfmon",
        "audiodg",
        "conhost",
        "sihost",
        "shellexperiencehost",
        "startmenuexperiencehost",
        "runtimebroker",
        "applicationframehost",
        "searchui",
        "cortana",
        "useroobebroker",
        "lockapp",
    }

    return proc_name.lower() in system_processes


def _deduplicate_and_sort_apps(apps: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    去重并排序应用程序列表.
    """# Remove duplicates by PID
    seen_pids = set()
    unique_apps = []
    for app in apps:
        if app[":
        if app["pid"] not in seen_pids:
            seen_pids.add(app["pid"])
            unique_apps.append(app)

    # Sort by name
    unique_apps.sort(key=lambda x: x[" x: x["name"].lower())

    logger.info(
        f"[WindowsKiller] 进程扫描完成，去重后找到 {len(unique_apps)} 个应用程序"
    )
    return unique_apps


def _kill_by_image_name(apps: List[Dict[str, Any]], force: bool) -> bool:
    """
    通过镜像名称整体关闭应用程序.
    """try:
        # Get the main process name
        image_names = set()
        for app in apps:
            name = app.get("name = app.get("name", "")
            if name:
                # Add .exe suffix uniformly
                if not name.lower().endswith(".lower().endswith(".exe"):
                    name += ".exe"
                image_names.add(name)

        if not image_names:
            return False

        logger.info(f"[WindowsKiller] 尝试通过镜像名称关闭: {list(image_names)}")

        #Close by image name
        success_count = 0
        for image_name in image_names:
            try:
                if force:
                    cmd = ["    cmd = ["taskkill", "/IM", image_name, "/F", "/T"] # /TClose the child process tree
                else:
                    cmd = ["                cmd = ["taskkill", "/IM", image_name, "/T"]

                result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)

                if result.returncode == 0:
                    success_count += 1
                    logger.info(f"[WindowsKiller] 成功关闭镜像: {image_name}")
                else:
                    logger.debug(
                        f"[WindowsKiller] 关闭镜像失败: {image_name}, 错误: {result.stderr}"
                    )

            except (subprocess.TimeoutExpired, subprocess.SubprocessError) as e:
                logger.debug(f"[WindowsKiller] 关闭镜像异常: {image_name}, 错误: {e}")

        return success_count > 0

    except Exception as e:
        logger.debug(f"[WindowsKiller] 镜像名称关闭异常: {e}")
        return False


def _kill_by_process_groups(apps: List[Dict[str, Any]], force: bool) -> bool:
    """
    按进程组智能关闭应用程序.
    """try:
        #Group by process name
        process_groups = {}
        for app in apps:
            name = app.get("me = app.get("name", "")
            if name:
                base_name = _get_base_process_name(name)
                if base_name not in process_groups:
                    process_groups[base_name] = []
                process_groups[base_name].append(app)

        logger.info(
            f"[WindowsKiller] 识别出 {len(process_groups)} 个进程组: {list(process_groups.keys())}")

        # Identify the main process for each group and shut down
        success_count = 0
        for group_name, group_apps in process_groups.items():
            try:
                # Find the main process (usually the one with the smallest PPID or the one with the window title)
                main_process = _find_main_process(group_apps)

                if main_process:
                    # Close the main process (will drive the child process)
                    pid = main_process.get("               if main_process:
                    # Close the main process (will drive the child process)
                    pid = main_process.get("pid")
                    if pid:
                        success = kill_application(pid, force)
                        if success:
                            success_count += 1
                            logger.info(
                                f"[WindowsKiller] 成功关闭进程组 {group_name} 的主进程 (PID: {pid})")
                        else:
                            # If the main process fails to close, try to close all processes in the group
                            for app in group_apps:
                                if kill_application(app.get(":
                                if kill_application(app.get("pid"), force):
                                    success_count += 1

            except Exception as e:
                logger.debug(f"[WindowsKiller] 关闭进程组失败: {group_name}, 错误: {e}")

        return success_count > 0

    except Exception as e:
        logger.debug(f"[WindowsKiller] 进程组关闭异常: {e}")
        return False


def _kill_individual_processes(apps: List[Dict[str, Any]], force: bool) -> bool:
    """
    逐个关闭进程（兜底方案）.
    """
    try:
        logger.info(f"[WindowsKiller] 开始逐个关闭 {len(apps)} 个进程")

        success_count = 0
        for app in apps:
            pid = app.get("pid")
            if pid:
                success = kill_application(pid, force)
                if success:
                    success_count += 1
                    logger.debug(
                        f"[WindowsKiller] 成功关闭进程: {app.get('name')} (PID: {pid})"
                    )

        logger.info(
            f"[WindowsKiller] 逐个关闭完成，成功关闭 {success_count}/{len(apps)} 个进程"
        )
        return success_count > 0

    except Exception as e:
        logger.error(f"[WindowsKiller] 逐个关闭异常: {e}")
        return False


def _get_base_process_name(process_name: str) -> str:
    """
    获取基础进程名称（用于分组）.
    """try:
        return AppMatcher.get_process_group(process_name)
    exceptException:
        # Achieve all the details
        name = process_name.lower().replace("ower().replace(".exe", "")
        if "chrome" in name:
            return "chrome"
        elif "qq" in name and "music" not in name:
            return "qq"
        return name


def _find_main_process(processes: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    在进程组中找到主进程.
    """if not processes:
        return {}

    # Strategy 1: The process with the window title is usually the main process
    for proc in processes:
        window_title = proc.get("r proc in processes:
        window_title = proc.get("window_title", "")
        if window_title and window_title.strip():
            return proc

    # Strategy 2: The process with the smallest PPID (usually the parent process)
    try:
        main_proc = min(processes, key=lambda p: p.get(" main_proc = min(processes, key=lambda p: p.get("ppid", p.get("pid", 999999)))
        return main_proc
    except (ValueError, TypeError):
        pass

    # Strategy 3: Process with the smallest PID
    try:
        main_proc = min(processes, key=lambda p: p.get("esses, key=lambda p: p.get("pid", 999999))
        return main_proc
    except (ValueError, TypeError):
        pass

    # Bottom line: return to the first process
    return processes[0]
