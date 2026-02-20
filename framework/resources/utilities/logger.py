"""
Logging utility for the test automation framework.
"""

import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Optional


class Logger:
    """Custom logger class for framework-wide logging."""

    def __init__(self, name: str, log_dir: str = "logs", log_level: str = "INFO"):
        """
        Initialize logger.

        Args:
            name: Logger name (typically module or test name)
            log_dir: Directory to store log files
            log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        """
        self.name = name
        self.log_dir = log_dir
        self.log_level = getattr(logging, log_level.upper(), logging.INFO)
        self.logger = self._setup_logger()

    def _setup_logger(self) -> logging.Logger:
        """
        Set up logger with file and console handlers.

        Returns:
            Configured logger instance
        """
        # Create logger
        logger = logging.getLogger(self.name)
        logger.setLevel(self.log_level)

        # Avoid adding duplicate handlers if logger already exists
        if logger.handlers:
            return logger

        # Create log directory if it doesn't exist
        Path(self.log_dir).mkdir(parents=True, exist_ok=True)

        # Create formatters
        detailed_formatter = logging.Formatter(
            fmt='%(asctime)s [%(levelname)s] [%(name)s] [%(filename)s:%(lineno)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_formatter = logging.Formatter(
            fmt='%(asctime)s [%(levelname)s] %(message)s',
            datefmt='%H:%M:%S'
        )

        # File handler - detailed logging to file
        timestamp = datetime.now().strftime("%Y%m%d")
        log_filename = f"test_automation_{timestamp}.log"
        log_filepath = os.path.join(self.log_dir, log_filename)

        file_handler = logging.FileHandler(log_filepath, mode='a', encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)  # File gets all logs
        file_handler.setFormatter(detailed_formatter)

        # Console handler - less verbose, for user feedback
        console_handler = logging.StreamHandler()
        console_handler.setLevel(self.log_level)
        console_handler.setFormatter(console_formatter)

        # Add handlers to logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        return logger

    def debug(self, message: str) -> None:
        """Log debug message."""
        self.logger.debug(message)

    def info(self, message: str) -> None:
        """Log info message."""
        self.logger.info(message)

    def warning(self, message: str) -> None:
        """Log warning message."""
        self.logger.warning(message)

    def error(self, message: str) -> None:
        """Log error message."""
        self.logger.error(message)

    def critical(self, message: str) -> None:
        """Log critical message."""
        self.logger.critical(message)

    def exception(self, message: str) -> None:
        """Log exception with traceback."""
        self.logger.exception(message)


def get_logger(name: str, log_dir: str = "logs", log_level: str = "INFO") -> Logger:
    """
    Factory function to get a logger instance.

    Args:
        name: Logger name
        log_dir: Directory to store log files
        log_level: Logging level

    Returns:
        Logger instance
    """
    return Logger(name=name, log_dir=log_dir, log_level=log_level)
