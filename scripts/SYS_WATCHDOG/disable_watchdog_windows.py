"""
Path: scripts/SYS_WATCHDOG/disable_watchdog_windows.py
Description: Disables Windows services for SYS_WATCHDOG (stub).
Version: 2.1.0
Sub_System: SYS_WATCHDOG
System: JERICHO_SYSTEM
"""

import subprocess


def disable_service(service_name: str):
    subprocess.run(["sc", "stop", service_name], check=False)
