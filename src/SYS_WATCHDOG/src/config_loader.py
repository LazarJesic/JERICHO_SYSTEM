"""
Path: src/SYS_WATCHDOG/src/config_loader.py
Description: Loads .env, Vault secrets, and YAML configuration for SYS_WATCHDOG.
Version: 2.1.0
Sub_System: SYS_WATCHDOG
System: JERICHO_SYSTEM
"""

import os
from pathlib import Path

import hvac
import yaml
from dotenv import load_dotenv

from ..exceptions import ConfigError

CONFIG = None
SECRETS = {}


def _cfg_path() -> Path:
    """Return path to YAML config, defaulting to CWD."""
    env_path = os.getenv("WATCHDOG_CONFIG")
    if env_path:
        return Path(env_path)
    return Path.cwd() / "config" / "SYS_WATCHDOG" / "config.yaml"


def _env_path() -> Path:
    return Path.cwd() / "SYS_WATCHDOG" / ".env"


# Load .env if present
ENV_FILE = _env_path()
if ENV_FILE.exists():
    load_dotenv(ENV_FILE)


def load_config() -> dict:
    """Load YAML configuration, raising ConfigError if missing."""
    global CONFIG
    cfg = _cfg_path()
    if not cfg.exists():
        raise ConfigError(f"Missing configuration file: {cfg}")
    with open(cfg, "r") as fh:
        CONFIG = yaml.safe_load(fh)
    return CONFIG


def get_config() -> dict:
    """Return configuration, reloading from disk each call."""
    return load_config()


def _load_secrets(config: dict) -> dict:
    vault_addr = os.getenv("VAULT_ADDR", config.get("vault_address"))
    vault_token = os.getenv("VAULT_TOKEN")
    secrets: dict = {}
    if vault_addr and vault_token:
        try:
            client = hvac.Client(url=vault_addr, token=vault_token)
            secret = client.secrets.kv.v2.read_secret_version(path="sys_watchdog")
            secrets = secret["data"]["data"]
        except Exception as exc:
            raise ConfigError(f"Vault secret retrieval failed: {exc}") from exc
    return secrets


def load_env() -> dict:
    """Return environment and Vault-derived settings."""
    env_file = _env_path()
    if env_file.exists():
        load_dotenv(env_file)

    config = get_config()
    global SECRETS
    if not SECRETS:
        SECRETS = _load_secrets(config)

    env = {
        "DB_URL": SECRETS.get("db_url") or os.getenv("DB_URL"),
        "SMTP_USER": SECRETS.get("smtp_user") or os.getenv("SMTP_USER"),
        "SMTP_PASS": SECRETS.get("smtp_pass") or os.getenv("SMTP_PASS"),
        "SMTP_HOST": SECRETS.get("smtp_host") or os.getenv("SMTP_HOST"),
        "SMTP_PORT": int(SECRETS.get("smtp_port") or os.getenv("SMTP_PORT", 587)),
        "ALERT_EMAIL": SECRETS.get("alert_email") or os.getenv("ALERT_EMAIL"),
        "LOG_LEVEL": os.getenv("LOG_LEVEL", "INFO"),
    }
    return env

def load_processes_config() -> list:
    """Load optional processes configuration from CWD."""
    proc_path = Path.cwd() / "config" / "SYS_WATCHDOG" / "processes.json"
    if not proc_path.exists():
        return []
    with open(proc_path, "r") as f:
        return yaml.safe_load(f)
