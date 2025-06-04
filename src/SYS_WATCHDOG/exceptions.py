"""
Path: src/SYS_WATCHDOG/exceptions.py
Description: Custom exceptions for SYS_WATCHDOG.
Version: 2.1.0
Sub_System: SYS_WATCHDOG
System: JERICHO_SYSTEM
"""

class ConfigError(Exception):
    """Raised when configuration is missing or invalid."""

class DatabaseError(Exception):
    """Raised for database connection or ORM errors."""

class AlertError(Exception):
    """Raised when email or Slack alert fails."""
