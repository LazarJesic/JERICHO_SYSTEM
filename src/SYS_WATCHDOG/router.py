"""
Path: src/SYS_WATCHDOG/router.py
Description: FastAPI router for SYS_WATCHDOG endpoints.
Version: 2.1.0
Sub_System: SYS_WATCHDOG
System: JERICHO_SYSTEM
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .schema import HealthStatus, LogEntry
from .database import get_db, Log

router = APIRouter()

@router.get("/healthz", response_model=HealthStatus)
async def health_check(db: Session = Depends(get_db)):
    try:
        db.execute("SELECT 1")
        return HealthStatus(status="healthy")
    except Exception:
        raise HTTPException(status_code=500, detail="Database unreachable")

@router.get("/logs", response_model=List[LogEntry])
async def get_logs(limit: int = 100, db: Session = Depends(get_db)):
    rows = db.query(Log).order_by(Log.timestamp.desc()).limit(limit).all()
    return [LogEntry(timestamp=r.timestamp.isoformat(),
                     event_type=r.event_type,
                     message=r.message)
            for r in rows]
