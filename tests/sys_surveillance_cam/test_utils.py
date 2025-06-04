"""
Path: tests/sys_surveillance_cam/test_utils.py
Description: Unit tests for utils module.
Version: 1.0.2
Sub_System: SYS_SURVEILLANCE_CAM
System: JERICHO_SYSTEM
"""

from pathlib import Path
from src.sys_surveillance_cam.src.utils import generate_uuid, iso_timestamp, safe_join


def test_generate_uuid():
    uid = generate_uuid()
    assert isinstance(uid, str) and len(uid) > 0


def test_iso_timestamp():
    ts = iso_timestamp()
    assert ts.endswith("Z") and "T" in ts


def test_safe_join(tmp_path):
    base = tmp_path / "dir"
    result = safe_join(base, "file.txt")
    assert Path(result).parent.exists()
