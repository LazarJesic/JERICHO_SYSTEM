"""
Path: src/SYS_WATCHDOG/schema.py
Description: Pydantic models for SYS_WATCHDOG validation.
Version: 2.1.0
Sub_System: SYS_WATCHDOG
System: JERICHO_SYSTEM
"""

from pydantic import BaseModel
from typing import Optional

class ProcessConfig(BaseModel):
    name: str
    start_command: Optional[str] = None

class Config(BaseModel):
    monitor_interval: int
    cpu_threshold: int
    memory_threshold: int
    disk_threshold: int
    slack_webhook: Optional[str]
    backup_schedule: str
    backup_retention_days: int
    backup_directory: str

class HealthStatus(BaseModel):
    status: str
    details: Optional[str] = None

class LogEntry(BaseModel):
    timestamp: str
    event_type: str
    message: str
