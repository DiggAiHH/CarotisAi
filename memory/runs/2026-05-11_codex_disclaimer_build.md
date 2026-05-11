---
name: 2026-05-11_codex_disclaimer_build
type: run
agent: Codex GPT-5.5
date: 2026-05-11
phase: P0g
task: K-56
source: memory/runs/2026-05-10_disclaimer_audit.md
---

## Goal

G1-G5 aus dem Disclaimer-Audit schliessen: Pflicht-Splash, UI-/Export-Watermark, CDS-Feature-Flag-Gate, Splash-Audit-Event und Begriffssubstitution gemaess `memory/domain/zweckbestimmung_master_2026-05-06.md`.

## Done

- `ResearchSplashGate` ist vor `AuthGate` in `App.tsx` aktiv, nutzt das Master-Wording aus §E, verlangt 3 Checkboxen, speichert nur in `sessionStorage` und sendet `{ session_id, confirmed_at, role_hash, version }`.
- `Watermark` ist als App-Sibling nach Splash/Auth eingebunden; Text: `RESEARCH USE ONLY · Forschungsverwendung · Kein Medizinprodukt`.
- Backend public inference response ist auf `InferenceResponse` ohne `stenosis_pct_nascet`, `vulnerability_markers` und rohes `confidence` reduziert; `InternalInferenceRecord`/`PredictionResponse` behalten Forschungswerte intern.
- `feature_flags.py` steuert CDS-/Quantifizierungs-Exposure default-off; `/api/v1/audit/splash-confirmation` schreibt `splash_confirmation`; `/api/v1/audit/events?type=splash_confirmation` gibt `payload_redacted` zurueck.
- JSON Decision-Tree-Exports erhalten Top-Level `_disclaimer: "RESEARCH USE ONLY · Kein Medizinprodukt"`.
- Frontend-Demo, AiPanel und DicomViewer zeigen keine Prozent-/NASCET-/Vulnerability-Texte im Forschungsmodus.

## Verification

- Backend: `pytest tests/ -q -p no:warnings` mit Test-Env: **128 passed, 11 skipped**.
- Frontend: `npm run typecheck`, `npm run lint`, `npm test -- --run`: **45 passed**, `npm run build` gruen mit bekannten Cornerstone/WASM- und Chunk-Size-Warnungen.
- Grep-Sweep auf `code/frontend/src` und `code/backend/app/api` fuer die Alt-Begriffe aus G5: **0 Treffer**.
- Lokaler Playwright-Smoke gegen `http://127.0.0.1:3001/` mit `VITE_SKIP_AUTH=true`: Cold Open zeigt Splash; nach Confirmation Watermark sichtbar; kein `%`, kein `NASCET`, kein `Vulnerability` im sichtbaren Text.
- Live-Smoke gegen `https://carotis.diggai.de/`: Domain liefert noch alten Deploy-Stand mit AuthGate direkt, **kein Splash/Watermark**. Code ist lokal gruen, Deployment/Freigabe steht noch aus.

## Surprised by

- Der vorhandene Worktree hatte bereits Teilimplementierungen, aber Splash sendete `user_id` statt `role_hash`, `/audit/events` fehlte und der Viewer zeigte weiterhin Prozentwerte.
- Browser-Harness war wegen fehlendem Chrome Remote Debugging blockiert; Playwright/Chromium funktionierte als lokale Verifikationsstrecke.

## Avoided

- Keine Patientendaten, keine Cloud-Inferenz, kein Office-Doc-Edit, kein Revert fremder Worktree-Aenderungen, kein Deploy ohne Lou-Freigabe.

## Next

- Lou-Freigabe-Gate, dann Deploy auf Hetzner/Live-Domain und erneuter Live-Smoke gegen `https://carotis.diggai.de/`.
