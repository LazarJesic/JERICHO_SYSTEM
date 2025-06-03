"""
Path: scripts/sys_surveillance_cam/disable_device_linux.py
Description: Disables all webcams by removing the uvcvideo kernel module (requires sudo).
Version: 1.0.2
Sub_System: SYS_SURVEILLANCE_CAM
System: JERICHO_SYSTEM
"""
import subprocess

def disable_webcam():
    """
    Removes uvcvideo module to disable Linux webcams.
    """
    subprocess.run(["sudo", "modprobe", "-r", "uvcvideo"], check=True)
    print("Webcam module removed.")

if __name__ == "__main__":
    disable_webcam()
