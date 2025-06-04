"""
Path: src/SYS_WATCHDOG/src/metrics.py
Description: Prometheus metrics exposition.
Version: 2.1.0
Sub_System: SYS_WATCHDOG
System: JERICHO_SYSTEM
"""

from prometheus_client import Gauge, start_http_server
import psutil
import threading
import time

from .config_loader import get_config

CPU_GAUGE = Gauge('sys_cpu_percent', 'CPU usage percent')
MEM_GAUGE = Gauge('sys_memory_percent', 'Memory usage percent')
DISK_GAUGE = Gauge('sys_disk_percent', 'Disk usage percent')


def _collect_loop(interval: int):
    while True:
        CPU_GAUGE.set(psutil.cpu_percent())
        MEM_GAUGE.set(psutil.virtual_memory().percent)
        DISK_GAUGE.set(psutil.disk_usage('/').percent)
        time.sleep(interval)


def start_metrics_server():
    cfg = get_config()
    port = cfg.get('metrics_port', 9000)
    start_http_server(port)
    thread = threading.Thread(target=_collect_loop, args=(cfg.get('monitor_interval', 30),), daemon=True)
    thread.start()
