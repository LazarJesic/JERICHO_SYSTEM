"""
Path: src/sys_surveillance_cam/main.py
Description: Entry point for launching all camera configurations and handlers.
Version: 1.0.2
Sub_System: SYS_SURVEILLANCE_CAM
System: JERICHO_SYSTEM
"""
from src.sys_surveillance_cam.src.config_loader import load_all_camera_configs
from src.sys_surveillance_cam.src.camera import CameraHandler
from loguru import logger
import threading


def launch_all_cameras():
    """
    Loads all camera configs and starts a CameraHandler thread for each.
    """
    configs = load_all_camera_configs()
    threads = []

    for config in configs:
        try:
            handler = CameraHandler(config)
            t = threading.Thread(target=handler.run, daemon=True)
            t.start()
            threads.append(t)
            logger.info(f"Camera {config['camera_id']} started successfully.")
        except Exception as e:
            logger.exception(f"Failed to start camera {config.get('camera_id', '?')}: {e}")

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    launch_all_cameras()
