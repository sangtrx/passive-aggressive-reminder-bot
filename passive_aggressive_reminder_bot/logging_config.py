"""Centralized logging configuration for enterprise deployments."""
from __future__ import annotations

import logging
from logging.config import dictConfig


DEFAULT_LOG_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {"format": "%(asctime)s %(levelname)s [%(name)s] %(message)s"}
    },
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "default"}
    },
    "root": {"level": "INFO", "handlers": ["console"]},
}


def configure_logging(config: dict | None = None) -> None:
    """Apply logging configuration. If no config is provided, the default is used."""
    dictConfig(config or DEFAULT_LOG_CONFIG)


def get_logger(name: str) -> logging.Logger:
    configure_logging()
    return logging.getLogger(name)
"""Logging configuration for the reminder bot."""

import logging
import sys
from pathlib import Path

# Default log level
DEFAULT_LOG_LEVEL = logging.INFO


def setup_logging(verbose: bool = False, log_file: Path | None = None) -> logging.Logger:
    """Configure logging for the reminder bot.
    
    Args:
        verbose: If True, sets log level to DEBUG
        log_file: Optional path to log file (logs to stdout if None)
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger("reminder_bot")
    logger.setLevel(logging.DEBUG if verbose else DEFAULT_LOG_LEVEL)
    
    # Remove existing handlers
    logger.handlers.clear()
    
    # Create formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stderr)
    console_handler.setLevel(logging.DEBUG if verbose else DEFAULT_LOG_LEVEL)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler (optional)
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance."""
    return logging.getLogger(f"reminder_bot.{name}")
