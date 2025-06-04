"""
Path: src/SYS_WATCHDOG/src/monitor.py
Description: Async resource and process monitoring checks.
Version: 2.1.0
Sub_System: SYS_WATCHDOG
System: JERICHO_SYSTEM
"""

import asyncio
import psutil
import subprocess

from .config_loader import get_config, load_processes_config
from .event_logger import log_event


async def check_metrics():
    """Check system resource usage against thresholds."""
    issues = []
    cfg = get_config()
    cpu = psutil.cpu_percent()
    if cpu > cfg.get('cpu_threshold', 85):
        issues.append(f'CPU {cpu}%')
    mem = psutil.virtual_memory().percent
    if mem > cfg.get('memory_threshold', 85):
        issues.append(f'Memory {mem}%')
    disk = psutil.disk_usage('/').percent
    if disk > cfg.get('disk_threshold', 90):
        issues.append(f'Disk {disk}%')
    if issues:
        log_event('RESOURCE_ALERT', {'issues': issues})
    return issues


async def check_processes_from_config():
    """Ensure configured processes are running; restart if necessary."""
    restarts = []
    processes = load_processes_config()
    for proc in processes:
        name = proc.get('name')
        cmd = proc.get('start_command')
        if not any(p.info['name'] == name for p in psutil.process_iter(['name'])):
            if cmd:
                try:
                    subprocess.Popen(cmd.split())
                    restarts.append(name)
                except Exception:
                    restarts.append(name)
    if restarts:
        log_event('PROC_RESTART', {'processes': restarts})
    return restarts
