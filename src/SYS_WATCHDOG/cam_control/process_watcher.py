"""
Path: src/SYS_WATCHDOG/cam_control/process_watcher.py
Description: Monitors and restarts specific processes (fallback if monitor.py fails).
Version: 2.1.0
Sub_System: SYS_WATCHDOG
System: JERICHO_SYSTEM
"""

import psutil
import subprocess


def ensure_running(process_name: str, start_command: str):
    """Restart process if not running."""
    if not any(p.info['name'] == process_name for p in psutil.process_iter(['name'])):
        try:
            subprocess.Popen(start_command.split())
        except Exception as e:
            raise RuntimeError(f"Failed to restart {process_name}: {e}")
