"""
Path: src/sys_surveillance_cam/src/event_logger.py
Description: Structured motion event logging to JSON files for downstream systems.
Version: 1.0.2
Sub_System: SYS_SURVEILLANCE_CAM
System: JERICHO_SYSTEM
"""
import json
from datetime import datetime
from pathlib import Path

from src.sys_surveillance_cam.src.utils import generate_uuid, iso_timestamp, safe_join


def log_motion_event(camera_id: str):
    """
    Logs a motion-detected event as a JSON file under data/sys_surveillance_cam/events/{camera_id}/.
    """
    event = {
        "event": "motion_detected",
        "camera_id": camera_id,
        "timestamp": iso_timestamp(),
        "event_id": generate_uuid(),
    }

    out_dir = Path("data/sys_surveillance_cam/events") / camera_id
    out_dir.mkdir(parents=True, exist_ok=True)
    filename = f"event_{datetime.utcnow().strftime('%Y-%m-%d_%H-%M-%S')}.json"
    path = safe_join(out_dir, filename)

    with open(path, "w") as f:
        json.dump(event, f, indent=2)
