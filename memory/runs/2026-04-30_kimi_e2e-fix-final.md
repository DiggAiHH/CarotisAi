---
name: 2026-04-30_kimi_e2e-fix-final
type: run
---

## Goal
S15 E2E-Stresstest (`tests/test_rohde_walkthrough_e2e.py`) debuggen — 7 Tests waren auf 422/DB-Fehler.

## Done
- **E2E Test Rewrite**: Komplette Überarbeitung von `tests/test_rohde_walkthrough_e2e.py`:
  1. **Env-Vars vor app-Import**: `os.environ` setzt API_KEY, ADMIN_API_KEY, DATABASE_URL, ONNX_MODEL_PATH, ANONYMIZATION_SALT vor dem Import von `app.main`, da `create_app()` bei Modul-Import sofort ausgeführt wird.
  2. **Gemockter Inference-Service**: Jeder Test bekommt einen eigenen `client`-Fixture mit `MagicMock` + `AsyncMock` für `InferenceService.predict()`, damit kein echtes ONNX-Modell nötig ist.
  3. **ASGITransport**: `httpx.AsyncClient(transport=ASGITransport(app=app))` statt veraltetem `AsyncClient(app=app)`.
  4. **Unique Tokens**: `_make_token()` generiert UUID-basierte Demo-Tokens, um UNIQUE-constraint-Fehler in `demo_tokens` zu vermeiden.
  5. **Korrekte Payloads**: Decision-Tree-Capture nutzt jetzt das exakte `DecisionTreeRequest`-Schema aus `app/schemas/inference.py` (inkl. aller 4 required `vulnerability_markers`-Keys).
  6. **Audit-Auth**: Audit-Trail-Requests senden korrekt sowohl `X-API-Key` als auch `X-Admin-Key` (Router hat `dependencies=[Depends(verify_api_key), Depends(verify_admin_key)]`).
  7. **Unique case_ids**: Verschiedene case_ids pro Test (`d*64` in smoke, `f*64`/`e*64` in E2E), damit die UNIQUE-Constraint auf `decision_trees.case_id` nicht zuschlägt beim Suite-Run.

## Ergebnis
- **E2E Tests**: 7/7 passing
- **Smoke Tests**: 6/6 passing
- **Gesamte Suite**: 100 passed, 5 failed (sklearn fehlt in venv — bekannt), 11 skipped (torch/transformers)

## Surprised by
- `DecisionTreeRequest` required alle 4 Vulnerability-Marker-Keys (`intraplaque_hemorrhage`, `thin_fibrous_cap`, `lipid_rich_necrotic_core`, `systolic_motion_anomaly`) — leeres Dict `{}` reicht nicht.
- `decision_trees` hat UNIQUE-Constraint auf `case_id` — das führt zu Cross-Test-Fehlern wenn verschiedene Testdateien denselben case_id verwenden.

## Next
- S16 (Bundle Analysis) und S17 (Pre-Deploy Checklist) sind bereits erledigt.
- Alle 17 Optimierungsschritte sind damit abgeschlossen.
- Verbleibende Deploy-Blocker (4 Stück) erfordern menschliche Schritte (FLY_API_TOKEN, SSH-Key, DNS, flyctl).
