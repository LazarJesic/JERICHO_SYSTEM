#!/usr/bin/env bash
# Path: scripts/SYS_WATCHDOG/backup_db.sh
# Description: Automated backup script for PostgreSQL; invoked by APScheduler hourly.
# Version: 2.1.0
# Sub_System: SYS_WATCHDOG
# System: JERICHO_SYSTEM

set -e

DB_HOST="postgres"
DB_PORT=5432
DB_NAME="jericho_db"
DB_USER="watchdog"
DB_PASSWORD="password"
BACKUP_DIR="/backups"

mkdir -p $BACKUP_DIR

TIMESTAMP=$(date +"%Y-%m-%dT%H%M%SZ")
FILENAME="$BACKUP_DIR/jericho_db_backup_$TIMESTAMP.sql.gz"

export PGPASSWORD=$DB_PASSWORD
pg_dump -h $DB_HOST -p $DB_PORT -U $DB_USER $DB_NAME | gzip > $FILENAME

find $BACKUP_DIR -type f -mtime +${BACKUP_RETENTION_DAYS} -name "*.sql.gz" -exec rm {} \;
