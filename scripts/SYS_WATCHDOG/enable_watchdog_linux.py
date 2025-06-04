"""
Path: scripts/SYS_WATCHDOG/enable_watchdog_linux.py
Description: Enables Linux services for SYS_WATCHDOG (stub).
Version: 2.1.0
Sub_System: SYS_WATCHDOG
System: JERICHO_SYSTEM
"""

import os


def enable_service(service_name: str):
    os.system(f"systemctl start {service_name}")
