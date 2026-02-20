"""
Autologger - Logging decorator for test automation framework.

Provides automatic logging of function entry/exit with timing information.
"""

import logging
import functools
from datetime import datetime

logger = logging.getLogger(__name__)


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
            # Build log prefix
            prefix = f"[{category}] " if category else ""
            func_name = func.__name__

            logger.info(f"{prefix}{func_name} - START")
            start_time = datetime.now()

            try:
                # Execute function
                result = func(*args, **kwargs)

                duration = (datetime.now() - start_time).total_seconds()
                logger.info(f"{prefix}{func_name} - END ({duration:.2f}s)")

                return result

            except Exception as e:
                duration = (datetime.now() - start_time).total_seconds()
                logger.error(f"{prefix}{func_name} - FAILED ({duration:.2f}s): {repr(e)}")
                raise

        return wrapper
    return decorator
