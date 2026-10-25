#!/bin/bash
# Zero-token watchdog: restarts the scanner if it ever dies.
# Usage:  nohup ./scripts/supervise.sh > /dev/null 2>&1 &
set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(dirname "$HERE")"
SUP="${KATANA_SUP_LOG:-$ROOT/.katana/supervisor.log}"
mkdir -p "$(dirname "$SUP")"
PAT="agent"; PAT="${PAT}.persistent"

while true; do
  if ! pgrep -f "$PAT" > /dev/null 2>&1; then
    echo "[$(date -Is)] scanner DOWN - restarting" >> "$SUP"
    cd "$ROOT"
    setsid nohup "$HERE/run_persistent.sh" >> "$ROOT/.katana/stdout.log" 2>&1 < /dev/null &
  else
    echo "[$(date -Is)] scanner UP pid=$(pgrep -f "$PAT" | head -1)" >> "$SUP"
  fi
  sleep 60
done
