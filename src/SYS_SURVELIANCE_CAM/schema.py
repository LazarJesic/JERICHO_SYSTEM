"""
Path: src/sys_surveillance_cam/schema.py
Description: Pydantic schema models for YAML camera config and motion event validation.
Version: 1.0.2
Sub_System: SYS_SURVEILLANCE_CAM
System: JERICHO_SYSTEM
"""
from pydantic import BaseModel, Field
from typing import Literal

class CameraConfig(BaseModel):
    camera_id: str
    source: int
    frame_width: int = Field(default=640, ge=1)
    frame_height: int = Field(default=480, ge=1)
    fps: int = Field(default=20, ge=1, le=60)
    codec: Literal["mp4v", "XVID", "MJPG"] = "mp4v"

class MotionEvent(BaseModel):
    event: Literal["motion_detected"]
    camera_id: str
    timestamp: str
    event_id: str
