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
from src.sys_surveillance_cam.exceptions import InvalidConfigError

CONFIG_DIR = Path("config/sys_surveillance_cam")


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
    configs = []
    for file in CONFIG_DIR.glob("*.yaml"):
        try:
            configs.append(load_camera_config(file))
        except InvalidConfigError as e:
            logger.error(str(e))
    return configs
