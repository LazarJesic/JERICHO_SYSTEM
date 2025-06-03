"""
Path: scripts/sys_audit/report_writer.py
Description: Writes the audit results as a unified, timestamped JSON report.
Version: 1.0.0
Sub_System: SYS_SURVEILLANCE_CAM
System: JERICHO_SYSTEM
"""
import json
from pathlib import Path
from datetime import datetime

def write_audit_report(webcam_devices, webcam_procs, mic_devices, mic_procs, output_dir):
    # Writes a comprehensive audit report of webcams and microphones with their associated processes.
    timestamp = datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")
    report = {
        "timestamp": timestamp,
        "webcams": webcam_devices,
        "webcam_processes": webcam_procs,
        "microphones": mic_devices,
        "mic_processes": mic_procs,
    }
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    outfile = output_dir / f"system_audit_{timestamp}.json"
    with open(outfile, "w") as f:
        json.dump(report, f, indent=2)
    print(f"System audit saved to {outfile}")


def write_hardware_report(hardware_info, output_dir):
    # Writes a report of hardware information (webcams, microphones, etc.) with a timestamp.
    timestamp = datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")
    report = {
        "timestamp": timestamp,
        "hardware_info": hardware_info,
    }
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    outfile = output_dir / f"hardware_report_{timestamp}.json"
    with open(outfile, "w") as f:
        json.dump(report, f, indent=2)
    print(f"Hardware report saved to {outfile}")

def write_process_report(process_info, output_dir):
    # Writes a report of processes using webcams and microphones with a timestamp.
    timestamp = datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")
    report = {
        "timestamp": timestamp,
        "process_info": process_info,
    }
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    outfile = output_dir / f"process_report_{timestamp}.json"
    with open(outfile, "w") as f:
        json.dump(report, f, indent=2)
    print(f"Process report saved to {outfile}")

def write_combined_report(webcam_devices, webcam_procs, mic_devices, mic_procs, hardware_info, process_info, output_dir):
    # Combines all reports into a single JSON file with a timestamp.
    timestamp = datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")
    report = {
        "timestamp": timestamp,
        "webcams": webcam_devices,
        "webcam_processes": webcam_procs,
        "microphones": mic_devices,
        "mic_processes": mic_procs,
        "hardware_info": hardware_info,
        "process_info": process_info,
    }
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    outfile = output_dir / f"combined_report_{timestamp}.json"
    with open(outfile, "w") as f:
        json.dump(report, f, indent=2)
    print(f"Combined report saved to {outfile}")

def write_summary_report(webcam_devices, mic_devices, output_dir):
    # Writes a summary report of discovered webcams and microphones.

    timestamp = datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")
    report = {
        "timestamp": timestamp,
        "webcams": webcam_devices,
        "microphones": mic_devices,
    }
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    outfile = output_dir / f"summary_report_{timestamp}.json"
    with open(outfile, "w") as f:
        json.dump(report, f, indent=2)
    print(f"Summary report saved to {outfile}")

def write_device_report(devices, output_dir):
    # Writes a report of all discovered devices (webcams, microphones, etc.).
    timestamp = datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")
    report = {
        "timestamp": timestamp,
        "devices": devices,
    }
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    outfile = output_dir / f"device_report_{timestamp}.json"
    with open(outfile, "w") as f:
        json.dump(report, f, indent=2)
    print(f"Device report saved to {outfile}")

def write_process_audit_report(processes, output_dir):
    # Writes a report of processes using webcams and microphones.
    timestamp = datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")
    report = {
        "timestamp": timestamp,
        "processes": processes,
    }
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    outfile = output_dir / f"process_audit_report_{timestamp}.json"
    with open(outfile, "w") as f:
        json.dump(report, f, indent=2)
    print(f"Process audit report saved to {outfile}")

def write_combined_audit_report(webcam_devices, webcam_procs, mic_devices, mic_procs, hardware_info, process_info, output_dir):
    # Combines all audit reports into a single JSON file with a timestamp.
    timestamp = datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")
    report = {
        "timestamp": timestamp,
        "webcams": webcam_devices,
        "webcam_processes": webcam_procs,
        "microphones": mic_devices,
        "mic_processes": mic_procs,
        "hardware_info": hardware_info,
        "process_info": process_info,
    }
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    outfile = output_dir / f"combined_audit_report_{timestamp}.json"
    with open(outfile, "w") as f:
        json.dump(report, f, indent=2)
    print(f"Combined audit report saved to {outfile}")

def write_hardware_audit_report(hardware_info, output_dir):
    # Writes a report of hardware information (webcams, microphones, etc.) with a timestamp.
    timestamp = datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")
    report = {
        "timestamp": timestamp,
        "hardware_info": hardware_info,
    }
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    outfile = output_dir / f"hardware_audit_report_{timestamp}.json"
    with open(outfile, "w") as f:
        json.dump(report, f, indent=2)
    print(f"Hardware audit report saved to {outfile}")

def write_process_audit_summary(process_info, output_dir):
    # Writes a summary report of processes using webcams and microphones.
    timestamp = datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")
    report = {
        "timestamp": timestamp,
        "process_info": process_info,
    }
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    outfile = output_dir / f"process_audit_summary_{timestamp}.json"
    with open(outfile, "w") as f:
        json.dump(report, f, indent=2)
    print(f"Process audit summary saved to {outfile}")

def write_combined_audit_summary(webcam_devices, webcam_procs, mic_devices, mic_procs, hardware_info, process_info, output_dir):
    # Combines all audit summaries into a single JSON file with a timestamp.
    timestamp = datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")
    report = {
        "timestamp": timestamp,
        "webcams": webcam_devices,
        "webcam_processes": webcam_procs,
        "microphones": mic_devices,
        "mic_processes": mic_procs,
        "hardware_info": hardware_info,
        "process_info": process_info,
    }
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    outfile = output_dir / f"combined_audit_summary_{timestamp}.json"
    with open(outfile, "w") as f:
        json.dump(report, f, indent=2)
    print(f"Combined audit summary saved to {outfile}")

def write_device_audit_report(devices, output_dir):
    # Writes a report of all discovered devices (webcams, microphones, etc.) with a timestamp.
    timestamp = datetime.utcnow().strftime("%Y-%m-%d_%H:%M:%S")
    report = {
        "timestamp": timestamp,
        "devices": devices,
    }
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    outfile = output_dir / f"device_audit_report_{timestamp}.json"
    with open(outfile, "w") as f:
        json.dump(report, f, indent=2)
    print(f"Device audit report saved to {outfile}")

def main():
    # Example usage of the report writer functions
    webcam_devices = [{"device": "/dev/video0", "name": "Webcam 1", "platform": "linux"}]
    webcam_procs = [{"device": "/dev/video0", "pid": 1234, "cmdline": "webcam_app"}]
    mic_devices = [{"device": "/dev/snd/mic0", "name": "Microphone 1", "platform": "linux"}]
    mic_procs = [{"device": "/dev/snd/mic0", "pid": 5678, "cmdline": "mic_app"}]
    hardware_info = {"webcams": webcam_devices, "microphones": mic_devices}
    process_info = {"webcam_processes": webcam_procs, "mic_processes": mic_procs}
    
    output_dir = "./reports"
    
    write_audit_report(webcam_devices, webcam_procs, mic_devices, mic_procs, output_dir)
    #write_hardware_report(hardware_info, output_dir)
    #write_process_report(process_info, output_dir)
    #write_combined_report(webcam_devices, webcam_procs, mic_devices, mic_procs, hardware_info, process_info, output_dir)
    #write_summary_report(webcam_devices, mic_devices, output_dir)
    #write_device_report(webcam_devices + mic_devices, output_dir)
    #write_process_audit_report(webcam_procs + mic_procs, output_dir)
    #write_combined_audit_report(webcam_devices, webcam_procs, mic_devices, mic_procs, hardware_info, process_info, output_dir)
    #write_hardware_audit_report(hardware_info, output_dir)
    #write_process_audit_summary(process_info, output_dir)
    #write_combined_audit_summary(webcam_devices, webcam_procs, mic_devices, mic_procs, hardware_info, process_info, output_dir)
    #write_device_audit_report(webcam_devices + mic_devices, output_dir)