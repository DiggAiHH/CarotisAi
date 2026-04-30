#!/usr/bin/env bash
# Carotis-AI 5-Min-Demo Launcher — Linux / macOS
#
# Usage (from code/ directory):
#   bash scripts/run_demo.sh
set -euo pipefail

# -- Locate code/ root ---------------------------------------------------------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CODE_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$CODE_ROOT"

# -- Helpers -------------------------------------------------------------------
CYAN='\033[0;36m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
RED='\033[0;31m'; GRAY='\033[0;90m'; RESET='\033[0m'

banner() { echo -e "\n${CYAN}  --------------------------------\n  |  $1  |\n  --------------------------------${RESET}\n"; }
step()   { echo -e "${YELLOW}  > $1${RESET}"; }
ok()     { echo -e "${GREEN}  [OK] $1${RESET}"; }
fail()   { echo -e "${RED}  [FAIL] $1${RESET}"; exit 1; }

banner "Carotis-AI Demo Launcher"

# -- Step 0: Port check --------------------------------------------------------
step "Checking ports..."
_port_busy() {
    if command -v ss &>/dev/null; then
        ss -tlnp 2>/dev/null | grep -q ":$1 "
    elif command -v netstat &>/dev/null; then
        netstat -tlnp 2>/dev/null | grep -q ":$1 "
    else
        return 1
    fi
}
for port in 3000 8000; do
    if _port_busy "$port"; then
        echo -e "${YELLOW}  WARNING: Port $port is already in use.${RESET}"
    fi
done
ok "Port check done."

# -- Step 1: Pre-Flight --------------------------------------------------------
step "Running pre-flight..."
if [[ -f ../scripts/preflight.sh ]]; then
    bash ../scripts/preflight.sh || fail "Pre-flight failed"
else
    step "Skipping pre-flight (not found)"
fi
ok "Pre-flight done."

# -- Step 2: Docker ------------------------------------------------------------
step "Checking Docker..."
if ! docker info &>/dev/null; then
    fail "Docker is not running -- start Docker Desktop / Docker daemon and retry."
fi
ok "Docker is running."

# -- Step 3: Data directories --------------------------------------------------
step "Creating data directories..."
mkdir -p data/models data/db data/dicom_temp

# Ensure .env exists
if [[ ! -f backend/.env ]]; then
    if [[ -f backend/.env.example ]]; then
        cp backend/.env.example backend/.env
        ok "Created backend/.env from .env.example"
    else
        step "WARNING: backend/.env missing and no .env.example found"
    fi
fi

docker compose up -d
ok "Containers started."

# -- Step 4: Demo ONNX model ---------------------------------------------------
step "Checking demo ONNX model..."
if [[ ! -f data/models/mfsd_unet.onnx ]]; then
    PYTHON=""
    for candidate in "backend/.venv/bin/python" "backend/.venv/bin/python3" \
                     "$(which python3 2>/dev/null)" "$(which python 2>/dev/null)"; do
        if [[ -x "$candidate" ]]; then PYTHON="$candidate"; break; fi
    done
    [[ -z "$PYTHON" ]] && fail "Python 3.11+ not found."
    "$PYTHON" scripts/generate_demo_model.py
    ok "Demo model generated."
else
    ok "Demo model already present."
fi

# -- Step 5: Demo data ---------------------------------------------------------
step "Checking demo data..."
if [[ ! -d data/demo/dicoms ]] || [[ $(ls data/demo/dicoms/*.dcm 2>/dev/null | wc -l) -lt 10 ]]; then
    PYTHON=""
    for candidate in "backend/.venv/bin/python" "backend/.venv/bin/python3" \
                     "$(which python3 2>/dev/null)" "$(which python 2>/dev/null)"; do
        if [[ -x "$candidate" ]]; then PYTHON="$candidate"; break; fi
    done
    [[ -z "$PYTHON" ]] && fail "Python not found."
    "$PYTHON" scripts/generate_demo_data.py --count 10
    ok "Demo data generated."
else
    ok "Demo data already present."
fi

# -- Step 6: POST decision trees to backend ------------------------------------
step "Seeding decision trees into backend..."
API_KEY_VAL=$(grep "^API_KEY=" backend/.env 2>/dev/null | cut -d= -f2 | tr -d '"' || echo "carotis-dev-key-change-in-prod")

for f in data/demo/decision_trees/*.json; do
    curl -sf -o /dev/null -w "%{http_code}" \
        -H "Content-Type: application/json" \
        -H "X-API-Key: ${API_KEY_VAL}" \
        -d "@$f" \
        http://localhost:8000/api/v1/decision-tree/capture >/dev/null 2>&1 || true
done
ok "Decision trees seeded."

# -- Step 7: Wait for backend health -------------------------------------------
step "Waiting for backend health..."
MAX=40; i=0; HEALTHY=false
while [[ $i -lt $MAX ]]; do
    i=$((i+1))
    if curl -sf http://localhost:8000/health >/dev/null 2>&1; then
        HEALTHY=true; break
    fi
    echo -e "${GRAY}  . (attempt $i/$MAX)${RESET}"
    sleep 3
done
[[ $HEALTHY == true ]] || fail "Backend not healthy after $((MAX*3))s"
ok "Backend is healthy."

# -- Step 8: Open browser ------------------------------------------------------
step "Opening browser..."
DASHBOARD_PATH="$(cd .. && pwd)/dashboard.html"
if command -v xdg-open &>/dev/null; then
    xdg-open http://localhost:3000 >/dev/null 2>&1 &
    xdg-open "file://$DASHBOARD_PATH" >/dev/null 2>&1 &
elif command -v open &>/dev/null; then
    open http://localhost:3000 >/dev/null 2>&1 &
    open "file://$DASHBOARD_PATH" >/dev/null 2>&1 &
else
    echo -e "${GRAY}  Please open manually:${RESET}"
    echo -e "${GRAY}    Frontend:  http://localhost:3000${RESET}"
    echo -e "${GRAY}    Dashboard: file://$DASHBOARD_PATH${RESET}"
fi
ok "Browser opened."

# -- Step 9: Done --------------------------------------------------------------
banner "DEMO READY"

echo -e "${GREEN}  Frontend:  http://localhost:3000${RESET}"
echo -e "${GREEN}  Backend:   http://localhost:8000${RESET}"
echo -e "${GREEN}  Dashboard: file://$DASHBOARD_PATH${RESET}"
echo ""
echo -e "${YELLOW}  Press any key to open VS Code with demo_walkthrough.md${RESET}"
read -n 1 -s

if command -v code &>/dev/null; then
    code scripts/demo_walkthrough.md
fi

echo ""
echo -e "${GRAY}  Stop:  bash scripts/teardown_demo.sh${RESET}"
echo ""
