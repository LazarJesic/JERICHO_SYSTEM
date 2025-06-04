"""
Path: src/SYS_WATCHDOG/src/alert.py
Description: Email and Slack alerting utilities.
Version: 2.1.0
Sub_System: SYS_WATCHDOG
System: JERICHO_SYSTEM
"""

import asyncio
from .config_loader import load_env
from utilities.notification_client import NotificationClient


env_cache = None


def _get_client() -> NotificationClient:
    global env_cache
    if env_cache is None:
        env_cache = load_env()
    return NotificationClient(
        env_cache['SMTP_HOST'],
        env_cache['SMTP_PORT'],
        env_cache['SMTP_USER'],
        env_cache['SMTP_PASS'],
    )


async def send_alert(subject: str, body: str):
    client = _get_client()
    recipient = env_cache.get('ALERT_EMAIL')
    if not recipient:
        return
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, client.send_email, subject, body, recipient, None)
    await client.send_slack(body, None)
