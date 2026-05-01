---
name: 2026-04-30_Kimi_K26-Run03_solo_cleanup
type: run
---

## Goal
Alles was ohne Human-Intervention machbar ist, abschliessen: Dokumente aktualisieren, Deploy-Bugs fixen, Cross-References pruefen.

## Done
- **AGENTS.md v2**: 11 Edits — Hosting Netlify→Fly/Hetzner, Test-Baselines (100/5/11), `npm test` existiert jetzt, orphaned router + export_onnx Duplikat + audit_service Bug als fixed markiert, CI-Env-Vars dokumentiert, CORS-Note aktualisiert, scikit-learn als optional dependency hinzugefuegt.
- **CLAUDE.md v1.2**: Hosting Netlify→Fly/Hetzner, P0f Phase Status mit S1-S17 Completion, aktuelle Test-Baselines.
- **CI workflow**: `ADMIN_API_KEY`, `ANONYMIZATION_SALT`, `ONNX_MODEL_PATH` zu `test-backend` Job hinzugefuegt (waren missing seit Config-Hardening S9).
- **Deploy-Bugfix (kritisch)**: `ANONYMIZATION_SALT` fehlte in `deploy-backend-hetzner.yml` und `hetzner-backend.compose.yml` und `docker-compose.demo.yml`. Ohne diesen Wert crasht der Container beim Start, weil `config.py` `Field(..., min_length=16)` required hat.
- **PRE_DEPLOY_CHECKLIST.md**: `ANONYMIZATION_SALT` zu Secrets-Checkliste hinzugefuegt.
- **Dev-Setup-Script**: `scripts/dev-setup.ps1` erstellt — automatisiert venv, deps, .env, Smoke-Test, Typecheck, Lint, Build auf Windows.
- **Cross-Reference Audit**: `01_HARNESS.md` Modellrouting konsistent mit AGENTS.md/ULTRAPLAN.md. `tasks.jsonl` W-01..W-10 alle done.

## Surprised by
- `ANONYMIZATION_SALT` war in keinem Deploy-File und keiner Secrets-Liste — ein klassischer "Config-Hardening-Rueckschlag": S9 hat das Feld required gemacht, aber die Deploy-Pipelines wurden nicht mitaktualisiert.
- `docker-compose.demo.yml` hatte `ADMIN_API_KEY: ${ADMIN_API_KEY:-}` (default empty) — das haette auch zu Config-Fehlern gefuehrt.

## Avoided
- Nichts pushen (kein Commit/Force-Push ohne Freigabe)
- Keine Human-Blocker angefasst (FLY_TOKEN, SSH, DNS)

## Next
- Human muss `ANONYMIZATION_SALT` als GitHub Secret setzen (min 16 Zeichen)
- Human muss 4 Deploy-Blocker loesen (FLY_API_TOKEN, SSH-Key, DNS, flyctl)
- Dann: Commit aller Aenderungen + Push

## Post-Session Fixes (waehrend Run-Log-Schreiben entdeckt)
- **E2E+Smoke Test-Isolation**: Wenn beide Testdateien zusammen liefen, gab es 401-Fehler. Ursache: `test_smoke.py` aendert `os.environ["API_KEY"]` in seinem Fixture; `test_rohde_walkthrough_e2e.py` importiert `app.main` bei Modul-Level, wo `create_app()` sofort ausgefuehrt wird. Fix: E2E-Fixture setzt Env-Vars zurueck und ruft `get_settings.cache_clear()` auf, BEVOR `create_app()` laeuft. Ergebnis: 13/13 passing zusammen.
