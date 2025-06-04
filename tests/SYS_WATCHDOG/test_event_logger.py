"""
Path: tests/SYS_WATCHDOG/test_event_logger.py
Description: Tests for the structured event_logger.
Version: 2.1.0
Sub_System: SYS_WATCHDOG
System: JERICHO_SYSTEM
"""

import json
import logging
from pathlib import Path
from src.SYS_WATCHDOG.src.event_logger import log_event


def test_log_event(tmp_path):
    log_file = tmp_path / "event.json"
    handler = logging.getLogger("event_logger").handlers[0]
    handler.baseFilename = str(log_file)
    details = {"key": "value"}
    log_event("TEST_EVENT", details)
    entry = json.loads(log_file.read_text().strip())
    assert entry["event_type"] == "TEST_EVENT"
    assert entry["details"] == details
