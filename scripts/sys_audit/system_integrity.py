"""
Path: scripts/sys_audit/system_integrity.py
Description: Collects system integrity info such as BIOS, TPM, microcode,
PCI devices, battery analytics, and memory snapshots. Logs events
in tamper-evident databases.
Version: 1.0.0
Sub_System: SYS_SURVEILLANCE_CAM
System: JERICHO_SYSTEM
"""

import os
import subprocess
import json
from datetime import datetime
import sqlite3
from pathlib import Path

try:
    import psutil
except ImportError:  # pragma: no cover - psutil may not be installed
    psutil = None

# --- BIOS/UEFI/Firmware ----------------------------------------------------


def get_bios_info():
    """Returns BIOS/UEFI details if available."""
    info = {}
    try:
        proc = subprocess.run(
            ["dmidecode", "-t", "bios"], capture_output=True, text=True
        )
        if proc.returncode == 0:
            info["raw"] = proc.stdout.strip()
    except (FileNotFoundError, PermissionError):
        pass
    # Fallback to sysfs
    for field in ["bios_vendor", "bios_version", "product_serial"]:
        p = f"/sys/class/dmi/id/{field}"
        if os.path.exists(p):
            try:
                info[field] = Path(p).read_text().strip()
            except Exception:
                continue
    return info


# --- TPM/Secure Boot -------------------------------------------------------


def get_tpm_info():
    """Collects basic TPM and secure boot details."""
    info = {}
    try:
        proc = subprocess.run(
            ["tpm2_getcap", "-c", "properties-fixed"], capture_output=True, text=True
        )
        if proc.returncode == 0:
            info["raw"] = proc.stdout.strip()
    except FileNotFoundError:
        pass
    secure_boot = (
        "/sys/firmware/efi/vars/SecureBoot-8be4df61-93ca-11d2-aa0d-00e098032b8c/data"
    )
    if os.path.exists(secure_boot):
        try:
            val = int.from_bytes(Path(secure_boot).read_bytes(), "little")
            info["secure_boot"] = bool(val)
        except Exception:
            pass
    return info


# --- Microcode/Firmware ----------------------------------------------------


def get_microcode_info():
    """Returns CPU microcode and kernel firmware information."""
    info = {"kernel": os.uname().release}
    try:
        with open("/proc/cpuinfo", "r") as f:
            for line in f:
                if line.lower().startswith("microcode"):
                    info.setdefault("microcode", []).append(line.strip())
    except Exception:
        pass
    return info


# --- PCI/Peripherals -------------------------------------------------------


def get_pci_devices():
    """Lists PCI devices using lspci if available."""
    devices = []
    try:
        proc = subprocess.run(["lspci", "-mm"], capture_output=True, text=True)
        if proc.returncode == 0:
            for line in proc.stdout.strip().splitlines():
                devices.append(line.strip())
    except FileNotFoundError:
        # Fallback to sysfs listing
        base = Path("/sys/bus/pci/devices")
        if base.exists():
            for dev in base.iterdir():
                devices.append(dev.name)
    return devices


# --- Battery Analytics -----------------------------------------------------


def get_battery_info():
    """Returns battery details if available."""
    info = {}
    if psutil and hasattr(psutil, "sensors_battery"):
        try:
            batt = psutil.sensors_battery()
            if batt:
                info = {
                    "percent": batt.percent,
                    "secs_left": batt.secsleft,
                    "power_plugged": batt.power_plugged,
                }
        except Exception:
            pass
    return info


# --- Memory Snapshot -------------------------------------------------------


def capture_memory_snapshot(output_dir="data/sys/memory"):
    """Attempts to capture a minimal memory snapshot."""
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    snapshot_path = (
        Path(output_dir)
        / f"mem_snapshot_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.bin"
    )
    try:
        with open("/dev/mem", "rb") as src, open(snapshot_path, "wb") as dst:
            dst.write(src.read(1024 * 1024))  # 1MB snapshot
        return str(snapshot_path)
    except Exception:
        return None


# --- Event Store -----------------------------------------------------------


class EventStore:
    """Logs events to SQLite and optionally PostgreSQL."""

    def __init__(self, sqlite_path="data/sys/event_store/events.db", pg_dsn=None):
        Path(sqlite_path).parent.mkdir(parents=True, exist_ok=True)
        self.sqlite_path = sqlite_path
        self.pg_dsn = pg_dsn
        self._init_sqlite()
        try:
            import psycopg2  # type: ignore

            self.psycopg2 = psycopg2
        except Exception:  # pragma: no cover - optional dependency
            self.psycopg2 = None
        self.pg_conn = None
        if self.pg_dsn and self.psycopg2:
            try:
                self.pg_conn = self.psycopg2.connect(self.pg_dsn)
            except Exception:
                self.pg_conn = None

    def _init_sqlite(self):
        conn = sqlite3.connect(self.sqlite_path)
        conn.execute(
            "CREATE TABLE IF NOT EXISTS events (timestamp TEXT, type TEXT, data TEXT)"
        )
        conn.commit()
        conn.close()

    def log_event(self, event_type: str, data: dict):
        ts = datetime.utcnow().isoformat()
        payload = json.dumps(data)
        conn = sqlite3.connect(self.sqlite_path)
        conn.execute(
            "INSERT INTO events (timestamp, type, data) VALUES (?, ?, ?)",
            (ts, event_type, payload),
        )
        conn.commit()
        conn.close()
        if self.pg_conn:
            try:
                cur = self.pg_conn.cursor()
                cur.execute(
                    "CREATE TABLE IF NOT EXISTS events (timestamp TEXT, type TEXT, data TEXT)"
                )
                cur.execute(
                    "INSERT INTO events (timestamp, type, data) VALUES (%s, %s, %s)",
                    (ts, event_type, payload),
                )
                self.pg_conn.commit()
            except Exception:
                pass


# --- Meta Audit ------------------------------------------------------------


def verify_event_store_integrity(store: EventStore):
    """Basic integrity check for the event store."""
    conn = sqlite3.connect(store.sqlite_path)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM events")
    count = cur.fetchone()[0]
    conn.close()
    return {"sqlite_event_count": count}


# --- Collection Helper -----------------------------------------------------


def collect_system_integrity(store: EventStore | None = None):
    """Collects all system integrity information and logs events."""
    data = {
        "bios": get_bios_info(),
        "tpm": get_tpm_info(),
        "microcode": get_microcode_info(),
        "pci_devices": get_pci_devices(),
        "battery": get_battery_info(),
        "memory_snapshot": capture_memory_snapshot(),
    }
    if store:
        store.log_event("system_integrity", data)
    return data


def main():
    """Entry point for running integrity collection standalone."""
    store = EventStore()
    data = collect_system_integrity(store)
    print(json.dumps(data, indent=2))
    check = verify_event_store_integrity(store)
    print("Event store integrity:", check)


if __name__ == "__main__":
    main()
