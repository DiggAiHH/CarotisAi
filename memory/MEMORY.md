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

## P0: 17-Step Pre-Deploy Optimization (S1–S17)
- **Datum:** 2026-04-30
- **Run-Log:** [memory/runs/2026-04-30_kimi_17-step-optimizations.md](runs/2026-04-30_kimi_17-step-optimizations.md) + [memory/runs/2026-04-30_kimi_e2e-fix-final.md](runs/2026-04-30_kimi_e2e-fix-final.md)
- **Status:** ✅ Done — alle 17 Schritte implementiert
- **Highlights:**
  - S1: CI-Pipeline (`.github/workflows/ci.yml`) mit lint, test-backend, test-frontend, build, security
  - S2: Deploy Health-Checks (Fly.io + Hetzner) mit curl-Verify
  - S3: Typed API Errors (`code/frontend/src/lib/apiError.ts`)
  - S4: Timeout+Retry (`apiClient.ts` mit AbortController + exponential backoff)
  - S5: ErrorBoundary (`ErrorBoundary.tsx` mit Backend-Logging)
  - S6: Dynamic physicianRoleHash (whoami → Zustand → DecisionForm)
  - S7: CORS List (`config.py` mit comma-split validator)
  - S8: Security Headers (`SecurityHeadersMiddleware` in `middleware.py`)
  - S9: Config Hardening (`anonymization_salt` required, `admin_api_key`, `model_sha` validator)
  - S10: Metrics Auth (`/metrics` protected by `verify_admin_key`)
  - S11: Graceful Shutdown (`InferenceService.close()` + lifespan cleanup, lazy sklearn)
  - S12: Resource Limits (Backend 2G/1.5 CPU, Caddy 256M/0.25 CPU)
  - S13: Caddy Healthcheck (in beiden compose files)
  - S14: Gzip Compression (`GZipMiddleware(minimum_size=1000)`)
  - S15: E2E Stresstest (`tests/test_rohde_walkthrough_e2e.py` — 7/7 passing)
  - S16: Bundle Analysis (`vite-bundle-analyzer` + `npm run analyze`)
  - S17: Pre-Deploy Checklist (`deploy/PRE_DEPLOY_CHECKLIST.md` mit 20 Punkten)
- **Tests:** 100 passed, 5 failed (sklearn fehlt in venv — bekannt), 11 skipped (torch/transformers)
- **Deploy-Blocker:** 4 human steps offen (FLY_API_TOKEN, Hetzner SSH-Key, INWX DNS, flyctl)

## P0: ULTRAPLAN v3 — Harness The Whole Knowledge
- **Datum:** 2026-04-30
- **Run-Logs:** 
  - [Run02: ULTRAPLAN v3 Harness](runs/2026-04-30_Kimi_K26-Run02_ultraplan_harness_v3.md)
  - [Run03: Solo Cleanup](runs/2026-04-30_Kimi_K26-Run03_solo_cleanup.md)
- **Status:** ✅ Done — ULTRAPLAN.md v3 + AGENTS.md v2 + CLAUDE.md v1.2 + Deploy-Bugfixes + Dev-Setup-Script
- **Highlights:**
  - Tool-Anti-Patterns: 11 Pattern mit Warum + Stattdessen
  - E2E-Wissen: Mock-Service, ASGITransport, Unique Tokens, DecisionTreeRequest Schema, Audit dual-auth
  - Anomalien-Register erweitert auf A-01..A-12
  - Memory-Disziplin: 5-Zeilen-Run-Log pro Prompt, Pfad-Konvention, MEMORY.md Update-Regel
  - **Kritischer Deploy-Bugfix:** `ANONYMIZATION_SALT` fehlte in allen Deploy-Files (hetzner-compose, demo-compose, deploy-workflow) — ohne diesen Wert crasht der Container
  - **E2E Test-Isolation:** Env-Var-Reset in Fixture + `get_settings.cache_clear()` — 13/13 (Smoke+E2E) passing zusammen
  - Dev-Setup-Script `scripts/dev-setup.ps1` fuer Windows
  - **Test-Baselines:** 100 passed, 5 failed (sklearn), 11 skipped (torch/transformers)

## P0: Code-Stack Init
- **Datum:** 2026-04-27 bis 2026-04-29
- **Run-Log:** [memory/runs/2026-04-29_kimi_e2e_verification.md](runs/2026-04-29_kimi_e2e_verification.md)
- **Status:** ✅ Done — K-01 bis K-16 alle passing
