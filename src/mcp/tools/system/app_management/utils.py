"""Universal tool for application management.

Provides unified application matching, lookup and caching capabilities"""

import platform
import re
import time
from typing import Any, Dict, List, Optional

from src.utils.logging_config import get_logger

logger = get_logger(__name__)

# Global application cache
_cached_applications: Optional[List[Dict[str, Any]]] = None
_cache_timestamp: float = 0
_cache_duration = 300  # Cache for 5 minutes


class AppMatcher:
    """Unified application matcher."""

    # Special application name mapping - sort by length to avoid short names matching first
    SPECIAL_MAPPINGS = {
        "qq music": ["qqmusic", "qq music", "qq music"],
        "qqmusic": ["qqmusic", "qq music", "qq music"],
        "qq music": ["qqmusic", "qq music", "qq music"],
        "tencent meeting": ["tencent meeting", "Tencent Conference", "voovmeeting"],
        "Tencent Conference": ["tencent meeting", "Tencent Conference", "voovmeeting"],
        "google chrome": ["chrome", "googlechrome", "google chrome"],
        "microsoft edge": ["msedge", "edge", "microsoft edge"],
        "microsoft office": [
            "microsoft office",
            "office",
            "word",
            "excel",
            "powerpoint",
        ],
        "microsoft word": ["microsoft word", "word"],
        "microsoft excel": ["microsoft excel", "excel"],
        "microsoft powerpoint": ["microsoft powerpoint", "powerpoint"],
        "visual studio code": ["code", "vscode", "visual studio code"],
        "wps office": ["wps", "wps office"],
        "qq": ["qq", "qqnt", "tencentqq"],
        "wechat": ["wechat", "weixin", "WeChat"],
        "dingtalk": ["dingtalk", "DingTalk", "ding"],
        "DingTalk": ["dingtalk", "DingTalk", "ding"],
        "chrome": ["chrome", "googlechrome", "google chrome"],
        "firefox": ["firefox", "mozilla"],
        "edge": ["msedge", "edge", "microsoft edge"],
        "safari": ["safari"],
        "notepad": ["notepad", "notepad++"],
        "calculator": ["calc", "calculator", "calculatorapp"],
        "calc": ["calc", "calculator", "calculatorapp"],
        "feishu": ["feishu", "Feishu", "lark"],
        "vscode": ["code", "vscode", "visual studio code"],
        "pycharm": ["pycharm", "pycharm64"],
        "cursor": ["cursor"],
        "typora": ["typora"],
        "wps": ["wps", "wps office"],
        "office": ["microsoft office", "office", "word", "excel", "powerpoint"],
        "word": ["microsoft word", "word"],
        "excel": ["microsoft excel", "excel"],
        "powerpoint": ["microsoft powerpoint", "powerpoint"],
        "finder": ["finder"],
        "terminal": ["terminal", "iterm"],
        "iterm": ["iterm", "iterm2"],
    }

    # Process grouping mapping (for grouping on shutdown)
    PROCESS_GROUPS = {
        "chrome": "chrome",
        "googlechrome": "chrome",
        "firefox": "firefox",
        "edge": "edge",
        "msedge": "edge",
        "safari": "safari",
        "qq": "qq",
        "qqnt": "qq",
        "tencentqq": "qq",
        "qqmusic": "qqmusic",
        "QQMUSIC": "QQMUSIC",
        "QQ Music": "QQ Music",
        "wechat": "wechat",
        "weixin": "wechat",
        "dingtalk": "dingtalk",
        "DingTalk": "dingtalk",
        "feishu": "feishu",
        "Feishu": "feishu",
        "lark": "feishu",
        "vscode": "vscode",
        "code": "vscode",
        "cursor": "cursor",
        "pycharm": "pycharm",
        "pycharm64": "pycharm",
        "typora": "typora",
        "calculatorapp": "calculator",
        "calc": "calculator",
        "calculator": "calculator",
        "tencent meeting": "tencent_meeting",
        "Tencent Conference": "tencent_meeting",
        "voovmeeting": "tencent_meeting",
        "wps": "wps",
        "word": "word",
        "excel": "excel",
        "powerpoint": "powerpoint",
        "finder": "finder",
        "terminal": "terminal",
        "iterm": "iterm",
        "iterm2": "iterm",
    }

    @classmethod
    def normalize_name(cls, name: str) -> str:
        """Standardized application name."""
        if not name:
            return ""

        # Remove .exe suffix
        name = name.lower().replace(".exe", "")

        # Remove version numbers and special characters
        name = re.sub(r"\s+v?\d+[\.\d]*", "", name)
        name = re.sub(r"\s*\(\d+\)", "", name)
        name = re.sub(r"\s*\[.*?\]", "", name)
        name = " ".join(name.split())

        return name.strip()

    @classmethod
    def get_process_group(cls, process_name: str) -> str:
        """Get the group to which the process belongs."""
        normalized = cls.normalize_name(process_name)

        # Check direct mapping
        if normalized in cls.PROCESS_GROUPS:
            return cls.PROCESS_GROUPS[normalized]

        # Check for inclusion relationships
        for key, group in cls.PROCESS_GROUPS.items():
            if key in normalized or normalized in key:
                return group

        return normalized

    @classmethod
    def match_application(cls, target_name: str, app_info: Dict[str, Any]) -> int:
        """Matches an application, returning a match score.

        Args:
            target_name: target application name
            app_info: application information

        Returns:
            int: matching score (0-100), 0 means no match"""
        if not target_name or not app_info:
            return 0

        target_lower = target_name.lower()
        app_name = app_info.get("name", "").lower()
        display_name = app_info.get("display_name", "").lower()
        window_title = app_info.get("window_title", "").lower()
        exe_path = app_info.get("command", "").lower()

        # 1. Exact match (100 points)
        if target_lower == app_name or target_lower == display_name:
            return 100

        # 2. Special mapping matching (95-98 points) - Prioritize matching of more specific keywords
        best_special_score = 0

        for key in cls.SPECIAL_MAPPINGS:
            if key in target_lower or target_lower == key:
                # Check if there is a matching alias
                for alias in cls.SPECIAL_MAPPINGS[key]:
                    if alias.lower() in app_name or alias.lower() in display_name:
                        # Calculate match score: more specific matches score higher
                        if target_lower == key:
                            score = 98  # Exact match for special map keys
                        elif len(key) > len(target_lower) * 0.8:
                            score = 97  # matches of similar length
                        else:
                            score = 95  # General special mapping matching

                        if score > best_special_score:
                            best_special_score = score

        if best_special_score > 0:
            return best_special_score

        # 3. Standardized name matching (90 points)
        normalized_target = cls.normalize_name(target_name)
        normalized_app = cls.normalize_name(app_info.get("name", ""))
        normalized_display = cls.normalize_name(app_info.get("display_name", ""))

        if (
            normalized_target == normalized_app
            or normalized_target == normalized_display
        ):
            return 90

        # 4. Contains matches (70-80 points)
        if target_lower in app_name:
            return 80
        if target_lower in display_name:
            return 75
        if app_name and app_name in target_lower:
            # Avoid mismatching short names with long names
            if len(app_name) < len(target_lower) * 0.5:
                return 50  # lower score
            return 70

        # 5. Window title matching (60 points)
        if window_title and target_lower in window_title:
            return 60

        # 6. Path matching (50 points)
        if exe_path and target_lower in exe_path:
            return 50

        # 7. Fuzzy matching (30 points)
        if cls._fuzzy_match(target_lower, app_name) or cls._fuzzy_match(
            target_lower, display_name
        ):
            return 30

        return 0

    @classmethod
    def _fuzzy_match(cls, target: str, candidate: str) -> bool:
        """Fuzzy matching."""
        if not target or not candidate:
            return False

        # Remove all non-alphanumeric characters for comparison
        target_clean = re.sub(r"[^a-zA-Z0-9\u4e00-\u9fff]", "", target)
        candidate_clean = re.sub(r"[^a-zA-Z0-9\u4e00-\u9fff]", "", candidate)

        return target_clean in candidate_clean or candidate_clean in target_clean


async def get_cached_applications(force_refresh: bool = False) -> List[Dict[str, Any]]:
    """Get a list of cached applications.

    Args:
        force_refresh: whether to force cache refresh

    Returns:
        Application list"""
    global _cached_applications, _cache_timestamp

    current_time = time.time()

    # Check if cache is valid
    if (
        not force_refresh
        and _cached_applications is not None
        and (current_time - _cache_timestamp) < _cache_duration
    ):
        logger.debug(
            f"[AppUtils] List of applications using cache, cache time: {int(current_time - _cache_timestamp)} seconds ago"
        )
        return _cached_applications

    # Rescan application
    try:
        import json

        from .scanner import scan_installed_applications

        logger.info("[AppUtils] Refresh application cache")
        result_json = await scan_installed_applications(
            {"force_refresh": force_refresh}
        )
        result = json.loads(result_json)

        if result.get("success", False):
            _cached_applications = result.get("applications", [])
            _cache_timestamp = current_time
            logger.info(
                f"[AppUtils] Application cache flushed, {len(_cached_applications)} apps found"
            )
            return _cached_applications
        else:
            logger.warning(
                f"[AppUtils] Application scan failed: {result.get('message', 'Unknown error')}"
            )
            return _cached_applications or []

    except Exception as e:
        logger.error(f"[AppUtils] Failed to refresh application cache: {e}")
        return _cached_applications or []


async def find_best_matching_app(
    app_name: str, app_type: str = "any"
) -> Optional[Dict[str, Any]]:
    """Find the best matching app.

    Args:
        app_name: application name
        app_type: application type filter ("installed", "running", "any")

    Returns:
        Best matching application information"""
    try:
        if app_type == "running":
            # Get running applications
            import json

            from .scanner import list_running_applications

            result_json = await list_running_applications({})
            result = json.loads(result_json)

            if not result.get("success", False):
                return None

            applications = result.get("applications", [])
        else:
            # Get installed applications
            applications = await get_cached_applications()

        if not applications:
            return None

        # Calculate the matching degree of all applications
        matches = []
        for app in applications:
            score = AppMatcher.match_application(app_name, app)
            if score > 0:
                matches.append((score, app))

        if not matches:
            return None

        # Sort by score and return the best match
        matches.sort(key=lambda x: x[0], reverse=True)
        best_score, best_app = matches[0]

        logger.info(
            f"[AppUtils] Find the best match: {best_app.get('display_name', best_app.get('name', ''))} (score: {best_score})"
        )
        return best_app

    except Exception as e:
        logger.error(f"[AppUtils] Failed to find matching app: {e}")
        return None


def clear_app_cache():
    """Clear application cache."""
    global _cached_applications, _cache_timestamp

    _cached_applications = None
    _cache_timestamp = 0
    logger.info("[AppUtils] Application cache cleared")


def get_cache_info() -> Dict[str, Any]:
    """Get cache information."""

    current_time = time.time()
    cache_age = current_time - _cache_timestamp if _cache_timestamp > 0 else -1

    return {
        "cached": _cached_applications is not None,
        "count": len(_cached_applications) if _cached_applications else 0,
        "age_seconds": int(cache_age) if cache_age >= 0 else None,
        "valid": cache_age >= 0 and cache_age < _cache_duration,
        "cache_duration": _cache_duration,
    }


def get_system_scanner():
    """Get the corresponding scanner module according to the current system.

    Returns:
        Scanner module corresponding to the system"""
    system = platform.system()

    if system == "Darwin":  # macOS
        from .mac import scanner

        return scanner
    elif system == "Windows":  # Windows
        from .windows import scanner

        return scanner
    elif system == "Linux":  # Linux
        from .linux import scanner

        return scanner
    else:
        logger.warning(f"[AppUtils] Unsupported system: {system}")
        return None
