# 2026-04-30_opus47_p0f_pivot_plan

---

name: 2026-04-30_opus47_p0f_pivot_plan
type: run
to: kimi-k2.6 + codex-5.5 + sonnet-4.6
session: P0f Plan — Rohde-Demo-Pivot
---

## Goal

Strategie-Shift fuer Rohde-Anbahnung. Alt: Mail mit Konzept + 30-Min-Demo bei Termin. Neu: Mail mit Live-Link + Repo + Webseite. Rohde kann selbst pruefen bevor er antwortet. Anlass: P0e ist done (101/101 Tests, 12/12 Vitest, alle 6 Anomalien fixed). Stride V2 Docs liegen bereit. App + Backend lauffaehig. Webseite fehlt noch.

## Done (in dieser Session)

- Alle 47 Run-Logs ueberflogen, P0e-Handoff vollstaendig integriert.
- CLAUDE.md Phase-Status auf P0f aktualisiert.
- MEMORY.md Pointer auf diesen Run + neue Prompt-Datei eingetragen.
- Prompt-Deliverable `kimi_prompt_p0f_pivot_ready.md` geschrieben — 6 Wellen (W-01..W-12) fuer Kimi K2.6 + Codex GPT-5.5 + Sonnet 4.6.

## Surprised by
Stride V2 ist bereits abgeschlossen (alle 7 Office-Docs in `Stride V2/` vorhanden), aber der `tasks.jsonl` zeigt T-001..T-009 noch als pending. Das ist ein Datenstand-Drift: Doks fertig, Tracker nicht synchronisiert. Wird in W-09 mit Mail v3 zugleich auf done gesetzt.

## Avoided

- Keine Office-Doc-Edits direkt durch Modell — alle Office-Aenderungen nur ueber Stride V3.
- Keine Patientendaten — Webseite + Demo-App nur synthetische Faelle.
- Kein Cloud-Training, nur Cloud-Hosting der oeffentlichen Webseite + Demo-Frontend; Backend-Inferenz bleibt lokal mit getunneltem Demo-Endpoint via Cloudflare Tunnel oder Tailscale.

## New Phase Definition: P0f — Production-Ready Demo-Pivot

**Wann fertig:** Rohde kann unter `carotis.diggai.de` klicken, von dort in `app.carotis.diggai.de` einloggen mit persoenlichem Token, eine 5-Min-Walkthrough-Tour absolvieren, eine eigene synthetische DICOM laden und das Decision-Tree-Capture testen. Mail v3 ist abgeschickt.

**Bloecke (parallel ausfuehrbar nach disjunkten Ownership-Grenzen):**

| ID | Welle | Was | Owner | Tool | Files (disjunkt) |
|----|-------|-----|-------|------|------------------|
| W-01 | A | Public Landing `carotis.diggai.de` | Kimi K2.6 | static HTML+Tailwind | `code/website/` neu |
| W-02 | A | Demo-Deploy + Auth-Gate `app.carotis.diggai.de` | Codex GPT-5.5 | Caddy+Docker+Fly.io | `deploy/` neu, `code/backend/app/core/security.py` |
| W-03 | B | Walkthrough-Mode (5-Step-Tour) im Frontend | Kimi K2.6 | React-driven overlay | `code/frontend/src/components/Walkthrough/` neu |
| W-04 | B | i18n-Dict + UI-String-Audit DE | Kimi K2.6 | i18n.ts | `code/frontend/src/lib/i18n.ts` neu |
| W-05 | B | 30 Synthetic-Cases + 5 Decision-Tree-Beispiele | Kimi K2.6 | extend script | `code/scripts/generate_demo_data.py` (extend) |
| W-06 | C | Rohde-Token-Generator + Audit-Tag | Codex GPT-5.5 | CLI script | `code/scripts/generate_rohde_token.py` neu |
| W-07 | C | Rohde-Anleitung 2-Seiten | Sonnet 4.6 | docx skill | `outputs/Rohde_Anleitung_v1.docx` |
| W-08 | C | Walkthrough-Video-Skript (3 Min) | Sonnet 4.6 | text | `outputs/Rohde_Video_Script_v1.md` |
| W-09 | D | Mail v3 (Stride-Prompt) | Opus 4.7 | Stride V3 prompt | `Stride V3/Anschreiben_Aroob_an_Rohde_v3_PROMPT.md` |
| W-10 | D | Stride V3 Office-Doc-Updates (alle 7) | Opus 4.7 | Stride V3 prompts | `Stride V3/*_PROMPT.md` |
| W-11 | E | Demo-Stresstest + Pre-Send-Smoke | Codex GPT-5.5 | k6+pytest | `tests/test_rohde_walkthrough_e2e.py` |
| W-12 | E | Mail rausschicken (human) | Lou | Gmail | n/a |

**Welle-Timing:** Welle A+B parallel (Tag 1-3). Welle C parallel zu B-Ende (Tag 3-4). Welle D nach A+B+C done (Tag 5). Welle E nach D done (Tag 6-7).

## Memory updates

- CLAUDE.md Phase-Status: P0e DONE → P0f IN PROGRESS hinzugefuegt.
- MEMORY.md Run-Logs-Sektion erhaelt Eintrag fuer diesen Run.
- MEMORY.md Stride-Sektion erhaelt Eintrag fuer V3.
- Neue Datei `kimi_prompt_p0f_pivot_ready.md` als Top-Level-Deliverable.

## Next

Lou liest `kimi_prompt_p0f_pivot_ready.md`, gibt Welle A frei. Kimi K2.6 + Codex GPT-5.5 starten parallel auf disjunkten Datei-Ownerschaften. Nach jeder Welle Verify-Run (pytest + Vitest + Lint + Typecheck + Build). Wenn alle Wellen gruen: Opus generiert Stride V3 Mail v3, Lou versendet.
