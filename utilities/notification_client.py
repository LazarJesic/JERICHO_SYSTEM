"""
Path: utilities/notification_client.py
Description: PGP-signed Slack and Email notification client.
Version: 2.1.0
Sub_System: UTILITIES
System: JERICHO_SYSTEM
"""

import smtplib
import httpx
from email.mime.text import MIMEText
from gnupg import GPG
import os


class NotificationClient:
    """Sends PGP-signed messages to Slack and Email."""

    def __init__(self, smtp_host, smtp_port, smtp_user, smtp_pass, gpg_home=None):
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.smtp_user = smtp_user
        self.smtp_pass = smtp_pass
        self.gpg = GPG(gnupghome=gpg_home) if gpg_home else GPG()
        self.slack_webhook = os.getenv("SLACK_WEBHOOK")

    def sign_message(self, message: str, key_fingerprint: str) -> str:
        signed_data = self.gpg.sign(message, keyid=key_fingerprint)
        return str(signed_data)

    def send_email(self, subject: str, message: str, recipient: str, key_fingerprint: str):
        signed = self.sign_message(message, key_fingerprint)
        msg = MIMEText(signed)
        msg["Subject"] = subject
        msg["From"] = self.smtp_user
        msg["To"] = recipient
        with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
            server.starttls()
            server.login(self.smtp_user, self.smtp_pass)
            server.send_message(msg)

    async def send_slack(self, body: str, key_fingerprint: str):
        if not self.slack_webhook:
            return
        signed = self.sign_message(body, key_fingerprint)
        async with httpx.AsyncClient() as client:
            await client.post(self.slack_webhook, json={"text": signed})
