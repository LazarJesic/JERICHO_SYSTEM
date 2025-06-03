"""
Path: src/sys_surveillance_cam/constants.py
Description: Central constants used across the SYS_SURVEILLANCE_CAM subsystem.
Version: 1.0.2
Sub_System: SYS_SURVEILLANCE_CAM
System: JERICHO_SYSTEM
"""
DEFAULT_CODEC = "mp4v"
VIDEO_EXTENSION = "mp4"
LOG_FILE_TEMPLATE = "data/sys_surveillance_cam/logs/{camera_id}/surveillance.log"
RECORDING_DIR_TEMPLATE = "data/sys_surveillance_cam/recordings/{camera_id}/{date}/"
EVENT_DIR_TEMPLATE = "data/sys_surveillance_cam/events/{camera_id}/"
