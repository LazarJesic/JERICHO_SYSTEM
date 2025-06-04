"""
Path: src/sys_surveillance_cam/movement_detection/motion_detector.py
Description: Frame differencing and motion detection using Gaussian blur and contour analysis.
Version: 1.0.2
Sub_System: SYS_SURVEILLANCE_CAM
System: JERICHO_SYSTEM
"""
import cv2


class MotionDetector:
    """
    Detects motion via frame differencing and contour area thresholding.
    """
    def __init__(self, sensitivity: int = 5000):
        self.previous_frame = None
        self.sensitivity = sensitivity

    def detect(self, frame) -> bool:
        """
        Compares the current frame to the previous grayscale frame.
        Returns True if any contour exceeds the sensitivity threshold.
        """
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        if self.previous_frame is None:
            self.previous_frame = gray
            return False

        delta = cv2.absdiff(self.previous_frame, gray)
        thresh = cv2.threshold(delta, 25, 255, cv2.THRESH_BINARY)[1]
        dilated = cv2.dilate(thresh, None, iterations=2)
        contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        self.previous_frame = gray

        for contour in contours:
            if cv2.contourArea(contour) > self.sensitivity:
                return True
        return False
