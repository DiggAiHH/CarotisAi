#!/usr/bin/env bash
# Carotis-AI Demo Teardown — Linux / macOS
#
# Usage: bash scripts/teardown_demo.sh [--keep-data]
set -euo pipefail

KEEP_DATA=false
if [[ "${1:-}" == "--keep-data" ]]; then
    KEEP_DATA=true
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CODE_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$CODE_ROOT"

echo "Stopping containers..."
docker compose down --volumes

if [[ "$KEEP_DATA" == "false" ]]; then
    echo "Removing demo data..."
    rm -rf data/demo
    echo "Demo data removed."
else
    echo "Keeping demo data (use --keep-data flag)."
fi

echo "Teardown complete."
