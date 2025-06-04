"""
Path: scripts/sys_audit/audit_entrypoint.py
Description: Main entrypoint to perform hardware discovery, process auditing, and report writing.
Version: 1.0.0
Sub_System: SYS_SURVEILLANCE_CAM
System: JERICHO_SYSTEM
"""
from hardware_discovery import discover_webcams, discover_microphones
from process_audit import audit_webcam_processes, audit_mic_processes
from system_integrity import EventStore, collect_system_integrity, verify_event_store_integrity
from report_writer import (
    write_audit_report,
    write_hardware_report,
    write_process_report,
    write_combined_report,
    write_integrity_report,
)
import sys


def main():
    webcam_devices = discover_webcams()
    mic_devices = discover_microphones()
    webcam_procs = audit_webcam_processes(webcam_devices)
    mic_procs = audit_mic_processes(mic_devices)
    store = EventStore()
    integrity_data = collect_system_integrity(store)
    integrity_check = verify_event_store_integrity(store)
    write_audit_report(
        webcam_devices, webcam_procs, mic_devices, mic_procs,
        output_dir="data/sys/audit"
    )
    write_hardware_report(
        {"webcams": webcam_devices, "microphones": mic_devices},
        output_dir="data/sys/hardware"
    )
    write_process_report(
        {"webcam_processes": webcam_procs, "mic_processes": mic_procs},
        output_dir="data/sys/processes"
    )
    write_combined_report(
        webcam_devices, webcam_procs, mic_devices, mic_procs,
        {"webcams": webcam_devices, "microphones": mic_devices},
        {"webcam_processes": webcam_procs, "mic_processes": mic_procs},
        output_dir="data/sys/combined"
    )
    write_integrity_report(
        {"integrity": integrity_data, "event_store": integrity_check},
        output_dir="data/sys/integrity",
    )
    print("System audit completed successfully.")
    sys.exit(0)

if __name__ == "__main__":
    main()
