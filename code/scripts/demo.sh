#!/usr/bin/env bash
# Carotis-AI one-shot demo launcher — Linux / macOS
#
# Usage (from code/ directory):
#   bash scripts/demo.sh
set -euo pipefail

# ── Locate code/ root ─────────────────────────────────────────────────────────
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CODE_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$CODE_ROOT"

# ── Colours ──────────────────────────────────────────────────────────────────
CYAN='\033[0;36m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
RED='\033[0;31m'; GRAY='\033[0;90m'; RESET='\033[0m'

banner() { echo -e "\n${CYAN}  ──────────────────────────────────\n  │  $1  │\n  ──────────────────────────────────${RESET}\n"; }
step()   { echo -e "${YELLOW}  ► $1${RESET}"; }
ok()     { echo -e "${GREEN}  ✓ $1${RESET}"; }
fail()   { echo -e "${RED}  ✗ $1${RESET}"; exit 1; }

banner "Carotis-AI Demo Launcher"

# ── Step 1: Docker ───────────────────────────────────────────────────────────
step "Checking Docker..."
if ! docker info &>/dev/null; then
    fail "Docker is not running — start Docker Desktop / Docker daemon and retry."
fi
ok "Docker is running."

# ── Step 2: Data directories ─────────────────────────────────────────────────
step "Creating data directories..."
mkdir -p data/models data/db data/dicom_temp
ok "data/ ready."

# ── Step 3: .env ─────────────────────────────────────────────────────────────
step "Checking backend/.env..."
if [[ ! -f backend/.env ]]; then
    cp backend/.env.example backend/.env
    ok "Copied .env.example → .env  (edit API_KEY before production!)"
else
    ok ".env already present."
fi

# ── Step 4: Demo ONNX model ───────────────────────────────────────────────────
step "Checking demo ONNX model..."
if [[ ! -f data/models/mfsd_unet.onnx ]]; then
    echo -e "${GRAY}  Generating demo model (first run — ~30 s)...${RESET}"

    PYTHON=""
    for candidate in "backend/.venv/bin/python" "backend/.venv/bin/python3" \
                     "$(which python3 2>/dev/null)" "$(which python 2>/dev/null)"; do
        if [[ -x "$candidate" ]]; then PYTHON="$candidate"; break; fi
    done
    [[ -z "$PYTHON" ]] && fail "Python 3.11+ not found. Install it and re-run."

    "$PYTHON" scripts/generate_demo_model.py
    ok "Demo model generated."
else
    ok "Demo model already present."
fi

# ── Step 5: Docker Compose + Ollama/Hermes bootstrap ─────────────────────────
step "Building and starting containers (backend + frontend + ollama + hermes)..."
docker compose up --build -d
ok "Containers started."

# Wait for Ollama
step "Waiting for Ollama to become ready..."
MAX_OLLAMA=60; i=0; OLLAMA_OK=false
while [[ $i -lt $MAX_OLLAMA ]]; do
    i=$((i+1))
    if curl -sf http://localhost:11434/api/tags >/dev/null 2>&1; then
        OLLAMA_OK=true; break
    fi
    echo -e "${GRAY}  . Ollama starting ($i/$MAX_OLLAMA)${RESET}"
    sleep 3
done

if [[ $OLLAMA_OK == true ]]; then
    ok "Ollama is ready."

    # Pull Hermes model (skip if already present)
    HERMES_MODEL="${HERMES_MODEL:-nous-hermes-3-llama-3.1}"
    if ! docker compose exec -T ollama ollama list 2>/dev/null | grep -q "hermes"; then
        step "Pulling Hermes model (${HERMES_MODEL}) — this runs once (~5–15 min on first launch)..."
        docker compose exec -T ollama ollama pull "${HERMES_MODEL}" \
            || echo -e "${YELLOW}  ⚠ Model pull failed — Hermes features will be unavailable${RESET}"
    else
        ok "Hermes model already available."
    fi

    # Pull compression model
    COMPRESSION_MODEL="${COMPRESSION_MODEL:-qwen2.5-coder:7b}"
    if ! docker compose exec -T ollama ollama list 2>/dev/null | grep -q "qwen2.5-coder"; then
        step "Pulling compression model (${COMPRESSION_MODEL})..."
        docker compose exec -T ollama ollama pull "${COMPRESSION_MODEL}" \
            || echo -e "${YELLOW}  ⚠ Compression model pull failed — non-critical${RESET}"
    else
        ok "Compression model already available."
    fi
else
    echo -e "${YELLOW}  ⚠ Ollama did not start in time — Hermes AI features unavailable${RESET}"
fi

# ── Step 6: Health checks ─────────────────────────────────────────────────────
step "Waiting for backend health endpoint..."
MAX=40; i=0; HEALTHY=false
while [[ $i -lt $MAX ]]; do
    i=$((i+1))
    if curl -sf http://localhost:8000/health >/dev/null 2>&1; then
        HEALTHY=true; break
    fi
    echo -e "${GRAY}  . (attempt $i/$MAX)${RESET}"
    sleep 3
done
[[ $HEALTHY == true ]] || fail "Backend not healthy after $((MAX*3))s — run: docker compose logs backend"
ok "Backend is healthy."

step "Smoke testing API endpoints..."

# Health
HEALTH_STATUS=$(curl -sf http://localhost:8000/health | python3 -c "import sys,json; print(json.load(sys.stdin).get('status','?'))" 2>/dev/null || echo "unknown")
[[ $HEALTH_STATUS == "ok" ]] && ok "GET /health → ok" || echo -e "${YELLOW}  ⚠ /health returned: ${HEALTH_STATUS}${RESET}"

# Audit trail (expects 200 + pagination schema)
API_KEY_VAL=$(grep "^API_KEY=" backend/.env 2>/dev/null | cut -d= -f2 | tr -d '"' || echo "carotis-dev-key-change-in-prod")
AUDIT_STATUS=$(curl -sf -o /dev/null -w "%{http_code}" \
    -H "x-api-key: ${API_KEY_VAL}" \
    http://localhost:8000/api/v1/audit/trail 2>/dev/null || echo "000")
[[ $AUDIT_STATUS == "200" ]] && ok "GET /api/v1/audit/trail → 200" \
    || echo -e "${YELLOW}  ⚠ /audit/trail returned: ${AUDIT_STATUS}${RESET}"

# Hermes (optional)
HERMES_STATUS=$(curl -sf -o /dev/null -w "%{http_code}" http://localhost:8200/health 2>/dev/null || echo "000")
[[ $HERMES_STATUS == "200" ]] && ok "GET Hermes /health → 200" \
    || echo -e "${YELLOW}  ⚠ Hermes not reachable (status: ${HERMES_STATUS}) — non-critical${RESET}"

# ── Step 7: URLs ─────────────────────────────────────────────────────────────
banner "Carotis-AI is running!"
echo -e "${CYAN}  Frontend  →  http://localhost:3000"
echo -e "  Backend   →  http://localhost:8000"
echo -e "  API docs  →  http://localhost:8000/docs"
echo -e "  Health    →  http://localhost:8000/health"
echo -e "  Audit     →  http://localhost:8000/api/v1/audit/trail"
echo -e "  Hermes    →  http://localhost:8200/health${RESET}"
echo -e "${GRAY}"
echo -e "  Stop:  docker compose down"
echo -e "  Logs:  docker compose logs -f"
echo -e "  Logs (ollama):  docker compose logs ollama"
echo -e "  Logs (hermes):  docker compose logs hermes${RESET}"
echo ""

# ── Step 8: Extended Smoke Test ────────────────────────────────────────────────
step "Running extended smoke test..."
docker compose run --rm backend pytest tests/test_smoke.py -q || fail "Smoke test failed"
ok "All systems operational."

banner "Demo Stack Ready"
echo -e "  Backend:   http://localhost:8000"
echo -e "  Frontend:  http://localhost:3000"
echo -e "  Ollama:    http://localhost:11434"
echo -e "  Hermes:    http://localhost:8200"
echo -e "  Dashboard: ../dashboard.html (open in browser)"
echo ""
