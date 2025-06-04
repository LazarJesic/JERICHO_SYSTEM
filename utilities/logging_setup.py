"""
Path: utilities/logging_setup.py
Description: Configures structured JSON logging using Loguru with rotation.
Version: 2.1.0
Sub_System: UTILITIES
System: JERICHO_SYSTEM
"""

from loguru import logger
import sys


def setup_logging(log_path: str = "logs/watchdog.log", level: str = "INFO"):
    """Configure Loguru logger to write JSON logs with rotation."""
    logger.remove()
    logger.add(
        log_path,
        rotation="10 MB",
        retention="7 days",
        level=level,
        serialize=True,
        backtrace=True,
        diagnose=True
    )
    logger.add(sys.stdout, level=level, format="{time} {level} {message}")
