# Plan: Codex-NN Delta (Abschluss P0d)

## Ziel
P0d vollständig abschließen: Trust-Score-UI + ADR-006 + ONNX-Kalibrierungs-Export.

## Reihenfolge

| # | Task | Team | Files | Dauer |
|---|------|------|-------|-------|
| 1 | ADR-006 schreiben | Delta | `regulatory/adr/006_confidence_calibration.md` | 10 min |
| 2 | Frontend Trust-Score-Panel | Beta | `AiPanel.tsx` erweitern | 15 min |
| 3 | ONNX Calibration Export | Gamma | `ml/inference/onnx_export.py` | 20 min |
| 4 | Full-Suite Verify | Delta | pytest + ruff + black + npm | 10 min |
| 5 | Run-Log + MEMORY.md Update | Delta | `memory/runs/2026-04-29_K-NN-final.md` | 5 min |

## Definition of Done (P0d)
- [ ] ADR-006 existiert und beschreibt Calibration-Architektur + Trade-offs
- [ ] Frontend zeigt `trust_score` als visuellen Indicator (low=rot, medium=gelb, high=grün)
- [ ] ONNX-Export enthält Kalibrierungs-Layer (Platt/Isotonic als ONNX-Node)
- [ ] 78/78 Tests passing, ruff 0, black formatted, npm typecheck/build/lint 0
- [ ] Run-Log geschrieben, MEMORY.md + CLAUDE.md aktualisiert

## Risiken
- ONNX-Export mit sklearn-Modellen (LogisticRegression/IsotonicRegression) kann komplex werden → Fallback: Calibrate nach ONNX-Export via ONNX-Runtime-Custom-Op oder separater Calibration-Node
- Frontend-Build kann durch Cornerstone-WASM Warnungen nicht blockiert werden
