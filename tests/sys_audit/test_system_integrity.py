"""
Path: tests/sys_audit/test_system_integrity.py
Description: Basic tests for system_integrity module.
Version: 1.0.0
Sub_System: SYS_SURVEILLANCE_CAM
System: JERICHO_SYSTEM
"""

from scripts.sys_audit.system_integrity import (
    EventStore,
    collect_system_integrity,
    verify_event_store_integrity,
)


def test_collect_system_integrity(tmp_path):
    store = EventStore(sqlite_path=tmp_path / "events.db")
    data = collect_system_integrity(store)
    assert isinstance(data, dict)
    assert "bios" in data
    check = verify_event_store_integrity(store)
    assert check["sqlite_event_count"] >= 1
