"""
Path: src/SYS_WATCHDOG/src/utils.py
Description: Utility functions for ISO timestamp and UUID generation.
Version: 2.1.0
Sub_System: SYS_WATCHDOG
System: JERICHO_SYSTEM
"""

import uuid
from datetime import datetime


def generate_uuid():
    """Return a new UUID4 string."""
    return str(uuid.uuid4())


def current_iso_timestamp():
    """Return current UTC time in ISO 8601 format."""
    return datetime.utcnow().isoformat() + "Z"
