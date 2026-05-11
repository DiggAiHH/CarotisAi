---
name: 2026-05-04_Codex_GPT55-Run17_live_browser_ui_fix
type: run
agent: Codex GPT-5.5
date: 2026-05-04
---

## Goal

Live-Browser-Test von `https://carotis.diggai.de/`, Master-Demo-Token pruefen und sichtbare UI-/Demo-Probleme verbessern.

## Done

- Browser-Harness konnte nicht an Chrome attachen (`DevToolsActivePort not found`); Test deshalb mit Playwright Chromium gegen die Live-Domain ausgefuehrt.
- Master-Demo-Token im Frontend-Gate getestet: API `/api/v1/demo/whoami` liefert 200 und Token wird gespeichert.
- CSP-Blocker im Frontend behoben: `code/frontend/nginx.conf` erlaubt jetzt `connect-src 'self' https://api.carotis.diggai.de`.
- Healthcheck-Bug behoben: `apiClient.getHealth()` nutzt `/health/` statt `/health`, um den HTTP-Redirect hinter Caddy/Uvicorn zu vermeiden.
- Walkthrough-UI verbessert: weniger dunkles Overlay, sauberer Tour-Button, bessere Kartenposition bei Resize/Mobile, erste sichtbare Tour-Texte mit Umlauten.
- Frontend auf Hetzner neu gebaut und gestartet.

## Verification

- `npm test -- --run src/components/AuthGate/AuthGate.test.tsx src/components/Walkthrough/Walkthrough.test.tsx` -> 11 passed.
- `npm run build` -> success; Cornerstone/Vite WASM-Warnungen bleiben erwartbar.
- Live Playwright: `whoami` 200, `/health/` 200, Header zeigt `Online`, keine CSP-/Requestfailed-Events.
- `BASE_URL=https://carotis.diggai.de DEMO_TOKEN=<master> CI=true npx playwright test e2e/chromium_visual_smoke.spec.ts --project=chromium --reporter=list` -> 1 passed.

## Evidence

- Screenshots lokal: `code/frontend/test-results/live-final-desktop.png`, `code/frontend/test-results/live-final-mobile.png`.

## Safety

Keine Patientendaten verwendet. Rohwert des Master-Demo-Tokens nicht in diese Memory-Datei geschrieben.
