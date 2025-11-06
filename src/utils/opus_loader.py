# Process opus dynamic library before importing opuslib
import ctypes
import os
import platform
import shutil
import sys
from enum import Enum
from pathlib import Path
from typing import List, Tuple, Union, cast

# Get logger
from src.utils.logging_config import get_logger

logger = get_logger(__name__)


# Platform constant definition
class PLATFORM(Enum):
    WINDOWS = "windows"
    MACOS = "darwin"
    LINUX = "linux"


# Architectural constant definition
class ARCH(Enum):
    WINDOWS = {"arm": "x64", "intel": "x64"}
    MACOS = {"arm": "arm64", "intel": "x64"}
    LINUX = {"arm": "arm64", "intel": "x64"}


# Dynamic link library path constant definition
class LIB_PATH(Enum):
    WINDOWS = "libs/libopus/win/x64"
    MACOS = "libs/libopus/mac/{arch}"
    LINUX = "libs/libopus/linux/{arch}"


# Dynamic link library name constant definition
class LIB_INFO(Enum):
    WINDOWS = {"name": "opus.dll", "system_name": ["opus"]}
    MACOS = {"name": "libopus.dylib", "system_name": ["libopus.dylib"]}
    LINUX = {"name": "libopus.so", "system_name": ["libopus.so.0", "libopus.so"]}


def get_platform() -> str:
    system = platform.system().lower()
    if system == "windows" or system.startswith("win"):
        system = PLATFORM.WINDOWS
    elif system == "darwin":
        system = PLATFORM.MACOS
    else:
        system = PLATFORM.LINUX
    return system


def get_arch(system: PLATFORM) -> str:
    architecture = platform.machine().lower()
    is_arm = "arm" in architecture or "aarch64" in architecture
    if system == PLATFORM.WINDOWS:
        arch_name = ARCH.WINDOWS.value["arm" if is_arm else "intel"]
    elif system == PLATFORM.MACOS:
        arch_name = ARCH.MACOS.value["arm" if is_arm else "intel"]
    else:
        arch_name = ARCH.LINUX.value["arm" if is_arm else "intel"]
    return architecture, arch_name


def get_lib_path(system: PLATFORM, arch_name: str):
    if system == PLATFORM.WINDOWS:
        lib_name = LIB_PATH.WINDOWS.value
    elif system == PLATFORM.MACOS:
        lib_name = LIB_PATH.MACOS.value.format(arch=arch_name)
    else:
        lib_name = LIB_PATH.LINUX.value.format(arch=arch_name)
    return lib_name


def get_lib_name(system: PLATFORM, local: bool = True) -> Union[str, List[str]]:
    """Get the library name.

    Args:
        system (PLATFORM): platform
        local (bool, optional): Whether to get the local name (str), the default is True. If it is False, get the system name list (List).

    Returns:
        str | List: library name"""
    key = "name" if local else "system_name"
    if system == PLATFORM.WINDOWS:
        lib_name = LIB_INFO.WINDOWS.value[key]
    elif system == PLATFORM.MACOS:
        lib_name = LIB_INFO.MACOS.value[key]
    else:
        lib_name = LIB_INFO.LINUX.value[key]
    return lib_name


def get_system_info() -> Tuple[str, str]:
    """Get current system information."""
    # Standardized system name
    system = get_platform()

    # Standardized schema name
    _, arch_name = get_arch(system)
    logger.info(f"Detected system: {system}, architecture: {arch_name}")

    return system, arch_name


def get_search_paths(system: PLATFORM, arch_name: str) -> List[Tuple[Path, str]]:
    """Get a list of library file search paths (using Unified Resource Finder)"""
    from .resource_finder import find_libs_dir, get_project_root

    lib_name = cast(str, get_lib_name(system))

    search_paths: List[Tuple[Path, str]] = []

    # Mapping system names to directory names
    system_dir_map = {
        PLATFORM.WINDOWS: "win",
        PLATFORM.MACOS: "mac",
        PLATFORM.LINUX: "linux",
    }

    system_dir = system_dir_map.get(system)

    # First try to find the libs directory for your specific platform and architecture
    if system_dir:
        specific_libs_dir = find_libs_dir(f"libopus/{system_dir}", arch_name)
        if specific_libs_dir:
            search_paths.append((specific_libs_dir, lib_name))
            logger.debug(f"Find the specific platform architecture libs directory: {specific_libs_dir}")

    # Then look for the libs directory for the specific platform
    if system_dir:
        platform_libs_dir = find_libs_dir(f"libopus/{system_dir}")
        if platform_libs_dir:
            search_paths.append((platform_libs_dir, lib_name))
            logger.debug(f"Find the platform-specific libs directory: {platform_libs_dir}")

    # Find common libs directory
    general_libs_dir = find_libs_dir()
    if general_libs_dir:
        search_paths.append((general_libs_dir, lib_name))
        logger.debug(f"Add general libs directory: {general_libs_dir}")

    # Add the project root directory as a last resort
    project_root = get_project_root()
    search_paths.append((project_root, lib_name))

    # Print all search paths to help debugging
    for dir_path, filename in search_paths:
        full_path = dir_path / filename
        logger.debug(f"Search path: {full_path} (Exists: {full_path.exists()})")
    return search_paths


def find_system_opus() -> str:
    """Find the opus library from the system path."""
    system, _ = get_system_info()
    lib_path = ""

    try:
        # Get the name of the opus library on the system
        lib_names = cast(List[str], get_lib_name(system, False))

        # Try loading every possible name
        for lib_name in lib_names:
            try:
                # Import ctypes.util to use find_library function
                import ctypes.util

                system_lib_path = ctypes.util.find_library(lib_name)

                if system_lib_path:
                    lib_path = system_lib_path
                    logger.info(f"Find the opus library in the system path: {lib_path}")
                    break
                else:
                    # Directly try to load the library name
                    ctypes.cdll.LoadLibrary(lib_name)
                    lib_path = lib_name
                    logger.info(f"Directly load the system opus library: {lib_name}")
                    break
            except Exception as e:
                logger.debug(f"Failed to load system library {lib_name}: {e}")
                continue

    except Exception as e:
        logger.error(f"Failed to find system opus library: {e}")

    return lib_path


def copy_opus_to_project(system_lib_path):
    """Copy the system libraries to the project directory."""
    from .resource_finder import get_project_root

    system, arch_name = get_system_info()

    if not system_lib_path:
        logger.error("Unable to copy opus library: system library path is empty")
        return None

    try:
        # Use resource_finder to get the project root directory
        project_root = get_project_root()

        # Get target directory path - use actual directory structure
        target_path = get_lib_path(system, arch_name)
        target_dir = project_root / target_path

        # Create the target directory if it does not exist
        target_dir.mkdir(parents=True, exist_ok=True)

        # Determine the target file name
        lib_name = cast(str, get_lib_name(system))
        target_file = target_dir / lib_name

        # Copy files
        shutil.copy2(system_lib_path, target_file)
        logger.info(f"Copied opus library from {system_lib_path} to {target_file}")

        return str(target_file)

    except Exception as e:
        logger.error(f"Failed to copy opus library to project directory: {e}")
        return None


def setup_opus() -> bool:
    """Set up opus dynamic library."""
    # Check if it has been loaded by runtime_hook
    if hasattr(sys, "_opus_loaded"):
        logger.info("opus library has been loaded by runtime hook")
        return True

    # Get current system information
    system, arch_name = get_system_info()
    logger.info(f"Current system: {system}, architecture: {arch_name}")

    # Build search path
    search_paths = get_search_paths(system, arch_name)

    # Find local library files
    lib_path = ""
    lib_dir = ""

    for dir_path, file_name in search_paths:
        full_path = dir_path / file_name
        if full_path.exists():
            lib_path = str(full_path)
            lib_dir = str(dir_path)
            logger.info(f"Find the opus library file: {lib_path}")
            break

    # If not found locally, try to find it from the system
    if not lib_path:
        logger.warning("The opus library file was not found locally. Try loading it from the system path.")
        system_lib_path = find_system_opus()

        if system_lib_path:
            # First attempt to use system libraries directly
            try:
                _ = ctypes.cdll.LoadLibrary(system_lib_path)
                logger.info(f"The opus library has been loaded from the system path: {system_lib_path}")
                sys._opus_loaded = True
                return True
            except Exception as e:
                logger.warning(f"Failed to load system opus library: {e}, try to copy to project directory")

            # If direct loading fails, try copying to the project directory
            lib_path = copy_opus_to_project(system_lib_path)
            if lib_path:
                lib_dir = str(Path(lib_path).parent)
            else:
                logger.error("Unable to find or copy opus library file")
                return False
        else:
            logger.error("The opus library file was not found in the system.")
            return False

    # Special handling for Windows platform
    if system == PLATFORM.WINDOWS and lib_dir:
        # Add DLL search path
        if hasattr(os, "add_dll_directory"):
            try:
                os.add_dll_directory(lib_dir)
                logger.debug(f"Added DLL search path: {lib_dir}")
            except Exception as e:
                logger.warning(f"Failed to add DLL search path: {e}")

        # Set environment variables
        os.environ["PATH"] = lib_dir + os.pathsep + os.environ.get("PATH", "")

    # patch library path
    _patch_find_library("opus", lib_path)

    # Try loading the library
    try:
        # Load DLL and store reference to prevent garbage collection
        _ = ctypes.CDLL(lib_path)
        logger.info(f"Successfully loaded opus library: {lib_path}")
        sys._opus_loaded = True
        return True
    except Exception as e:
        logger.error(f"Failed to load opus library: {e}")
        return False


def _patch_find_library(lib_name: str, lib_path: str):
    """Fix ctypes.util.find_library function."""
    import ctypes.util

    original_find_library = ctypes.util.find_library

    def patched_find_library(name):
        if name == lib_name:
            return lib_path
        return original_find_library(name)

    ctypes.util.find_library = patched_find_library
