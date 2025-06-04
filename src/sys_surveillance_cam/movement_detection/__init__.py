"""
Path: src/sys_surveillance_cam/movement_detection/__init__.py
Description: Compatibility package forwarding to src.movement_detection.
Version: 1.0.3
Sub_System: SYS_SURVEILLANCE_CAM
System: JERICHO_SYSTEM
"""
from ..src.movement_detection.motion_detector import MotionDetector
__all__ = ["MotionDetector"]
