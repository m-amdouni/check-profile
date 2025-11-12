"""Logging configuration"""
import logging
import sys
from pathlib import Path
from rich.logging import RichHandler
from .config import Config


def setup_logger(name: str = "linkedin_scraper") -> logging.Logger:
    """
    Setup logger with both file and console handlers

    Args:
        name: Logger name

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, Config.LOG_LEVEL))

    # Remove existing handlers
    logger.handlers.clear()

    # Console handler with Rich
    console_handler = RichHandler(
        rich_tracebacks=True,
        show_time=True,
        show_path=False
    )
    console_handler.setLevel(logging.INFO)
    console_format = logging.Formatter("%(message)s")
    console_handler.setFormatter(console_format)

    # File handler
    Path(Config.LOG_FILE).parent.mkdir(parents=True, exist_ok=True)
    file_handler = logging.FileHandler(Config.LOG_FILE)
    file_handler.setLevel(logging.DEBUG)
    file_format = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(file_format)

    # Add handlers
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger
