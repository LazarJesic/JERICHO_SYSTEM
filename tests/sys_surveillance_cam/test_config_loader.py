"""
Path: tests/sys_surveillance_cam/test_config_loader.py
Description: Unit tests for config_loader module.
Version: 1.0.2
Sub_System: SYS_SURVEILLANCE_CAM
System: JERICHO_SYSTEM
"""

import yaml
import pytest
from src.sys_surveillance_cam.src.config_loader import (
    load_camera_config,
    load_all_camera_configs,
)


@pytest.fixture
def tmp_config_dir(tmp_path, monkeypatch):
    cfg_dir = tmp_path / "sys_surveillance_cam"
    cfg_dir.mkdir(parents=True)
    monkeypatch.chdir(tmp_path.parent)  # ensure config path is relative
    return cfg_dir


def test_load_valid_config(tmp_config_dir):
    cfg_file = tmp_config_dir / "camera1.yaml"
    content = {
        "camera_id": "cam1",
        "source": 0,
        "frame_width": 640,
        "frame_height": 480,
        "fps": 20,
        "codec": "mp4v",
    }
    cfg_file.write_text(yaml.dump(content))
    cfg = load_camera_config(cfg_file)
    assert cfg["camera_id"] == "cam1"


def test_load_all_camera_configs_skips_invalid(tmp_config_dir):
    valid = tmp_config_dir / "valid.yaml"
    invalid = tmp_config_dir / "invalid.yaml"
    valid.write_text(
        yaml.dump(
            {
                "camera_id": "cam1",
                "source": 0,
                "frame_width": 640,
                "frame_height": 480,
                "fps": 20,
                "codec": "mp4v",
            }
        )
    )
    invalid.write_text("not: valid: yaml")
    configs = load_all_camera_configs()
    assert len(configs) == 1
