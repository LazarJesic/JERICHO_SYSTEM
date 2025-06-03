"""
Path: tests/sys_surveillance_cam/test_event_logger.py
Description: Unit tests for event_logger module.
Version: 1.0.2
Sub_System: SYS_SURVEILLANCE_CAM
System: JERICHO_SYSTEM
"""
import json
import shutil
from pathlib import Path
import pytest
from src.sys_surveillance_cam.src.event_logger import log_motion_event

@pytest.fixture(autouse=True)
def cleanup(tmp_path, monkeypatch):
    # Redirect event directory to tmp_path for tests
    event_dir = tmp_path / "events"
    monkeypatch.chdir(tmp_path)
    yield
    shutil.rmtree(tmp_path, ignore_errors=True)

def test_log_motion_event_creates_file():
    camera_id = "camera_test"
    log_motion_event(camera_id)
    events = list(Path("data/sys_surveillance_cam/events") / camera_id.glob("*.json"))
    assert len(events) == 1
    data = json.loads(events[0].read_text())
    assert data["camera_id"] == camera_id
    assert "event_id" in data
    assert data["event"] == "motion_detected"
