# Plan: Naechste Phase (P0-Closure + P3-Vorbereitung)

## Stand
- K-01..K-34: Code-Stack vollstaendig (78/78 Tests gruen)
- Hermes + Browser Harness integriert
- T-001..T-010: Office-Dokumente noch offen (AGENTS.md: Modelle duerfen nicht direkt editieren)
- T-016..T-022: P3-Vorbereitung noch offen

## Ziel
P0 technisch abschliessen + P3-Vorbereitung starten.

## Reihenfolge

| # | Task | Team | Files | Blocker |
|---|------|------|-------|---------|
| 1 | Stride-Prompts G-H vorbereiten (fuer Lou) | Delta | `memory/runs/2026-04-30_stride_prompts_gh.md` | Keine |
| 2 | Modell-Signing-Pipeline (Sigstore/GPG) | Alpha | `scripts/sign_model.py`, `scripts/verify_model.py` | Keine |
| 3 | Modell-Update-Verfahren dokumentieren | Delta | `regulatory/model_update_procedure.md` | T-016 |
| 4 | Frontend Trust-Score-Visualisierung | Beta | `AiPanel.tsx` Erweiterung | Keine |
| 5 | Full-Suite Verify | Delta | pytest + ruff + black + npm | Alle oben |

## DoD
- [ ] Stride-Prompts G-H als Copy-Paste bereit
- [ ] Sign + Verify Skripte funktionieren
- [ ] Model-Update-Verfahren dokumentiert
- [ ] Trust-Score-Panel visuell ueberarbeitet
- [ ] 78/78 Tests passing
