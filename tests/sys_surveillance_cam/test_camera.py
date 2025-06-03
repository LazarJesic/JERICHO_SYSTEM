"""
Path: tests/sys_surveillance_cam/test_camera.py
Description: Unit tests for CameraHandler behavior (mocked).
Version: 1.0.2
Sub_System: SYS_SURVEILLANCE_CAM
System: JERICHO_SYSTEM
"""
import pytest
import cv2
import numpy as np
from pathlib import Path
from unittest.mock import MagicMock
from src.sys_surveillance_cam.src.camera import CameraHandler

class DummyCapture:
    def __init__(self, frames):
        self.frames = frames
        self.index = 0
        self.opened = True

    def isOpened(self):
        return self.opened

    def read(self):
        if self.index < len(self.frames):
            frame = self.frames[self.index]
            self.index += 1
            return True, frame
        return False, None

    def set(self, *args):
        pass

    def release(self):
        self.opened = False

@pytest.fixture(autouse=True)
def patch_videocapture(monkeypatch):
    # Create a dummy capture returning two identical blank frames, then stop
    blank = np.zeros((480, 640, 3), dtype=np.uint8)
    dummy = DummyCapture([blank, blank])
    monkeypatch.setattr(cv2, "VideoCapture", lambda src: dummy)

def test_camera_runs_without_error(tmp_path, monkeypatch):
    # Redirect data directory
    monkeypatch.chdir(tmp_path)
    config = {
        "camera_id": "cam_test",
        "source": 0,
        "frame_width": 640,
        "frame_height": 480,
        "fps": 20,
        "codec": "mp4v",
        "min_area": 1
    }
    handler = CameraHandler(config)
    # Should not raise any exceptions
    handler.run()
    # Verify recordings and events directories created
    assert (tmp_path / "data/sys_surveillance_cam/recordings/cam_test").exists()
    assert (tmp_path / "data/sys_surveillance_cam/events/cam_test").exists()
