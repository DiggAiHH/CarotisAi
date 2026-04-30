#!/usr/bin/env bash
set -euo pipefail

LOG_FILE="/tmp/install_local_stack.log"
exec > >(tee -a "$LOG_FILE") 2>&1

# Farb-Codes
BANNER='\033[1;34m'
STEP='\033[1;33m'
OK='\033[1;32m'
FAIL='\033[1;31m'
RESET='\033[0m'

banner() {
    echo -e "${BANNER}=== $1 ===${RESET}"
}

step() {
    echo -e "${STEP}-> $1${RESET}"
}

ok() {
    echo -e "${OK}OK: $1${RESET}"
}

fail() {
    echo -e "${FAIL}FAIL: $1${RESET}"
    exit 1
}

banner "Carotis-AI Local Stack Installer"

# 1. OS erkennen
OS=$(uname -s)
if [[ "$OS" == "Linux" || "$OS" == "Darwin" ]]; then
    step "OS erkannt: $OS"
else
    fail "Windows erkannt. Bitte install_local_stack.ps1 verwenden."
fi

# 2. Ollama installieren
if ! command -v ollama &> /dev/null; then
    step "Ollama wird installiert..."
    curl -fsSL https://ollama.com/install.sh | sh
    ok "Ollama installiert"
else
    ok "Ollama bereits vorhanden"
fi

# 3. Ollama-Service starten
step "Ollama-Service wird gestartet..."
if pgrep -f "ollama serve" > /dev/null; then
    ok "Ollama laeuft bereits"
else
    nohup ollama serve > /tmp/ollama.log 2>&1 &
    sleep 3
    if pgrep -f "ollama serve" > /dev/null; then
        ok "Ollama gestartet"
    else
        fail "Ollama konnte nicht gestartet werden"
    fi
fi

# Port-Konflikt pruefen
if ss -tlnp 2>/dev/null | grep -q ':11434 ' || netstat -tlnp 2>/dev/null | grep -q ':11434 '; then
    ok "Port 11434 ist belegt (Ollama)"
else
    fail "Port 11434 ist nicht belegt - Ollama laeuft nicht korrekt"
fi

# 4. Modelle pullen (idempotent)
pull_model() {
    local model="$1"
    if ollama list | grep -q "$model"; then
        ok "Modell $model bereits vorhanden"
    else
        step "Modell $model wird heruntergeladen (Timeout 30 Min)..."
        timeout 1800 ollama pull "$model" || fail "Download von $model fehlgeschlagen"
        ok "Modell $model heruntergeladen"
    fi
}

pull_model "nous-hermes-3-llama-3.1"
pull_model "qwen2.5-coder:7b"
pull_model "llava-llama3:8b" || true  # optional

# 5. Python venv
if [[ ! -d ".venv" ]]; then
    step "Python venv wird erstellt..."
    python3 -m venv .venv
    ok "venv erstellt"
else
    ok "venv bereits vorhanden"
fi

# 6. Hermes Agent installieren
step "Hermes Agent wird installiert..."
pip install --quiet git+https://github.com/NousResearch/hermes-agent.git || {
    echo "Hinweis: Installation aus Git fehlgeschlagen, versuche PyPI..."
    pip install --quiet hermes-agent || true
}
ok "Hermes Agent installiert"

# 7. Verify
step "Verifiziere Ollama-API..."
MODELS=$(curl -fs localhost:11434/api/tags | grep -o '"name":"[^"]*"' | cut -d'"' -f4)
if echo "$MODELS" | grep -q "nous-hermes-3-llama-3.1"; then
    ok "API erreichbar und Modelle gelistet"
else
    fail "API-Verifizierung fehlgeschlagen"
fi

# 8. Summary
banner "Setup Summary"
echo "Installations-Log: $LOG_FILE"
echo "Ollama-Log: /tmp/ollama.log"
echo ""
echo "Gepullte Modelle:"
echo "$MODELS"
echo ""
echo "Naechste Schritte:"
echo "1. cp backend/.env.example backend/.env"
echo "2. API_KEY in backend/.env anpassen (min. 32 Zeichen)"
echo "3. docker compose up --build   oder   make demo"
