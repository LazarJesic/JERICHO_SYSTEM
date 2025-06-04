# SYS_WATCHDOG v2.1 (Subsystem of SYSTEM_JERICHO)

**SYS_WATCHDOG** monitors system resources (CPU, Memory, Disk), watches specific processes, sends multi-channel alerts (Email + Slack), logs events to PostgreSQL, exposes Prometheus metrics, and performs automated backups. Version 2.1 adds observability, security integrations, and backup scheduling.

---

## Folder Structure

SYS_WATCHDOG/
├── config/
│   ├── config.yaml
│   └── processes.json
├── scripts/
│   ├── deploy.sh
│   └── backup_db.sh
├── src/
│   ├── SYS_WATCHDOG/
│   │   ├── __init__.py
│   │   ├── constants.py
│   │   ├── exceptions.py
│   │   ├── schema.py
│   │   ├── router.py
│   │   ├── main.py
│   │   ├── monitor.py
│   │   ├── metrics.py
│   │   ├── alert.py
│   │   ├── database.py
│   │   ├── utils.py
│   │   └── health.py
│   ├── movement_detection/
│   │   └── anomaly_detector.py
│   ├── cam_control/
│   │   └── process_watcher.py
└── tests/
    ├── test_config_loader.py
    ├── test_monitor.py
    ├── test_event_logger.py
    └── test_database.py

---

## Quick Start (Docker)

1. **Clone the repo**:
   ```bash
   git clone <repo_url> SYSTEM_JERICHO
   cd SYSTEM_JERICHO/SYS_WATCHDOG
   ```
2. Copy & edit `.env`:
   ```bash
   cp .env.template .env
   # Edit DB_URL, SMTP credentials, Vault settings, etc.
   ```
3. Deploy containers:
   ```bash
   chmod +x scripts/deploy.sh
   ./scripts/deploy.sh
   ```
This brings up Postgres (with automated backups) and the SYS_WATCHDOG service (metrics on port 9000, API on port 8000).

Monitor logs:
```bash
tail -f logs/watchdog.log
```

Access endpoints:

* Health: http://localhost:8000/healthz
* Logs: http://localhost:8000/logs
* Metrics: http://localhost:9000/metrics

### Configuration
- `config/config.yaml`: Adjust thresholds, observability ports, Vault address/token, backup schedule/retention, Slack webhook.
- `.env`: Populate DB_URL, SMTP_USER, SMTP_PASS, SMTP_HOST, SMTP_PORT, ALERT_EMAIL, LOG_LEVEL, and optionally VAULT_ADDR, VAULT_TOKEN.

### Testing
Run all tests with:
```bash
pytest src/tests/SYS_WATCHDOG
```

### CI/CD & Deployment
- **CodeAudit++**: Ensures code quality and security scans.
- **JerichoFormat**: Enforces folder structure and standardized headers.
- **DeployReady**: Confirms production readiness (Docker, backups, observability).
- **SysEmbed**: Keeps cross-chat augmentation for continuous improvement.
