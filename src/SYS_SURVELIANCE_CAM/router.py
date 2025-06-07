"""
Path: src/sys_surveillance_cam/router.py
Description: Optional FastAPI router to expose surveillance endpoints (future dashboard/API).
Version: 1.0.2
Sub_System: SYS_SURVEILLANCE_CAM
System: JERICHO_SYSTEM
"""
from fastapi import APIRouter

router = APIRouter()

@router.get("/status")
async def system_status():
    """
    Returns the current status of the surveillance subsystem.
    """
    return {"status": "SYS_SURVEILLANCE_CAM active", "version": "1.0.2"}

@router.get("/cameras")
async def list_cameras():
    """
    Stub endpoint: lists loaded camera IDs.
    """
    # In future, dynamically return actual camera IDs from config
    return {"cameras": ["camera1", "camera2"]}
