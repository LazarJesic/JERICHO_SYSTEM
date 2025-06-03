"""
Path: scripts/sys_surveillance_cam/audit_camera_processes.py
Description: Audits processes currently using webcam and microphone devices, outputs JSON with separate sections.
Version: 1.0.3
Sub_System: SYS_SURVEILLANCE_CAM
System: JERICHO_SYSTEM
"""
import os
import json
import datetime
import sys
import subprocess
from pathlib import Path


def audit_linux_webcams():
    """
    Lists processes holding /dev/video* handles on Linux.
    Returns:
        List[dict]: Each dict contains 'device', 'pid', and 'cmdline' for webcam processes.
    """
    results = []
    for dev in os.listdir("/dev"):
        if dev.startswith("video"):
            dev_path = f"/dev/{dev}"
            try:
                cmd = f"lsof {dev_path} -F pn"
                proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
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
                        results.append({"device": dev_path, "pid": pid, "cmdline": cmdline})
            except Exception:
                continue
    return results


def audit_linux_mics():
    """
    Lists processes holding /dev/snd/* handles on Linux.
    Returns:
        List[dict]: Each dict contains 'device', 'pid', and 'cmdline' for microphone processes.
    """
    results = []
    snd_dir = "/dev/snd"
    if os.path.isdir(snd_dir):
        for entry in os.listdir(snd_dir):
            dev_path = f"{snd_dir}/{entry}"
            try:
                cmd = f"lsof {dev_path} -F pn"
                proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
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
                        results.append({"device": dev_path, "pid": pid, "cmdline": cmdline})
            except Exception:
                continue
    return results


def audit_windows_webcams():
    """
    Uses handle.exe from SysInternals to find processes using webcam on Windows.
    Returns:
        List[dict]: Each dict contains 'info' from the handle output for webcam.
    """
    results = []
    cmd = 'handle64.exe -a -u | findstr /i "Camera"'
    try:
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        out, _ = proc.communicate()
        for line in out.splitlines():
            results.append({"info": line})
    except Exception:
        pass
    return results


def audit_windows_mics():
    """
    Uses handle.exe from SysInternals to find processes using microphone on Windows.
    Returns:
        List[dict]: Each dict contains 'info' from the handle output for microphone.
    """
    results = []
    # Common audio keywords: "Audio", "Microphone", "Wave"
    keywords = ["Audio", "Microphone", "Wave"]
    for kw in keywords:
        cmd = f'handle64.exe -a -u | findstr /i "{kw}"'
        try:
            proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            out, _ = proc.communicate()
            for line in out.splitlines():
                results.append({"info": line})
        except Exception:
            continue
    return results


def main():
    """
    Main entry: determines OS, audits webcams and microphones, and writes results to JSON.
    """
    timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")
    audit_dir = Path("data/sys_surveillance_cam/audit")
    audit_dir.mkdir(parents=True, exist_ok=True)
    outfile = audit_dir / f"audit_{timestamp}.json"

    audit_data = {
        "timestamp": timestamp,
        "platform": sys.platform,
        "webcam_processes": [],
        "mic_processes": []
    }

    if sys.platform.startswith("linux"):
        audit_data["webcam_processes"] = audit_linux_webcams()
        audit_data["mic_processes"] = audit_linux_mics()
    elif sys.platform.startswith("win"):
        audit_data["webcam_processes"] = audit_windows_webcams()
        audit_data["mic_processes"] = audit_windows_mics()
    else:
        print("Unsupported OS for media device auditing.")
        return

    try:
        with open(outfile, "w") as f:
            json.dump(audit_data, f, indent=2)
        print(f"Audit saved to {outfile}")
    except Exception as e:
        print(f"Failed to write audit results: {e}")


if __name__ == "__main__":
    main()
