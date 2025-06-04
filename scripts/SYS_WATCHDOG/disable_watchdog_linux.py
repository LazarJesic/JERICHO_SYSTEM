"""
Path: scripts/SYS_WATCHDOG/disable_watchdog_linux.py
Description: Disables Linux services for SYS_WATCHDOG (stub).
Version: 2.1.0
Sub_System: SYS_WATCHDOG
System: JERICHO_SYSTEM
"""

import os


def disable_service(service_name: str):
    os.system(f"systemctl stop {service_name}")
