"""
Autologger - Logging decorator for test automation framework.

Provides automatic logging of function entry/exit with timing information.
"""

import logging
import functools
from datetime import datetime


# Module-level logger instance
logger = None


def logger_init(level=logging.INFO, log_format="%(asctime)s %(message)s",
                datefmt="%H:%M:%S", error_log=None):
    """
    Initialize the logger for the test session.

    Args:
        level: Logging level (logging.INFO, logging.DEBUG, etc.)
        log_format: Log message format string
        datefmt: Date/time format string
        error_log: Optional path to error log file
    """
    global logger
    logger = logging.getLogger(__name__)
    logger.setLevel(level)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_formatter = logging.Formatter(log_format, datefmt=datefmt)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # File handler for errors (if specified)
    if error_log:
        file_handler = logging.FileHandler(error_log, mode='w')
        file_handler.setLevel(logging.ERROR)
        file_formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

    return logger


def automation_logger(category=""):
    """
    Decorator factory for logging function entry/exit.

    Args:
        category: Category label for log messages (e.g., "Test", "Role", "Task", "Page")

    Usage:
        @autologger.automation_logger("Test")
        def test_login(web_interface):
            ...
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Get logger instance
            log = logger if logger else logging.getLogger(__name__)

            # Build log prefix
            prefix = f"[{category}] " if category else ""
            func_name = func.__name__

            # Log entry
            log.info(f"{prefix}{func_name} - START")
            start_time = datetime.now()

            try:
                # Execute function
                result = func(*args, **kwargs)

                # Log successful exit
                duration = (datetime.now() - start_time).total_seconds()
                log.info(f"{prefix}{func_name} - END ({duration:.2f}s)")

                return result

            except Exception as e:
                # Log error and re-raise
                duration = (datetime.now() - start_time).total_seconds()
                log.error(f"{prefix}{func_name} - FAILED ({duration:.2f}s): {str(e)}")
                raise

        return wrapper
    return decorator
