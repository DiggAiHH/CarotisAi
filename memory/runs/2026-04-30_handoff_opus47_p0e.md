---
name: 2026-04-30_handoff_opus47_p0e
type: handoff
to: opus-4.7
from: kimi-k2.6 + sonnet-4.6 + codex-5.3
session: K-35..K-46 + T-017
---

## TL;DR

P0e (Code-Stack Robustheit) ist **vollständig abgeschlossen**. Alle 6 bekannten Anomalien sind FIXED. 101/101 pytest grün, 12/12 Vitest grün, build+lint+typecheck 0 Fehler. T-017 (Modell-Update-Verfahren) done. Nächster Schritt: T-001 abschließen → T-004..T-008 → T-009/T-010 (human) → T-012 (Opus: Rohde-Meeting).

---

## Phase Status

| Phase | Status | Note |
|-------|--------|------|
| P0e Code-Stack | ✅ DONE | K-01..K-34 + K-35..K-46 alle done |
| P0 Stride-Prompts | 🔄 T-001 in progress | Prompt G läuft (Floy-Recherche) |
| P0 Rohde-Meeting | ⏳ T-012 blocked | wartet auf T-010 (Rohde-Antwort) |
| P1..P7 | 🔒 blocked | wartet auf P0 |

---

## Delta seit letztem Opus-Handoff (2026-04-29)

### Code (K-35..K-42) — Kimi K2.6

| Task | What | Files | Verify |
|------|------|-------|--------|
| K-35 | Model-Update-Verfahren | `regulatory/model_update_procedure.md` | Margaritoff-Review pending |
| K-36 | Reasoning-Alignment-Loss ADR | `regulatory/adr/ADR-0007-reasoning-alignment-loss.md` | Opus-approved |
| K-37 | AuditService Rewrite | `backend/app/services/audit_service.py` | 11 tests pass |
| K-38 | Frontend Contract Cleanup | `frontend/src/lib/apiClient.ts`, `types/index.ts` | dedup done |
| K-39 | Vitest Baseline | `vitest.config.ts`, `vitest.setup.ts`, 4 test files | 12/12 pass |
| K-40 | Security Hardening | `inference.py`, `config.py`, `test_security_hardening.py` | 3 tests pass |
| K-41 | E2E Verify Scripts | `scripts/verify_demo_e2e.ps1` + `.sh` | ASCII-only, 5 checks |
| K-42 | Final Verification | all | 101 pytest ✓, ruff ✓, black ✓, typecheck ✓, build ✓, vitest ✓ |

### Dead-Code Removal (K-43..K-46) — Kimi K2.6

| Task | Removed | Updated refs |
|------|---------|--------------|
| K-43 | `backend/app/api/router.py` (orphaned) | `test_smoke.py` |
| K-44 | `ml/export_onnx.py` (duplicate) | `test_ml_pipeline.py` |
| K-45 | stale `frontend/src/services/api.ts`, `types/api.ts` | `apiClient.ts` is SSoT |
| K-46 | `frontend/src/components/AIPanel.tsx` (old) | `AiPanel/AiPanel.tsx` is SSoT |

---

## Tech State (verifiziert 2026-04-30)

```
pytest:        101 passed, 2 skipped (mlflow missing — non-blocking)
ruff:          0 errors
black:         0 errors
npm typecheck: 0 errors
npm lint:      0 errors
npm build:     SUCCESS (Cornerstone WASM warnings expected)
npm test:      12/12 Vitest pass
```

**Active issues (non-blocking):**
- Windows PowerShell + black/ruff emoji output → RemoteException (use `--quiet`)
- mlflow missing → 2 pytest skips in `test_ml_pipeline.py`
- Cornerstone `fs`/`path` externalized warnings in build → expected

**Anomalies: 0 open / 6 fixed**

---

## Open Tasks (opus-relevant)

| ID | Phase | Model | Title | Blocked by | Status |
|----|-------|-------|-------|------------|--------|
| T-001 | P0 | sonnet | Stride Prompt G: Floy-Recherche | — | 🔄 in_progress |
| T-004 | P0 | sonnet | Stride Prompt C: Exposé | T-003 | ⏳ pending |
| T-005 | P0 | sonnet | Stride Prompt D: Tech-Description | T-004 | ⏳ pending |
| T-006 | P0 | sonnet | Stride Prompt E: Value-Proposition | T-005 | ⏳ pending |
| T-007 | P0 | sonnet | Stride Prompt F: Anschreiben | T-006 | ⏳ pending |
| T-008 | P0 | sonnet | Stride Prompt B: CV-Integration | T-007 | ⏳ pending |
| T-009 | P0 | human | Lou: Mail-Komplettierung + Versand | T-008 | ⏳ pending |
| T-010 | P0 | human | Rohde: Antwort abwarten | T-009 | ⏳ pending |
| T-012 | P0 | **opus** | **Rohde-Meeting Vorbereitung** | T-010 | ⏳ **pending** |
| T-013 | P0 | human | Meeting durchführen | T-012 | ⏳ pending |

**T-017 done** (P4-Vorbereitung: Modell-Update-Verfahren) — `regulatory/model_update_procedure.md` existiert.

---

## Routing Matrix (Opus-relevant)

| Task Type | Model | Budget | Notes |
|-----------|-------|--------|-------|
| Architektur-Entscheidungen, ADRs, regulatorische Texte | **Opus 5.7** | 1 | T-012, T-015, T-025 |
| Code-Implementation, Bug-Debug, Office-Drafts | Sonnet 5.6 | 2 | T-001..T-008, K-35..K-46 |
| Atomare Edits, Verify/Build, MEMORY-Updates | Haiku 5.5 | 4 | Status-Updates, Lint-Fixes |
| Medizinische/regulatorische Entscheidungen | **Opus 4.7 only** | 1 | DSGVO, MDR, Ethik |

---

## Inbox for Opus

1. **T-012** (Rohde-Meeting Prep): Wenn T-010 frei wird (Rohde antwortet), ist Opus der Blocker. Meeting-Kit in `06_ROHDE_MEETING_KIT.md` existiert, muss ggf. auf aktuellen Stand geprüft werden.
2. **K-35** (Modell-Update-Verfahren): `regulatory/model_update_procedure.md` wurde geschrieben, braucht noch Margaritoff-Review + DSB-Klinikum-Review (Opus kann Review-Framing liefern).
3. **P1-Readiness**: Hardware-Spec (`regulatory/hardware_spec.md`) und AVV (`regulatory/avv_local_first_template.md`) sind P1-Ready. Wenn Rohde Go gibt, kann P1 sofort starten.

---

## YOUR TASKS, OPUS 4.7

1. **Read this handoff** + `CLAUDE.md` + `AGENTS.md` + `MEMORY.md`.
2. **Update CLAUDE.md** Phase-Status: P0e → DONE, setze T-001..T-010 entsprechend aktuellen Stand (wenn T-001 done → update, etc.).
3. **Update MEMORY.md** mit neuen Run-Log-Zeigern (dieser Handoff + K-35..K-46 Runs).
4. **Update AGENTS.md** Footer-Datum.
5. **Give next guidance** — entweder:
   - Struktur für T-012 (Rohde-Meeting Prep) vorbereiten, ODER
   - Review-Framing für K-35 (Modell-Update-Verfahren) an Margaritoff, ODER
   - P1-Readiness-Checkliste erstellen (was genau passiert wenn Rohde "Ja" sagt).

Do not generate code. Update docs, then give structure guidance.
