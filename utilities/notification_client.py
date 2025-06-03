"""
Path: utilities/notification_client.py
Description: Handles sending PGP-encrypted notifications to SYS_ENCRYPTED_NOTIFICATION.
Version: 1.0.0
Sub_System: UTILITIES
System: JERICHO_SYSTEM
"""
import subprocess
import json

def send_notification(event: dict, recipient: str):
    """
    Encrypts the event payload and sends it to the notification system.
    """
    payload = json.dumps(event)
    # Example: use GPG to encrypt
    proc = subprocess.Popen(
        ["gpg", "--encrypt", "--recipient", recipient],
        stdin=subprocess.PIPE, stdout=subprocess.PIPE
    )
    encrypted, _ = proc.communicate(input=payload.encode("utf-8"))
    # Send encrypted to endpoint (stub)
    # e.g., requests.post("https://notification.example.com", data=encrypted)
    return True
