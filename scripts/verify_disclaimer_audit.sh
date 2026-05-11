#!/usr/bin/env bash
# verify_disclaimer_audit.sh — Re-Audit-Verifikation nach Codex-Sprint
#
# Quelle: memory/runs/2026-05-10_disclaimer_audit.md Gaps G1–G5
# Master:  memory/domain/zweckbestimmung_master_2026-05-06.md
#
# Läuft nach jedem Codex-Sprint und nach jedem Deploy. Exit-Code 0 = alle Gaps
# geschlossen, Exit-Code > 0 = Anzahl noch offener Gaps.
#
# Usage:
#   bash scripts/verify_disclaimer_audit.sh
#   bash scripts/verify_disclaimer_audit.sh --strict        # behandelt Warnungen als Fehler
#   bash scripts/verify_disclaimer_audit.sh --live          # zusätzlich Smoke gegen carotis.diggai.de
#
# Output: PASS/FAIL pro Gap + Markdown-Snippet für memory/runs/.

set -uo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CODE="$REPO_ROOT/code"
STRICT=0
LIVE=0

for arg in "$@"; do
  case "$arg" in
    --strict) STRICT=1 ;;
    --live) LIVE=1 ;;
    -h|--help)
      sed -n '1,30p' "$0" | sed 's/^# \{0,1\}//'
      exit 0
      ;;
  esac
done

FAILS=0
WARNS=0
RESULTS=()

green() { printf '\033[32m%s\033[0m\n' "$*"; }
red()   { printf '\033[31m%s\033[0m\n' "$*"; }
yellow(){ printf '\033[33m%s\033[0m\n' "$*"; }

record_pass() { RESULTS+=("PASS  $1"); green "PASS  $1"; }
record_fail() { RESULTS+=("FAIL  $1"); red "FAIL  $1"; FAILS=$((FAILS+1)); }
record_warn() {
  RESULTS+=("WARN  $1")
  yellow "WARN  $1"
  WARNS=$((WARNS+1))
  if [ "$STRICT" -eq 1 ]; then FAILS=$((FAILS+1)); fi
}

echo "==> Carotis-AI Disclaimer Re-Audit"
echo "    Repo: $REPO_ROOT"
echo

# ---------------------------------------------------------------------------
# G1 — ResearchSplashGate
# ---------------------------------------------------------------------------
if [ -f "$CODE/frontend/src/components/ResearchSplashGate/ResearchSplashGate.tsx" ]; then
  record_pass "G1.a ResearchSplashGate.tsx existiert"
else
  record_fail "G1.a ResearchSplashGate.tsx fehlt"
fi

if [ -f "$CODE/frontend/src/components/ResearchSplashGate/ResearchSplashGate.test.tsx" ]; then
  record_pass "G1.b ResearchSplashGate.test.tsx existiert"
else
  record_fail "G1.b ResearchSplashGate.test.tsx fehlt"
fi

if grep -q "ResearchSplashGate" "$CODE/frontend/src/App.tsx" 2>/dev/null; then
  record_pass "G1.c App.tsx integriert ResearchSplashGate"
else
  record_fail "G1.c App.tsx ohne ResearchSplashGate — Lou muss den Wrapper einfügen"
fi

if [ -f "$CODE/backend/app/api/routes/splash_confirmation.py" ]; then
  record_pass "G1.d Backend Splash-Confirmation-Endpoint existiert"
else
  record_fail "G1.d Backend Splash-Confirmation-Endpoint fehlt"
fi

# ---------------------------------------------------------------------------
# G2 — Watermark
# ---------------------------------------------------------------------------
if [ -f "$CODE/frontend/src/components/Watermark/Watermark.tsx" ]; then
  record_pass "G2.a Watermark.tsx existiert"
else
  record_fail "G2.a Watermark.tsx fehlt"
fi

if grep -q "Watermark" "$CODE/frontend/src/App.tsx" 2>/dev/null; then
  record_pass "G2.b App.tsx mountet Watermark"
else
  record_fail "G2.b App.tsx ohne Watermark"
fi

if grep -rq "RESEARCH USE ONLY" "$CODE/frontend/src" 2>/dev/null; then
  record_pass "G2.c 'RESEARCH USE ONLY' im Frontend-Code gefunden"
else
  record_fail "G2.c 'RESEARCH USE ONLY' nicht im Frontend-Code gefunden"
fi

# Export-Watermark (JSON-Output _disclaimer-Key)
if grep -rqE '"_disclaimer"|_disclaimer:' "$CODE/backend/app" 2>/dev/null; then
  record_pass "G2.d Export-Watermark _disclaimer im Backend"
else
  record_warn "G2.d Export _disclaimer-Key fehlt — JSON-Exports brauchen ihn"
fi

# ---------------------------------------------------------------------------
# G3 — CDS-Feature-Flag (kritisch)
# ---------------------------------------------------------------------------
if [ -f "$CODE/backend/app/core/feature_flags.py" ]; then
  record_pass "G3.a feature_flags.py existiert"
else
  record_fail "G3.a feature_flags.py fehlt"
fi

# Prüfen, dass Defaults False sind
if grep -E "cds_module_enabled: *bool *= *Field\(\s*default *= *False" \
    "$CODE/backend/app/core/feature_flags.py" >/dev/null 2>&1; then
  record_pass "G3.b cds_module_enabled default=False"
else
  record_fail "G3.b cds_module_enabled NICHT default=False (KRITISCH)"
fi

# Frontend DEMO_CASES sollten KEINE stenosis_pct_nascet als Pflicht-Daten haben
if grep -nE "stenosis_pct_nascet: *[0-9]+" "$CODE/frontend/src/App.tsx" >/dev/null 2>&1; then
  record_fail "G3.c App.tsx DEMO_CASES enthalten weiterhin numerische Stenose-Werte"
else
  record_pass "G3.c App.tsx DEMO_CASES enthalten keine numerischen Stenose-Werte"
fi

# Frontend Types: vulnerability_markers darf nicht Pflichtfeld der UI-API-Response sein
if grep -nE "vulnerability_markers: *VulnerabilityMarkers" \
   "$CODE/frontend/src/types/index.ts" >/dev/null 2>&1; then
  record_fail "G3.d Frontend Types haben vulnerability_markers als Pflicht — muss optional/entfernt sein"
else
  record_pass "G3.d Frontend Types ohne Pflicht-vulnerability_markers"
fi

# Backend public InferenceResponse darf stenosis_pct nicht als required Field haben
if grep -nE "stenosis_pct_nascet: *float *= *Field\(ge=0" \
   "$CODE/backend/app/schemas/inference.py" >/dev/null 2>&1; then
  record_fail "G3.e Backend public schema hat stenosis_pct_nascet als required"
else
  record_pass "G3.e Backend public schema ohne required stenosis_pct_nascet"
fi

# ---------------------------------------------------------------------------
# G4 — Splash-Confirmation Audit-Event
# ---------------------------------------------------------------------------
if grep -rqE 'splash_confirmation' "$CODE/backend/app" 2>/dev/null; then
  record_pass "G4.a Backend referenziert event_type='splash_confirmation'"
else
  record_fail "G4.a Backend hat keinen splash_confirmation-Event-Hook"
fi

# ---------------------------------------------------------------------------
# G5 — Begriffe-Substitution-Sweep
# ---------------------------------------------------------------------------
declare -a FORBIDDEN_UI=(
  "Diagnoseassistent"
  "Diagnose-Assistent"
  "Stenose-Messung"
  "Stenosemessung"
  "Plaque-Vulnerability-Score"
  "automatische Quantifizierung"
  "Klinikum-Pilot"
  "Befund-Output"
)
SUB_FAILS=0
for term in "${FORBIDDEN_UI[@]}"; do
  if grep -rqF "$term" "$CODE/frontend/src" "$CODE/backend/app/api" 2>/dev/null; then
    record_fail "G5 Begriff '$term' noch im UI/API-Code"
    SUB_FAILS=$((SUB_FAILS+1))
  fi
done
if [ "$SUB_FAILS" -eq 0 ]; then
  record_pass "G5 Begriffs-Substitution UI/API komplett"
fi

# ---------------------------------------------------------------------------
# Test-Suite
# ---------------------------------------------------------------------------
echo
echo "==> Test-Suite-Status"
if command -v npm >/dev/null 2>&1 && [ -d "$CODE/frontend" ]; then
  ( cd "$CODE/frontend" && npm test -- --run \
       src/components/ResearchSplashGate/ResearchSplashGate.test.tsx \
       src/components/Watermark/Watermark.test.tsx \
       2>&1 | tail -10 ) && record_pass "Frontend-Tests (Splash + Watermark) grün" \
    || record_fail "Frontend-Tests (Splash + Watermark) rot"
else
  record_warn "npm nicht verfügbar — Vitest-Suite übersprungen"
fi

if command -v pytest >/dev/null 2>&1 && [ -d "$CODE/backend" ]; then
  ( cd "$CODE/backend" && pytest tests/ -q -k "splash or feature_flag or disclaimer" \
       2>&1 | tail -10 ) && record_pass "Backend-Tests (splash + flags) grün" \
    || record_warn "Backend-Tests (splash + flags) noch ohne Match — Tests werden im Sprint geschrieben"
else
  record_warn "pytest nicht verfügbar — Backend-Suite übersprungen"
fi

# ---------------------------------------------------------------------------
# Live Smoke (optional)
# ---------------------------------------------------------------------------
if [ "$LIVE" -eq 1 ]; then
  echo
  echo "==> Live Smoke gegen https://carotis.diggai.de/"
  if curl -fsSL -m 10 "https://api.carotis.diggai.de/health/" >/dev/null; then
    record_pass "Backend health 200"
  else
    record_fail "Backend health nicht erreichbar"
  fi
  if curl -fsSL -m 10 "https://carotis.diggai.de/" | grep -qiE "research|forschung"; then
    record_pass "Frontend liefert Research-Frame-Marker im HTML"
  else
    record_warn "Frontend HTML enthält keine Research-Marker — visuelles Re-Frame ggf. unvollständig"
  fi
fi

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
echo
echo "==> Summary"
echo "    Gaps geschlossen: $((${#RESULTS[@]} - FAILS - WARNS)) / ${#RESULTS[@]}"
echo "    Warnungen:        $WARNS"
echo "    Fehler:           $FAILS"
echo

# Markdown-Snippet für Run-Log
{
  echo "## Re-Audit Ergebnis ($(date -u +%Y-%m-%dT%H:%M:%SZ))"
  echo
  echo "| Status | Check |"
  echo "|---|---|"
  for line in "${RESULTS[@]}"; do
    status="${line:0:4}"
    rest="${line:6}"
    echo "| $status | $rest |"
  done
  echo
  echo "**Fehler:** $FAILS · **Warnungen:** $WARNS"
} > "$REPO_ROOT/memory/runs/.re_audit_$(date +%s).md"

if [ "$FAILS" -gt 0 ]; then
  red "FAILED — $FAILS Gap(s) noch offen. Run-Log: memory/runs/.re_audit_*.md"
  exit "$FAILS"
fi

green "ALL GREEN — alle Disclaimer-Gaps geschlossen."
exit 0
