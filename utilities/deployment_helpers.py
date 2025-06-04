"""
Path: utilities/deployment_helpers.py
Description: Helpers for CI/CD, environment validation, and migrations.
Version: 2.1.0
Sub_System: UTILITIES
System: JERICHO_SYSTEM
"""

import os
import subprocess


def ensure_environment_vars(vars_list):
    """Verify that required environment variables are defined."""
    missing = [v for v in vars_list if v not in os.environ]
    if missing:
        raise EnvironmentError(f"Missing environment variables: {', '.join(missing)}")


def run_migrations():
    """Run Alembic migrations (requires alembic.ini in db/)."""
    subprocess.run(["alembic", "upgrade", "head"], check=True)
