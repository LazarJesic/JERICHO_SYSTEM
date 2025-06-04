"""
Path: tests/SYS_WATCHDOG/test_monitor.py
Description: Unit tests for monitor (async resource/process checks).
Version: 2.1.0
Sub_System: SYS_WATCHDOG
System: JERICHO_SYSTEM
"""

import pytest
import psutil
from src.SYS_WATCHDOG.src.monitor import check_metrics, check_processes_from_config


class DummyHigh:
    @staticmethod
    def cpu_percent(interval=None):
        return 90

    @staticmethod
    def virtual_memory():
        return type('vm', (), {'percent': 90})()

    @staticmethod
    def disk_usage(path):
        return type('du', (), {'percent': 95})()


class DummyLow:
    @staticmethod
    def cpu_percent(interval=None):
        return 10

    @staticmethod
    def virtual_memory():
        return type('vm', (), {'percent': 10})()

    @staticmethod
    def disk_usage(path):
        return type('du', (), {'percent': 10})()


@pytest.mark.asyncio
async def test_metrics_alert(monkeypatch):
    monkeypatch.setattr(psutil, 'cpu_percent', DummyHigh.cpu_percent)
    monkeypatch.setattr(psutil, 'virtual_memory', DummyHigh.virtual_memory)
    monkeypatch.setattr(psutil, 'disk_usage', DummyHigh.disk_usage)
    issues = await check_metrics()
    assert len(issues) == 3


@pytest.mark.asyncio
async def test_metrics_ok(monkeypatch):
    monkeypatch.setattr(psutil, 'cpu_percent', DummyLow.cpu_percent)
    monkeypatch.setattr(psutil, 'virtual_memory', DummyLow.virtual_memory)
    monkeypatch.setattr(psutil, 'disk_usage', DummyLow.disk_usage)
    issues = await check_metrics()
    assert issues == []
