"""
Path: src/sys_surveillance_cam/src/utils.py
Description: Reusable utility functions for timestamps, UUIDs, and safe path handling.
Version: 1.0.2
Sub_System: SYS_SURVEILLANCE_CAM
System: JERICHO_SYSTEM
"""
import uuid
from datetime import datetime
from pathlib import Path


def generate_uuid() -> str:
    """
    Generates a UUID4 string.
    """
    return str(uuid.uuid4())


def iso_timestamp() -> str:
    """
    Returns the current UTC time in ISO 8601 format with 'Z' suffix.
    """
    return datetime.utcnow().isoformat() + "Z"


def safe_join(base: Path, filename: str) -> str:
    """
    Ensures the base directory exists and returns a full path for the filename.
    """
    base.mkdir(parents=True, exist_ok=True)
    return str(base / filename)
