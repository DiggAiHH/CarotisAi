---
name: 2026-05-02_Codex_GPT55-Run11_memory_deploy_smoke
type: run
model: Codex GPT-5.5
phase: P0f
---

## Goal
Erst Memory verdichten, dann Deploy online bringen und echte Frontend-/Backend-Smokes ausfuehren, ohne Secrets zu persistieren.

## Done
- Summary-first Memory-Verdichtung erstellt: `memory/domain/recent_runs_summary_2026-05-02.md`.
- Deploy-Kompaktstatus erstellt/aktualisiert: `memory/domain/p0f_deploy_state_compact_2026-05-02.md`.
- Lokale Secret-Dateien bereinigt: `add_ssh_key.py` und `deploy/bootstrap_hetzner.py` nutzen jetzt `HETZNER_ROOT_PASSWORD` statt hardcoded Passwort.
- GitHub Secrets geprueft: benoetigte Deploy-Secrets sind vorhanden.
- DNS geprueft: `carotis.diggai.de` zeigt auf Fly; `api.carotis.diggai.de` zeigt auf Hetzner-IP.
- Fly-App/Cert-Workflow ausgeloest: success.
- Frontend-Fly-Deploy ausgeloest: success.
- Online-Frontend-HTTP geprueft: `https://carotis.diggai.de/` liefert 200.
- Online-Frontend-Visual-Smoke ausgefuehrt: Playwright Chromium passed 1/1 gegen `https://carotis.diggai.de`.
- Backend-Deploy-Workflow ausgeloest: failure in `Prepare Hetzner host` wegen SSH `Permission denied`.
- Lokale SSH-Tests mit Deploy-Key, Default-Key und `diggai_deploy` gegen Hetzner: alle `Permission denied`.
- Online-Backend-Health geprueft: `https://api.carotis.diggai.de/health/` nicht erreichbar.
- Lokaler Backend-Smoke mit Dummy-Test-Keys: `tests/test_smoke.py` passed 6/6.

## Surprised by
Der vorherige `Test SSH Key` Workflow pruefte nur, ob der GitHub-Secret-Key syntaktisch valide ist; er testete keine Server-Verbindung. Der echte Deploy-Workflow zeigt weiterhin, dass der Server den Key nicht akzeptiert.

## Avoided
- Keine geposteten Secrets in Dateien, Run-Logs oder Commands persistiert.
- Kein Core-Memory-Overwrite.
- Keine Patientendaten oder Roh-DICOMs verwendet.
- Kein DNS-/Provider-Save ausser GitHub Workflow Dispatch.
- Kein globales SSH/PATH/Python-Setup veraendert.

## Next
- Backend kann erst online gehen, wenn der Server den GitHub-Deploy-Key oder einen lokal nutzbaren Key akzeptiert.
- Danach `deploy-backend-hetzner.yml` erneut ausloesen und `https://api.carotis.diggai.de/health/` pruefen.
- Nach erfolgreichem Backend-Deploy volle Rohde-Walkthrough-E2E gegen Live-Frontend + Live-Backend ausfuehren.
