"""
Path: src/sys_surveillance_cam/src/camera.py
Description: Core camera handler for capturing frames, detecting motion, recording video, and logging events.
Version: 1.0.2
Sub_System: SYS_SURVEILLANCE_CAM
System: JERICHO_SYSTEM
"""
import cv2
import time
from pathlib import Path
from loguru import logger
from datetime import datetime

from src.sys_surveillance_cam.src.utils import iso_timestamp, generate_uuid, safe_join
from src.sys_surveillance_cam.src.event_logger import log_motion_event
from src.sys_surveillance_cam.cam_control.video_writer import MP4Writer
from src.sys_surveillance_cam.movement_detection.motion_detector import MotionDetector
from src.sys_surveillance_cam.constants import DEFAULT_CODEC, VIDEO_EXTENSION


class CameraHandler:
    """
    Handles real-time capture, motion detection, video writing, and event logging for a single camera.
    """
    def __init__(self, config: dict):
        self.camera_id = config["camera_id"]
        self.source = config["source"]
        self.width = config.get("frame_width", 640)
        self.height = config.get("frame_height", 480)
        self.fps = config.get("fps", 20)
        self.codec = config.get("codec", DEFAULT_CODEC)
        self.motion_detector = MotionDetector(sensitivity=config.get("min_area", 5000))
        self.base_recording_dir = Path("data/sys_surveillance_cam/recordings") / self.camera_id

        self.cap = cv2.VideoCapture(self.source)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        self.cap.set(cv2.CAP_PROP_FPS, self.fps)

    def run(self):
        """
        Main loop: capture frames, detect motion, record video segments, and log JSON events.
        """
        logger.info(f"Initializing camera {self.camera_id} (source={self.source})")
        if not self.cap.isOpened():
            logger.error(f"Camera {self.camera_id} could not be opened.")
            return

        writer = None
        motion_active = False
        last_motion_ts = None

        while True:
            ret, frame = self.cap.read()
            if not ret:
                logger.warning(f"Camera {self.camera_id} failed to grab frame.")
                break

            if self.motion_detector.detect(frame):
                if not motion_active:
                    now = datetime.utcnow()
                    date_str = now.strftime("%Y-%m-%d")
                    time_str = now.strftime("%H-%M-%S")
                    filename = f"motion_{time_str}.{VIDEO_EXTENSION}"
                    output_dir = self.base_recording_dir / date_str
                    output_path = safe_join(output_dir, filename)

                    writer = MP4Writer(str(output_path), self.codec, self.fps, (self.width, self.height))
                    log_motion_event(self.camera_id)
                    motion_active = True
                    last_motion_ts = time.time()
                    logger.info(f"Motion detected on {self.camera_id}; started recording to {output_path}")

                if writer:
                    writer.write(frame)
                    last_motion_ts = time.time()

            elif motion_active and time.time() - last_motion_ts > 5:
                motion_active = False
                if writer:
                    writer.release()
                    writer = None
                    logger.info(f"Motion ended on {self.camera_id}; recording closed.")

            time.sleep(1 / self.fps)

        # Cleanup on exit
        self.cap.release()
        if writer:
            writer.release()
