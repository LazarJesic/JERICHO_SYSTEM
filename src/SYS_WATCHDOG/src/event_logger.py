"""
Path: src/SYS_WATCHDOG/src/event_logger.py
Description: Structured JSON event logger for monitoring events.
Version: 2.1.0
Sub_System: SYS_WATCHDOG
System: JERICHO_SYSTEM
"""

import json
import logging
from datetime import datetime
from pathlib import Path

logger = logging.getLogger("event_logger")
logger.setLevel(logging.INFO)
log_dir = Path("logs")
log_dir.mkdir(parents=True, exist_ok=True)
handler = logging.FileHandler(log_dir / "event_logger.json")
formatter = logging.Formatter('%(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

def log_event(event_type: str, details: dict):
    """Write a JSON-formatted event with timestamp, type, and details."""
    if handler.stream.name != handler.baseFilename:
        handler.close()
        handler.stream = open(handler.baseFilename, handler.mode)
    entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "event_type": event_type,
        "details": details
    }
    logger.info(json.dumps(entry))
