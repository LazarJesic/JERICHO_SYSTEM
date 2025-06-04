"""
Path: src/SYS_WATCHDOG/main.py
Description: Entry point – orchestrates monitoring, observability, and backup scheduling.
Version: 2.1.0
Sub_System: SYS_WATCHDOG
System: JERICHO_SYSTEM
"""

import asyncio
import logging
import json
import subprocess
from fastapi import FastAPI
from uvicorn import run as uvicorn_run

from .config_loader import load_env, get_config
from .database import init_db, get_db, Log
from .monitor import check_metrics, check_processes_from_config
from .metrics import start_metrics_server
from .alert import send_alert
from .constants import STATUS_OK, STATUS_ALERT
from .router import router

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

cfg = get_config()
logging.basicConfig(
    level=cfg.get("log_level", "INFO"),
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[logging.FileHandler("logs/watchdog.log"), logging.StreamHandler()]
)

app = FastAPI(title="SYS_WATCHDOG API")
app.include_router(router)

async def run_once():
    """One cycle of collecting metrics, checking processes, and logging to DB/alerts."""
    init_db()
    env = load_env()
    issues = await check_metrics()
    proc_restarts = await check_processes_from_config()
    status = STATUS_ALERT if issues or proc_restarts else STATUS_OK
    message_obj = {"issues": issues, "restarts": proc_restarts} if (issues or proc_restarts) else {"ok": True}
    message = json.dumps(message_obj)

    try:
        db = next(get_db())
        new_log = Log(event_type=status, message=message)
        db.add(new_log)
        db.commit()
    except Exception as e:
        logging.error(f"DB write failed: {e}")
    finally:
        db.close()

    if status == STATUS_ALERT:
        subject = "SYS_WATCHDOG Alert"
        body = "\n".join(issues + proc_restarts)
        await send_alert(subject, body)

async def scheduled_backup():
    """Invoke the backup script from scripts/backup_db.sh."""
    try:
        logging.info("Running automated backup...")
        subprocess.run(["scripts/backup_db.sh"], check=True)
    except Exception as e:
        logging.error(f"Backup failed: {e}")

async def main_loop():
    """Set up observability (metrics + health), scheduler, then loop."""
    start_metrics_server()
    logging.info("Prometheus metrics server started.")

    scheduler = AsyncIOScheduler()
    cfg = get_config()
    backup_cron = cfg.get("backup_schedule", "0 * * * *")
    trigger = CronTrigger.from_crontab(backup_cron)
    scheduler.add_job(scheduled_backup, trigger)
    scheduler.start()
    logging.info(f"Backup scheduled: {backup_cron}")

    cfg = get_config()
    interval = cfg.get("monitor_interval", 30)
    while True:
        try:
            await run_once()
        except Exception as e:
            logging.exception(f"Monitoring iteration failed: {e}")
        await asyncio.sleep(interval)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(main_loop())
    uvicorn_run("SYS_WATCHDOG.main:app", host="0.0.0.0", port=8000, log_level="info")
