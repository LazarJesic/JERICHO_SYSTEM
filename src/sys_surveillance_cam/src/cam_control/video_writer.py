"""
Path: src/sys_surveillance_cam/cam_control/video_writer.py
Description: MP4 video writer encapsulation using OpenCV.
Version: 1.0.2
Sub_System: SYS_SURVEILLANCE_CAM
System: JERICHO_SYSTEM
"""
import cv2
from pathlib import Path


class MP4Writer:
    """
    Abstracts OpenCV's VideoWriter for MP4 output.
    """
    def __init__(self, filepath: str, codec: str, fps: int, frame_size: tuple):
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        fourcc = cv2.VideoWriter_fourcc(*codec)
        self.writer = cv2.VideoWriter(filepath, fourcc, fps, frame_size)

    def write(self, frame):
        """
        Writes a single frame to the video file.
        """
        self.writer.write(frame)

    def release(self):
        """
        Releases the video writer and closes the file.
        """
        if self.writer:
            self.writer.release()
            self.writer = None
