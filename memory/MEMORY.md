# Carotis-AI — Long-Term Memory

## Phase A: Schema v0.3 — Override-Capture + CDSiC-Taxonomie
- **Datum:** 2026-04-29
- **Run-Log:** [memory/runs/2026-04-29_PhaseA-complete.md](runs/2026-04-29_PhaseA-complete.md)
- **Status:** ✅ Done — 44/44 Tests passing, Frontend build SUCCESS
- **Schema:** `schemas/decision_tree.schema.json` v0.3 — `disagreement`-Block mit CDSiC-Override-Reasons
- **Pydantic:** `backend/app/schemas/inference.py` — `Disagreement`-Modell mit Cross-Field-Validator
- **Backend:** `backend/app/services/decision_tree_service.py` — PII-Check auf `override_free_text` + Audit-Event `decision_tree_override`
- **Frontend:** `DecisionForm.tsx` — Bedingte Override-UI, `types/decision.ts` — `Disagreement`-Interface
- **Tests:** `tests/test_decision_tree_override.py` — 6/6 passing

## P1-Prep: Hardware-Spec + AVV-Vorlage
- **Datum:** 2026-04-29
- **Run-Log:** [memory/runs/2026-04-29_kimi_p1_prep.md](runs/2026-04-29_kimi_p1_prep.md)
- **Status:** ✅ Done — beide Dokumente geschrieben
- **Hardware:** 3 Optionen (Budget 4-5k€, Mittel 8-10k€ EMPFOHLEN, Premium 15-20k€)
- **AVV:** Art. 28 DSGVO / §11 BDSG, TOMs, Audit-Recht, EU AI Act Frist 2.8.2027

## P0c: Phase C — HiResCAM Evaluation
- **Datum:** 2026-04-29
- **Run-Log:** [memory/runs/2026-04-29_kimi_phase_c.md](runs/2026-04-29_kimi_phase_c.md)
- **Status:** ✅ Done — 66/66 Tests passing
- **Ergebnis:** HiRes-CAM 14x mehr Pixel, 18x schärfer, 1.6x schneller als Grad-CAM
- **ADR:** `regulatory/adr/005_hirescam_xai.md`

## P0c: Phase B — Transformers-PII-Layer
- **Datum:** 2026-04-29
- **Run-Log:** [memory/runs/2026-04-29_kimi_phase_b.md](runs/2026-04-29_kimi_phase_b.md)
- **Status:** ✅ Done — 61/61 Tests passing
- **Modell:** `OpenMed/OpenMed-PII-German-ClinicalLongformer-Base-149M-v1` (Apache 2.0)
- **Architektur:** Layered (Regex → Spacy → Transformers) mit Ensemble-Dedupe
- **ADR:** `regulatory/adr/004_transformers_pii_layer.md`

## P0b: Free-Text-Notes + PII-Detection
- **Datum:** 2026-04-29
- **Run-Log:** [memory/runs/2026-04-29_kimi_p0b_implementation.md](runs/2026-04-29_kimi_p0b_implementation.md)
- **Status:** ✅ Done — K-23 bis K-27 alle passing

## P0a: Demo-Robustness
- **Datum:** 2026-04-29
- **Run-Log:** [memory/runs/2026-04-29_kimi_e2e_verification.md](runs/2026-04-29_kimi_e2e_verification.md)
- **Status:** ✅ Done — K-17 bis K-22 alle passing

## P0: Code-Stack Init
- **Datum:** 2026-04-27 bis 2026-04-29
- **Run-Log:** [memory/runs/2026-04-29_kimi_e2e_verification.md](runs/2026-04-29_kimi_e2e_verification.md)
- **Status:** ✅ Done — K-01 bis K-16 alle passing
