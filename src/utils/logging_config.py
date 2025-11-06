import logging
from logging.handlers import TimedRotatingFileHandler

from colorlog import ColoredFormatter


def setup_logging():
    """Configure the logging system."""
    from .resource_finder import get_project_root

    # Use resource_finder to get the project root directory and create the logs directory
    project_root = get_project_root()
    log_dir = project_root / "logs"
    log_dir.mkdir(exist_ok=True)

    # Log file path
    log_file = log_dir / "app.log"

    # Create root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)  # Set root log level

    # Clear existing processors (avoid duplicate additions)
    if root_logger.handlers:
        root_logger.handlers.clear()

    # Create a console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Create file processors cut by day
    file_handler = TimedRotatingFileHandler(
        log_file,
        when="midnight",  # Cutting every midnight
        interval=1,  # every 1 day
        backupCount=30,  # Keep logs for 30 days
        encoding="utf-8",
    )
    file_handler.setLevel(logging.INFO)
    file_handler.suffix = "%Y-%m-%d.log"  # Log file suffix format

    # Create formatter
    formatter = logging.Formatter(
        "%(asctime)s[%(name)s] - %(levelname)s - %(message)s - %(threadName)s"
    )

    # Console color formatter
    color_formatter = ColoredFormatter(
        "%(green)s%(asctime)s%(reset)s[%(blue)s%(name)s%(reset)s] - "
        "%(log_color)s%(levelname)s%(reset)s - %(green)s%(message)s%(reset)s - "
        "%(cyan)s%(threadName)s%(reset)s",
        log_colors={
            "DEBUG": "cyan",
            "INFO": "white",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "red,bg_white",
        },
        secondary_log_colors={"asctime": {"green": "green"}, "name": {"blue": "blue"}},
    )
    console_handler.setFormatter(color_formatter)
    file_handler.setFormatter(formatter)

    # Add handler to root logger
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)

    # Output log configuration information
    logging.info("The log system has been initialized, log file: %s", log_file)

    return log_file


def get_logger(name):
    """Get the unified configured logger.

    Args:
        name: Logger name, usually module name

    Returns:
        logging.Logger: configured logger

    Example:
        logger = get_logger(__name__)
        logger.info("这是一条信息")
        logger.error("出错了: %s", error_msg)
    """
    logger = logging.getLogger(name)

    # Add some helper methods
    def log_error_with_exc(msg, *args, **kwargs):
        """Log errors and automatically include exception stacks."""
        kwargs["exc_info"] = True
        logger.error(msg, *args, **kwargs)

    # Add to logger
    logger.error_exc = log_error_with_exc

    return logger
