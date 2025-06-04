"""
Path: scripts/SYS_WATCHDOG/enable_watchdog_windows.py
Description: Enables Windows services for SYS_WATCHDOG (stub).
Version: 2.1.0
Sub_System: SYS_WATCHDOG
System: JERICHO_SYSTEM
"""

import subprocess


def enable_service(service_name: str):
    subprocess.run(["sc", "start", service_name], check=False)
