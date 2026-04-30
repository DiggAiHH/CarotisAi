---
name: 2026-04-29_Codex-NN_Alpha-Beta-Gamma
type: run
model: Sonnet 4.6
---

## Goal
Codex-NN Plan vollständig umsetzen: Confidence Calibration + Trust Score Services (Alpha), Frontend Schema-Sync (Beta), HiResCAM-Dokumentation (Gamma). Delta (Tests/Docs) finalisiert.

## Done
- **Alpha (Backend/API)**:
  - `ConfidenceCalibrationService` implementiert (Platt/Isotonic, ECE/MCE/Brier, save/load)
  - `TrustScoreService` implementiert (composite score: confidence 0.5, calibration 0.3, transparency 0.2)
  - `PredictionResponse` Schema erweitert: `trust_score`, `confidence_bucket`, `calibration_version`
  - `HealthResponse` Schema korrigiert: `model_loaded`/`db_ok` als `bool | None` (fix für `/health/` Liveness-Check)
  - `inference.py` Router: Trust-Score-Berechnung in Prediction-Pipeline eingebaut
  - `health.py` Router: Kalibrierungs-Metriken im Ready-Check
  - `main.py`: Lifespan initialisiert Calibration-Service
  - 12 Calibration-Tests (`test_confidence_calibration.py`) — alle passing
  - Ruff-Fix: `ValidationError` → `AppValidationError` (Kollision mit pydantic), unused `total` entfernt

- **Beta (Frontend/UI)**:
  - `InferenceResponse` Typen synchronisiert: `case_hash` → `case_id`, neue Felder `trust_score`, `confidence_bucket`, `calibration_version`
  - `DecisionTreeCreate`/`DecisionTreeResponse`: `case_hash` → `case_id`
  - `AiPanel.tsx`: Zeigt `calibration_version` statt `inference_ms`, `case_id` statt `case_hash`
  - `DecisionForm.tsx`: `case_id` verwendet
  - Typecheck: 0 Fehler
  - Build: SUCCESS
  - Lint: 0 Fehler, 0 Warnings

- **Gamma (XAI/ML)**:
  - HiResCAM-Tests (`test_gradcam.py`) bereits in vorheriger Session implementiert, 5/5 passing
  - ADR-005 (HiResCAM statt Grad-CAM) dokumentiert

- **Delta (Tests/Docs)**:
  - Full-Suite: **78/78 passing** (keine Regressionen)
  - Quality Gates: ruff 0, black formatted, pytest 78/78, npm typecheck 0, npm build SUCCESS, npm lint 0
  - Smoke-Tests: 6/6 passing (inkl. Health-Fix)

## Surprised by
- Health-Endpunkt 422 wegen `bool | None` vs `bool` — Pydantic v2 ist streng bei Response-Modellen. Schneller Fix durch Nullable-Typen.
- Frontend-Typen waren stark divergent (`case_hash`, `inference_ms`, `gradcam_b64`) — notwendige Sync hat mehr Files betroffen als erwartet.

## Avoided
- Keine Breaking Changes am API-Vertrag (nur Erweiterungen + Fix für Health)
- Keine PII-Leaks (B-14/B-15 eingehalten)
- Keine Code-Duplikation zwischen Frontend-Typen (`types/api.ts` war veraltet/unbenutzt, `types/index.ts` ist Single Source of Truth)

## Next
- Frontend: Trust-Score-Visualisierung in AiPanel (z.B. Farbcodierte Konfidenz-Bar)
- Frontend: Confidence-Bucket-Label (niedrig/mittel/hoch) neben Stenose-%
- Delta: ADR-006 dokumentieren (Confidence Calibration Architektur)
- Gamma: ONNX-Export-Skript um Kalibrierungs-Layer erweitern (Post-Training)

## Memory updates
- `AGENTS.md`: Tech-Stack aktualisiert (scikit-learn 1.8.0, numpy 2.4.4), Test-Count 78
- `CLAUDE.md`: Phase-Status auf P0-Codex-NN-complete setzen
