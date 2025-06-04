"""
Path: src/SYS_WATCHDOG/src/health.py
Description: Health check utilities (liveness/readiness probes).
Version: 2.1.0
Sub_System: SYS_WATCHDOG
System: JERICHO_SYSTEM
"""

from fastapi import Response, HTTPException
from sqlalchemy import text

from .database import engine


def check_db():
    """Attempts a simple DB query to verify connectivity."""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception:
        return False


def liveness_probe():
    """Always returns 200 if app is running."""
    return Response(content="OK", status_code=200)


def readiness_probe():
    """Returns 200 if DB is reachable, else 503."""
    if check_db():
        return Response(content="Ready", status_code=200)
    else:
        raise HTTPException(status_code=503, detail="Database unreachable")
