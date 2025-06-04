"""
Path: tests/SYS_WATCHDOG/test_config_loader.py
Description: Tests for config_loader (YAML + Vault integration).
Version: 2.1.0
Sub_System: SYS_WATCHDOG
System: JERICHO_SYSTEM
"""

import os
import pytest
from src.SYS_WATCHDOG.src.config_loader import load_env, load_processes_config, ConfigError


def test_missing_config_yaml(tmp_path, monkeypatch):
    cfg_dir = tmp_path / "config" / "SYS_WATCHDOG"
    cfg_dir.mkdir(parents=True, exist_ok=True)
    monkeypatch.chdir(tmp_path)
    with pytest.raises(ConfigError):
        load_env()


def test_load_processes(monkeypatch, tmp_path):
    cfg_dir = tmp_path / "config" / "SYS_WATCHDOG"
    cfg_dir.mkdir(parents=True, exist_ok=True)
    processes = [{"name": "proc", "start_command": "echo start"}]
    import json
    with open(cfg_dir / "processes.json", "w") as f:
        json.dump(processes, f)
    monkeypatch.chdir(tmp_path)
    loaded = load_processes_config()
    assert loaded == processes
