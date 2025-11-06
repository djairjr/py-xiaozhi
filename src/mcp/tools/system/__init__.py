"""System toolkit.

Provides complete system management functions, including device status query, audio control and other operations."""

from .device_status import get_device_status
from .manager import SystemToolsManager, get_system_tools_manager
from .tools import get_system_status, set_volume

__all__ = [
    "SystemToolsManager",
    "get_system_tools_manager",
    "get_device_status",
    "get_system_status",
    "set_volume",
]
