#!/usr/bin/env bash
# Carotis-AI Pre-Flight Check (Bash / Git Bash / WSL / Linux)
#
# Pflicht-Lauf am Anfang JEDER Modell-Session.
# Prüft: Working Memory geladen, Memory-Index aktuell, letzte Run-Logs gesehen,
# in_progress Tasks bekannt, bekannte Anomalien notiert.
#
# Usage: ./scripts/preflight.sh [feature_keyword]
#
# Wenn ein feature_keyword übergeben wird: Suche danach in memory/runs/ + memory/domain/.
# Output: stdout, exit 0.

set -euo pipefail

# Farb-Codes (nur wenn Terminal)
if [ -t 1 ]; then
  RED=$'\033[0;31m'
  GRN=$'\033[0;32m'
  YEL=$'\033[1;33m'
  CYA=$'\033[0;36m'
  RST=$'\033[0m'
else
  RED=''; GRN=''; YEL=''; CYA=''; RST=''
fi

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
WORKSPACE="$(cd -- "$SCRIPT_DIR/.." &> /dev/null && pwd)"

cd "$WORKSPACE"

echo "${CYA}=== Carotis-AI Pre-Flight Check ===${RST}"
echo "Workspace: $WORKSPACE"
echo "Date: $(date -u +'%Y-%m-%d %H:%M:%S UTC')"
echo

# --- 1. CLAUDE.md vorhanden? ---
echo "${CYA}[1/6] Working Memory${RST}"
if [ -f CLAUDE.md ]; then
  PHASE=$(grep -E '^\| P[0-9]+ \| 🔄' CLAUDE.md | head -1 | awk -F'|' '{print $2}' | xargs || echo "unknown")
  echo "  ${GRN}✓${RST} CLAUDE.md vorhanden — aktive Phase: ${YEL}${PHASE:-unknown}${RST}"
else
  echo "  ${RED}✗${RST} CLAUDE.md FEHLT — STOP, lies die README"
  exit 1
fi

# --- 2. MEMORY.md vorhanden? ---
echo
echo "${CYA}[2/6] Memory-Index${RST}"
if [ -f MEMORY.md ]; then
  ENTRIES=$(grep -cE '^- \[' MEMORY.md || true)
  echo "  ${GRN}✓${RST} MEMORY.md vorhanden — ${ENTRIES} Einträge"
else
  echo "  ${RED}✗${RST} MEMORY.md FEHLT"
  exit 1
fi

# --- 3. Letzte 3 Run-Logs ---
echo
echo "${CYA}[3/6] Letzte 3 Run-Logs${RST}"
if [ -d memory/runs ]; then
  RUNS=$(ls -t memory/runs/*.md 2>/dev/null | head -3 || true)
  if [ -z "$RUNS" ]; then
    echo "  ${YEL}!${RST} Noch keine Run-Logs — du bist die erste Session"
  else
    while IFS= read -r run; do
      basename "$run" | sed 's/^/  /'
    done <<< "$RUNS"
  fi
else
  echo "  ${YEL}!${RST} memory/runs/ existiert nicht"
fi

# --- 4. In-Progress Tasks ---
echo
echo "${CYA}[4/6] In-Progress Tasks${RST}"
if [ -f tasks.jsonl ]; then
  IN_PROGRESS=$(grep -c '"status":"in_progress"' tasks.jsonl || true)
  PENDING=$(grep -c '"status":"pending"' tasks.jsonl || true)
  DONE=$(grep -c '"status":"done"' tasks.jsonl || true)
  echo "  ${GRN}✓${RST} tasks.jsonl: ${YEL}${IN_PROGRESS}${RST} in_progress · ${PENDING} pending · ${DONE} done"
  if [ "${IN_PROGRESS:-0}" -gt 0 ]; then
    echo "  In-Progress Tasks (vorsichtig — vielleicht noch offen):"
    grep '"status":"in_progress"' tasks.jsonl | sed 's/.*"id":"\([^"]*\)".*"title":"\([^"]*\)".*/    - \1: \2/'
  fi
else
  echo "  ${YEL}!${RST} tasks.jsonl existiert nicht — vielleicht erste Session"
fi

# --- 5. Anomalien ---
echo
echo "${CYA}[5/6] Bekannte Anomalien${RST}"
if [ -d memory/anomalies ] && [ -n "$(ls -A memory/anomalies/ 2>/dev/null)" ]; then
  N=$(ls memory/anomalies/ | wc -l | xargs)
  echo "  ${YEL}!${RST} ${N} Anomalie-Einträge — vor Code-Änderung lesen!"
  ls memory/anomalies/ | sed 's/^/    - /'
else
  echo "  ${GRN}✓${RST} Keine Anomalien bekannt"
fi

# --- 6. Optionale Keyword-Suche ---
echo
echo "${CYA}[6/6] Keyword-Suche${RST}"
if [ "$#" -gt 0 ]; then
  KEYWORD="$1"
  echo "  Suche nach: '${KEYWORD}'"
  HITS=$(grep -rl --include='*.md' "$KEYWORD" memory/ 2>/dev/null || true)
  if [ -z "$HITS" ]; then
    echo "  ${GRN}✓${RST} Kein Vorkommen in memory/ — sicher, neuen Eintrag anzulegen"
  else
    echo "  ${YEL}!${RST} Vorkommen gefunden — vor Doppelarbeit prüfen:"
    echo "$HITS" | sed 's/^/    /'
  fi
else
  echo "  (Kein Keyword übergeben — überspringe Suche)"
fi

echo
echo "${GRN}Pre-Flight done. Du kannst arbeiten.${RST}"
echo "Reminder: Am Ende der Session memory/runs/$(date -u +'%Y-%m-%d')_<modell>_<thema>.md schreiben."
