"""
Screenshot tool for MCP.
"""

from src.utils.logging_config import get_logger

from .screenshot_camera import ScreenshotCamera

logger = get_logger(__name__)


def get_screenshot_camera_instance():
    """Get screenshot camera instance."""
    return ScreenshotCamera.get_instance()


def take_screenshot(arguments: dict) -> str:
    """Utility function to capture desktop and analyze it.

    Args:
        arguments: dictionary containing parameters such as question, display, etc.
                  display optional values: None (all displays),"main"(Home screen),"secondary"(secondary screen), 1,2,3...(specific monitor)

    Returns:
        JSON string of analysis results"""
    camera = get_screenshot_camera_instance()
    logger.info(f"Using screenshot camera implementation: {camera.__class__.__name__}")

    question = arguments.get("question", "")
    display_id = arguments.get("display", None)

    # Parse display parameters
    if display_id:
        if isinstance(display_id, str):
            if display_id.lower() in ["main", "Home screen", "main monitor", "notebook", "Inner screen"]:
                display_id = "main"
            elif display_id.lower() in [
                "secondary",
                "Secondary screen",
                "Secondary display",
                "external",
                "external screen",
                "second screen",
            ]:
                display_id = "secondary"
            else:
                try:
                    display_id = int(display_id)
                except ValueError:
                    logger.warning(
                        f"Invalid display parameter: {display_id}, using default"
                    )
                    display_id = None

    logger.info(f"Taking screenshot with question: {question}, display: {display_id}")

    # screenshot
    success = camera.capture(display_id)
    if not success:
        logger.error("Failed to capture screenshot")
        return '{"success": false, "message": "Failed to capture screenshot"}'

    # Analyze screenshots
    logger.info("Screenshot captured, starting analysis...")
    return camera.analyze(question)
