"""
Path: utilities/deployment_helpers.py
Description: Helper functions for Docker builds, CI/CD, and environment setup.
Version: 1.0.0
Sub_System: UTILITIES
System: JERICHO_SYSTEM
"""
import os
import subprocess

def build_docker_image(subsys: str):
    """
    Builds a Docker image for the given subsystem.
    """
    image_tag = f"jericho_{subsys.lower()}:latest"
    subprocess.run(["docker", "build", "-t", image_tag, "."], check=True)
    return image_tag

def run_subsys_container(subsys: str):
    """
    Runs the subsystem in a Docker container.
    """
    image_tag = build_docker_image(subsys)
    container_name = f"jericho_{subsys.lower()}"
    subprocess.run(["docker", "run", "--rm", "--name", container_name, image_tag], check=True)
