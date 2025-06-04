"""
Path: scripts/sys_audit/hardware_discovery.py
Description: Enumerates all webcams and microphones attached to the system.
Version: 1.0.0
Sub_System: SYS_SURVEILLANCE_CAM
System: JERICHO_SYSTEM
"""

import sys


def discover_webcams():
    """
    Returns a list of dicts with info for all connected webcams (device path, model if available).
    """
    webcams = []
    if sys.platform.startswith("linux"):
        import glob

        for dev in glob.glob("/dev/video*"):
            webcams.append({"device": dev, "platform": "linux"})
    elif sys.platform.startswith("win"):
        # On Windows, use wmic or PowerShell to enumerate imaging devices
        import subprocess

        try:
            cmd = (
                "wmic path Win32_PnPEntity where "
                "\"Description like '%Camera%' or Description like '%Imaging Device%'\" "
                "get Name,DeviceID"
            )
            proc = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            for line in proc.stdout.strip().splitlines()[1:]:
                parts = line.strip().split()
                if parts:
                    name = " ".join(parts[:-1])
                    device_id = parts[-1]
                    webcams.append(
                        {"device": device_id, "name": name, "platform": "win"}
                    )
        except Exception:
            pass
    return webcams


def discover_microphones():
    """
    Returns a list of dicts with info for all connected microphones (device path, model if available).
    """
    mics = []
    if sys.platform.startswith("linux"):
        import glob

        for dev in glob.glob("/dev/snd/*"):
            mics.append({"device": dev, "platform": "linux"})
    elif sys.platform.startswith("win"):
        import subprocess

        try:
            # Use wmic to list audio input devices (microphones)
            cmd = "wmic path Win32_SoundDevice get Name,DeviceID"
            proc = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            for line in proc.stdout.strip().splitlines()[1:]:
                parts = line.strip().split()
                if parts:
                    name = " ".join(parts[:-1])
                    device_id = parts[-1]
                    mics.append({"device": device_id, "name": name, "platform": "win"})
        except Exception:
            pass
    return mics


def discover_hardware():
    """
    Discovers all webcams and microphones attached to the system.
    Returns:
        dict: Contains lists of webcams and microphones.
    """
    return {"webcams": discover_webcams(), "microphones": discover_microphones()}


def discover_audio_devices():
    """
    Discovers all audio devices attached to the system.
    Returns:
        dict: Contains lists of audio devices.
    """
    audio = []
    if sys.platform.startswith("linux"):
        import glob

        for dev in glob.glob("/dev/snd/*"):
            audio.append({"device": dev, "platform": "linux"})
    elif sys.platform.startswith("win"):
        import subprocess

        try:
            cmd = "wmic path Win32_SoundDevice get Name,DeviceID"
            proc = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            for line in proc.stdout.strip().splitlines()[1:]:
                parts = line.strip().split()
                if parts:
                    name = " ".join(parts[:-1])
                    device_id = parts[-1]
                    audio.append({"device": device_id, "name": name, "platform": "win"})
        except Exception:
            pass
    return audio


def discover_processes_using_devices(devices):
    """
    Given a list of device dicts, returns a list of processes using those devices.
    """
    results = []
    if sys.platform.startswith("linux"):
        import subprocess

        for device in devices:
            dev = device["device"]
            try:
                cmd = f"lsof {dev} -F pn"
                proc = subprocess.Popen(
                    cmd,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                )
                out, _ = proc.communicate()
                pid = None
                for line in out.splitlines():
                    if line.startswith("p"):
                        pid = int(line[1:])
                    elif line.startswith("n") and pid:
                        try:
                            with open(f"/proc/{pid}/cmdline", "r") as f:
                                cmdline = f.read().replace("\x00", " ")
                        except Exception:
                            cmdline = ""
                        results.append({"device": dev, "pid": pid, "cmdline": cmdline})
            except Exception:
                continue
    elif sys.platform.startswith("win"):
        # Use handle64.exe if available, fallback to psutil for process names
        try:
            import subprocess

            handle_path = "handle64.exe"
            for device in devices:
                device_id = device["device"]
                cmd = f'"{handle_path}" -a -u | findstr /i "{device_id}"'
            proc = subprocess.Popen(
                cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            out, _ = proc.communicate()
            for line in out.splitlines():
                results.append({"device": device_id, "raw_handle_output": line})
        except Exception:
            pass
    return results


def discover_processes_using_webcams(webcams):
    """
    Given a list of webcam device dicts, returns process info using those devices.
    """
    return discover_processes_using_devices(webcams)


def discover_processes_using_microphones(mics):
    """
    Given a list of microphone device dicts, returns process info using those devices.
    """
    return discover_processes_using_devices(mics)


def discover_processes_using_audio(audio):
    """
    Given a list of audio device dicts, returns process info using those devices.
    """
    return discover_processes_using_devices(audio)


def discover_processes():
    """
    Discovers all processes using webcams, microphones, and audio devices.
    Returns:
        dict: Contains lists of processes using webcams, microphones, and audio devices.
    """
    webcams = discover_webcams()
    microphones = discover_microphones()
    audio_devices = discover_audio_devices()

    return {
        "webcam_processes": discover_processes_using_webcams(webcams),
        "mic_processes": discover_processes_using_microphones(microphones),
        "audio_processes": discover_processes_using_audio(audio_devices),
    }


def discover_hardware_and_processes():
    """
    Discovers all hardware (webcams, microphones, audio devices) and processes using them.
    Returns:
        dict: Contains hardware info and process info.
    """
    hardware_info = discover_hardware()
    process_info = discover_processes()

    return {"hardware_info": hardware_info, "process_info": process_info}


def discover_usb():
    """
    Discovers all USB devices attached to the system.
    Returns:
        list: Contains dicts with USB device info.
    """
    usb_devices = []
    if sys.platform.startswith("linux"):
        import glob

        for dev in glob.glob("/dev/bus/usb/*/*"):
            usb_devices.append({"device": dev, "platform": "linux"})
    elif sys.platform.startswith("win"):
        import subprocess

        try:
            cmd = "wmic path Win32_USBControllerDevice get DeviceID,Description"
            proc = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            for line in proc.stdout.strip().splitlines()[1:]:
                parts = line.strip().split()
                if parts:
                    description = " ".join(parts[:-1])
                    device_id = parts[-1]
                    usb_devices.append(
                        {
                            "device": device_id,
                            "description": description,
                            "platform": "win",
                        }
                    )
        except Exception:
            pass
    return usb_devices


def main():
    """
    Main function to run the hardware discovery.
    """
    hardware_info = discover_hardware()
    print("Webcams:", hardware_info["webcams"])
    print("Microphones:", hardware_info["microphones"])
    print("Audio Devices:", discover_audio_devices())
    print(
        "Processes using webcams:",
        discover_processes_using_webcams(hardware_info["webcams"]),
    )
    print(
        "Processes using microphones:",
        discover_processes_using_microphones(hardware_info["microphones"]),
    )
    print(
        "Processes using audio devices:",
        discover_processes_using_audio(discover_audio_devices()),
    )
    print("USB Devices:", discover_usb())
    print("Hardware and process discovery completed successfully.")


if __name__ == "__main__":
    main()

# Code Explanation
# This script is part of the Jericho System Surveillance Camera module.
# This code is a standalone script for discovering webcams and microphones on the system.
# It can be used as part of a larger system audit or surveillance camera setup.
