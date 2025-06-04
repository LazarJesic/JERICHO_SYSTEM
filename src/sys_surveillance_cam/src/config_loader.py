"""
Path: src/sys_surveillance_cam/src/config_loader.py
Description: Validates and loads all YAML camera configurations.
Version: 1.0.2
Sub_System: SYS_SURVEILLANCE_CAM
System: JERICHO_SYSTEM
"""
import yaml
from pathlib import Path
from loguru import logger
from src.sys_surveillance_cam.src.exceptions import InvalidConfigError

def get_config_dir() -> Path:
    """Return the directory containing camera config files."""
    candidates = [
        Path("config/sys_surveillance_cam"),
        Path("sys_surveillance_cam"),
    ]
    for c in candidates:
        if c.exists():
            return c
    for p in Path(".").rglob("sys_surveillance_cam"):
        if p.is_dir() and any(p.glob("*.yaml")):
            return p
    return candidates[0]


def load_camera_config(file_path: Path) -> dict:
    """
    Loads and validates a single YAML config file.

    Args:
        file_path (Path): Path to the YAML config.

    Returns:
        dict: Parsed and validated configuration.

    Raises:
        InvalidConfigError: If required fields are missing or YAML is invalid.
    """
    try:
        data = yaml.safe_load(file_path.read_text())
    except yaml.YAMLError as exc:
        raise InvalidConfigError(f"YAML error in {file_path}: {exc}")

    required = {"camera_id", "source", "frame_width", "frame_height", "fps", "codec"}
    missing = required - data.keys() if isinstance(data, dict) else required
    if missing:
        raise InvalidConfigError(f"Missing fields {missing} in {file_path}")

    return data


def load_all_camera_configs() -> list:
    """
    Iterates over CONFIG_DIR to load and validate all camera YAMLs.

    Returns:
        List[dict]: List of valid camera configurations.
    """
    cfg_dir = get_config_dir()
    configs = []
    for file in cfg_dir.glob("*.yaml"):
        try:
            configs.append(load_camera_config(file))
        except InvalidConfigError as e:
            logger.error(str(e))
    return configs
