#!/usr/bin/env bash
# Path: scripts/SYS_WATCHDOG/deploy.sh
# Description: Deploys SYS_WATCHDOG (v2.1) with Docker Compose, observability, and backup scheduling.
# Version: 2.1.0
# Sub_System: SYS_WATCHDOG
# System: JERICHO_SYSTEM

set -e

echo "Stopping existing containers..."
docker-compose -f SYS_WATCHDOG/docker/docker-compose.yaml down --remove-orphans

echo "Building and starting containers..."
docker-compose -f SYS_WATCHDOG/docker/docker-compose.yaml up --build -d

echo "SYS_WATCHDOG and Postgres are online."
