"""
Path: scripts/sys_surveillance_cam/enable_device_linux.py
Description: Re-enables all webcams by reloading the uvcvideo kernel module (requires sudo).
Version: 1.0.2
Sub_System: SYS_SURVEILLANCE_CAM
System: JERICHO_SYSTEM
"""
import subprocess

def enable_webcam():
    """
    Inserts uvcvideo module to enable Linux webcams.
    """
    subprocess.run(["sudo", "modprobe", "uvcvideo"], check=True)
    print("Webcam module inserted.")

if __name__ == "__main__":
    enable_webcam()
