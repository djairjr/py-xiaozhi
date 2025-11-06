import argparse
import asyncio
import signal
import sys

from src.application import Application
from src.utils.logging_config import get_logger, setup_logging

logger = get_logger(__name__)


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Xiaozhi Ai client")
    parser.add_argument(
        "--mode",
        choices=["gui", "cli"],
        default="gui",
        help="Running mode: gui (graphical interface) or cli (command line)",
    )
    parser.add_argument(
        "--protocol",
        choices=["mqtt", "websocket"],
        default="websocket",
        help="Communication protocol: mqtt or websocket",
    )
    parser.add_argument(
        "--skip-activation",
        action="store_true",
        help="Skip the activation process and launch the application directly (for debugging only)",
    )
    return parser.parse_args()


async def handle_activation(mode: str) -> bool:
    """Handle the device activation process and rely on the existing event loop.

    Args:
        mode: running mode,"gui"or"cli"Returns:
        bool: whether activation was successful"""
    try:
        from src.core.system_initializer import SystemInitializer

        logger.info("Start device activation process check...")

        system_initializer = SystemInitializer()
        # Unified use of activation processing in SystemInitializer, GUI/CLI adaptive
        result = await system_initializer.handle_activation_process(mode=mode)
        success = bool(result.get("is_activated", False))
        logger.info(f"The activation process is completed, result: {success}")
        return success
    except Exception as e:
        logger.error(f"Activation process exception: {e}", exc_info=True)
        return False


async def start_app(mode: str, protocol: str, skip_activation: bool) -> int:
    """
    启动应用的统一入口（在已有事件循环中执行）.
    """
    logger.info("Start Xiaozhi AI client")

    # Handle activation process
    if not skip_activation:
        activation_success = await handle_activation(mode)
        if not activation_success:
            logger.error("Device activation failed and the program exited")
            return 1
    else:
        logger.warning("Skip activation process (debug mode)")

    # Create and start the application
    app = Application.get_instance()
    return await app.run(mode=mode, protocol=protocol)


if __name__ == "__main__":
    exit_code = 1
    try:
        args = parse_args()
        setup_logging()

        # Detect Wayland environment and set Qt platform plug-in configuration
        import os

        is_wayland = (
            os.environ.get("WAYLAND_DISPLAY")
            or os.environ.get("XDG_SESSION_TYPE") == "wayland"
        )

        if args.mode == "gui" and is_wayland:
            # In a Wayland environment, make sure Qt uses the correct platform plugin
            if "QT_QPA_PLATFORM" not in os.environ:
                # Use the wayland plug-in first, if it fails, fall back to xcb (X11 compatibility layer)
                os.environ["QT_QPA_PLATFORM"] = "wayland;xcb"
                logger.info("Wayland environment: set QT_QPA_PLATFORM=wayland;xcb")

            # Disable some Qt features that are unstable under Wayland
            os.environ.setdefault("QT_WAYLAND_DISABLE_WINDOWDECORATION", "1")
            logger.info("Wayland environment detection is completed and compatibility configuration has been applied")

        # Unified setting of signal processing: Ignore possible SIGTRAP on macOS to avoid "trace trap" causing the process to exit
        try:
            if hasattr(signal, "SIGINT"):
                # Let qasync/Qt handle it Ctrl+C; keep the default or let it be handled by the GUI layer later
                pass
            if hasattr(signal, "SIGTERM"):
                # Allow the process to take the normal shutdown path when receiving a termination signal
                pass
            if hasattr(signal, "SIGTRAP"):
                signal.signal(signal.SIGTRAP, signal.SIG_IGN)
        except Exception:
            # Some platforms/environments do not support setting these signals, just ignore them.
            pass

        if args.mode == "gui":
            # In GUI mode, QApplication and qasync event loops are created uniformly by main
            try:
                import qasync
                from PyQt5.QtWidgets import QApplication
            except ImportError as e:
                logger.error(f"GUI mode requires qasync and PyQt5 libraries: {e}")
                sys.exit(1)

            qt_app = QApplication.instance() or QApplication(sys.argv)

            loop = qasync.QEventLoop(qt_app)
            asyncio.set_event_loop(loop)
            logger.info("The qasync event loop has been created in main")

            # Ensure that closing the last window does not automatically exit the application to avoid premature stopping of the event loop
            try:
                qt_app.setQuitOnLastWindowClosed(False)
            except Exception:
                pass

            with loop:
                exit_code = loop.run_until_complete(
                    start_app(args.mode, args.protocol, args.skip_activation)
                )
        else:
            # CLI mode uses standard asyncio event loop
            exit_code = asyncio.run(
                start_app(args.mode, args.protocol, args.skip_activation)
            )

    except KeyboardInterrupt:
        logger.info("Program interrupted by user")
        exit_code = 0
    except Exception as e:
        logger.error(f"Program exited abnormally: {e}", exc_info=True)
        exit_code = 1
    finally:
        sys.exit(exit_code)
