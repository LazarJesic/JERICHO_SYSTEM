"""
Path: src/sys_surveillance_cam/exceptions.py
Description: Custom exceptions for configuration, camera handling, and system errors.
Version: 1.0.2
Sub_System: SYS_SURVEILLANCE_CAM
System: JERICHO_SYSTEM
"""
class CameraLoadError(Exception):
    """Raised when a camera fails to initialize."""

class InvalidConfigError(Exception):
    """Raised when a YAML config is missing required fields or is malformed."""

class MotionDetectionError(Exception):
    """Raised when motion detection logic fails."""

class VideoWriteError(Exception):
    """Raised when unable to write video to file."""
