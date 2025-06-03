"""
Path: scripts/sys_surveillance_cam/disable_device_windows.py
Description: Disables all connected webcams on Windows via Device Manager (requires admin).
Version: 1.0.2
Sub_System: SYS_SURVEILLANCE_CAM
System: JERICHO_SYSTEM
"""
import subprocess

def disable_webcams():
    """
    Disables all camera devices using pnputil.
    """
    # Fetch DeviceIDs for imaging devices
    proc = subprocess.run(
        'wmic path Win32_PnPEntity where "Description like \'%Camera%\' or Description like \'%Imaging Device%\'" get DeviceID',
        shell=True, capture_output=True, text=True
    )
    for line in proc.stdout.strip().splitlines()[1:]:
        device_id = line.strip()
        if device_id:
            print(f"Disabling {device_id}")
            subprocess.run(f'pnputil /disable-device "{device_id}"', shell=True)

if __name__ == "__main__":
    disable_webcams()
