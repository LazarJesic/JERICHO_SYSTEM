"""
Path: tests/sys_surveillance_cam/test_motion_detector.py
Description: Unit tests for motion detection logic.
Version: 1.0.2
Sub_System: SYS_SURVEILLANCE_CAM
System: JERICHO_SYSTEM
"""

import numpy as np
import cv2
from src.sys_surveillance_cam.movement_detection.motion_detector import MotionDetector


def generate_blank_frame():
    return np.zeros((480, 640, 3), dtype=np.uint8)


def test_no_motion():
    detector = MotionDetector(sensitivity=1000)
    frame = generate_blank_frame()
    assert not detector.detect(frame)  # First frame sets previous_frame
    assert not detector.detect(frame)  # No change => no motion


def test_small_motion():
    detector = MotionDetector(sensitivity=1)
    frame1 = generate_blank_frame()
    frame2 = frame1.copy()
    cv2.circle(frame2, (100, 100), 50, (255, 255, 255), -1)
    assert not detector.detect(frame1)  # initialize
    assert detector.detect(frame2)  # circle should trigger motion
