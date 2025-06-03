"""
Path: scripts/sys_surveillance_cam/system_audit/process_audit.py
Description: Finds processes using specified webcam/microphone devices.
Version: 1.0.0
Sub_System: SYS_SURVEILLANCE_CAM
System: JERICHO_SYSTEM
"""
import sys
from hardware_discovery import discover_webcams, discover_microphones, discover_hardware

def audit_webcam_processes(webcams):
    """
    Given list of webcam device paths/names, returns process info (pid, cmdline) using those devices.
    """
    results = []
    if sys.platform.startswith("linux"):
        for cam in webcams:
            dev = cam["device"]
            try:
                import subprocess
                cmd = f"lsof {dev} -F pn"
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
                        results.append({"device": dev, "pid": pid, "cmdline": cmdline})
            except Exception:
                continue
    elif sys.platform.startswith("win"):
        # Use handle64.exe if available, fallback to psutil for process names
        try:
            import subprocess
            handle_path = "handle64.exe"
            for cam in webcams:
                device_id = cam["device"]
                # Not all Windows drivers use 'Device' name in handle.exe output, so this is heuristic
                cmd = f'"{handle_path}" -a -u | findstr /i "{device_id}"'
                proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                out, _ = proc.communicate()
                for line in out.splitlines():
                    results.append({"device": device_id, "raw_handle_output": line})
        except Exception:
            pass
    return results

def audit_mic_processes(mics):
    """
    Given list of mic device paths/names, returns process info using those devices.
    """
    results = []
    if sys.platform.startswith("linux"):
        for mic in mics:
            dev = mic["device"]
            try:
                import subprocess
                cmd = f"lsof {dev} -F pn"
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
                        results.append({"device": dev, "pid": pid, "cmdline": cmdline})
            except Exception:
                continue
    elif sys.platform.startswith("win"):
        # Use handle64.exe if available, fallback to psutil for process names
        try:
            import subprocess
            handle_path = "handle64.exe"
            for mic in mics:
                device_id = mic["device"]
                cmd = f'"{handle_path}" -a -u | findstr /i "{device_id}"'
                proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                out, _ = proc.communicate()
                for line in out.splitlines():
                    results.append({"device": device_id, "raw_handle_output": line})
        except Exception:
            pass
    return results

def main():
    """
    Main function to run the audits.
    """

    webcams = discover_webcams()
    microphones = discover_microphones()

    webcam_processes = audit_webcam_processes(webcams)
    mic_processes = audit_mic_processes(microphones)
    print("Webcam and Microphone Process Audit Results:")
    print("===========================================")
    print("\nWebcams:")
    for cam in webcams:
        print(f"Device: {cam['device']}, Name: {cam.get('name', 'N/A')}")   
    
    print("\nMicrophones:")
    for mic in microphones:
        print(f"Device: {mic['device']}, Name: {mic.get('name', 'N/A')}")
    
    print("\nProcesses using webcams and microphones:")
    print("===========================================")
    if not webcam_processes and not mic_processes:
        print("No processes found using webcams or microphones.")
        return
    if not webcam_processes:
        print("No processes found using webcams.")
    if not mic_processes:
        print("No processes found using microphones.")
    if webcam_processes:
        print("\nWebcam Processes:")    
        for proc in webcam_processes:
            print(proc)
    if mic_processes:
        print("\nMicrophone Processes:")
        for proc in mic_processes:
            print(proc)

if __name__ == "__main__":
    main()
    

######### Code Explanation #########
# This script is designed to be run as a standalone module.
# It will discover connected webcams and microphones, then audit processes using those devices.