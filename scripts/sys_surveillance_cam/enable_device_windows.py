"""
Path: scripts/sys_surveillance_cam/enable_device_windows.py
Description: Re-enables all webcams on Windows via Device Manager (requires admin).
Version: 1.0.2
Sub_System: SYS_SURVEILLANCE_CAM
System: JERICHO_SYSTEM
"""
import subprocess

def enable_webcams():
    """
    Enables all camera devices using pnputil.
    """
    proc = subprocess.run(
        'wmic path Win32_PnPEntity where "Description like \'%Camera%\' or Description like \'%Imaging Device%\'" get DeviceID',
        shell=True, capture_output=True, text=True
    )
    for line in proc.stdout.strip().splitlines()[1:]:
        device_id = line.strip()
        if device_id:
            print(f"Enabling {device_id}")
            subprocess.run(f'pnputil /enable-device "{device_id}"', shell=True)

if __name__ == "__main__":
    enable_webcams()
