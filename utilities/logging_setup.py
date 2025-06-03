"""
Path: utilities/logging_setup.py
Description: Centralized Loguru configuration for all subsystems.
Version: 1.0.0
Sub_System: UTILITIES
System: JERICHO_SYSTEM
"""
from loguru import logger
import os

def configure_logging(subsys: str):
    """
    Sets up a rotating file sink under data/<subsys>/logs/.
    """
    log_dir = os.path.join("data", subsys, "logs")
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, f"{subsys}.log")
    logger.remove()
    logger.add(log_path, rotation="10 MB", retention="14 days", serialize=False, level="INFO")
    return logger
