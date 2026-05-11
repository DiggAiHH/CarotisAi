---
name: 2026-05-10_disclaimer_audit
type: run
agent: Claude Opus 4.7
date: 2026-05-10
phase: A — Pivot-Finalisierung Woche 1
---

## Goal

Code-Disclaimer-Audit Sprint Phase-A-Task #7. Verifiziere im aktuellen P0f-Code-Stack gegen `memory/domain/zweckbestimmung_master_2026-05-06.md` ob (1) Splash-Gate, (2) Watermark, (3) CDS-Modul-Feature-Flag, (4) Audit-Log produktiv und korrekt implementiert sind. Output: Gap-Liste + Codex-Build-Prompt für die Behebung.

## Done

### Befund 1 — Splash-Gate: NICHT konform

- `code/frontend/src/components/AuthGate/AuthGate.tsx` existiert, ist aber ein **Demo-Token-Gate** (technische Zugangskontrolle), kein Forschungs-Splash-Gate.
- Master-Zweckbestimmung §E verlangt einen 3-Punkte-Pflicht-Klick-Dialog mit dem exakten Wording "Forschungsprototyp zur Erfassung von Workflow- und Entscheidungspfad-Daten…" — in der Codebasis NICHT vorhanden.
- Das Audit-Logging der Splash-Bestätigung (Zeitstempel, Nutzer-ID, Sitzungs-ID) ist nicht implementiert.
- **Status:** ❌ Build erforderlich (neue Komponente `ResearchSplashGate`).

### Befund 2 — Watermark: NICHT vorhanden

- `grep -rE "research[ _]use[ _]only|forschungsverwendung|kein medizinprodukt"` auf `frontend/src` und `backend/app` liefert **null Hits**.
- Master-Zweckbestimmung §D verlangt Mikro-Watermark "RESEARCH USE ONLY · Forschungsverwendung · Kein Medizinprodukt" auf jedem Export, PDF-Header, UI-Statusleiste — fehlt vollständig.
- **Status:** ❌ Build erforderlich (UI-Statusleisten-Komponente + Export-Header).

### Befund 3 — CDS-Modul-Feature-Flag: NICHT durchgesetzt — KRITISCHE LÜCKE

Die Master-Zweckbestimmung §G fordert:
- "Stenose-Messung" → "Aufmerksamkeits-Heatmap"
- "Plaque-Vulnerability-Score" → "Forschungsmerkmals-Aggregat (im Backend, nicht UI)"
- Modul E (CDS) per Feature-Flag deaktiviert

Tatsächlicher Code-Zustand:
- `code/backend/app/schemas/inference.py` hat weiterhin `stenosis_pct_nascet: float` und `vulnerability_markers: VulnerabilityMarkers` als **Pflicht-Felder** der API-Response.
- `code/backend/app/schemas/audit.py` speichert `ai_stenosis_pct: float` und `physician_stenosis_pct: float`.
- `code/backend/app/schemas/decision_tree.py` hat `stenosis_pct_nascet: float = Field(ge=0.0, le=100.0)`.
- `code/frontend/src/types/index.ts` typisiert `stenosis_pct_nascet` und `vulnerability_markers` als UI-sichtbare Felder.
- `code/frontend/src/App.tsx` `DEMO_CASES` zeigt explizit `stenosis_pct_nascet: 72`, `vulnerability_markers: { intraplaque_hemorrhage: 0.91, thin_fibrous_cap: 0.78, lipid_rich_necrotic_core: 0.45 }`, `label: "Symptomatisch, rechts ICA"`.
- Kein `feature_flags.py`, kein `CDS_ENABLED=False`, kein Render-Gate in der UI gefunden.
- **Status:** ❌ KRITISCH — der live verifizierte Demo-Stand widerspricht der dokumentierten Zweckbestimmung. Vor jeder Stakeholder-Anbindung MUSS dies gefixt werden, sonst hält die Forschungsprototyp-Behauptung nicht.

### Befund 4 — Audit-Log: KONFORM

- `code/backend/app/services/audit_service.py` ist sauber implementiert.
- `_strip_pii_from_payload` redigiert 9 bekannte PII-Keys (patient_name, patient_id, study_date, accession_number, …) — DSGVO/PS-3.15-konform.
- `AuditEvent` und `DecisionTree` Tabellen vorhanden (siehe `app/db/models`).
- **Status:** ✅ konform. Erweiterung um Splash-Gate-Confirmation-Event nötig (siehe Befund 1).

## Verification

- `find code/frontend/src/components -type d` → AuthGate + Walkthrough vorhanden, kein Splash/Watermark/Disclaimer-Verzeichnis.
- `grep -riE "(research[ _]use[ _]only|forschungsverwendung|watermark|kein medizinprodukt)"` → 0 Hits.
- `grep -riE "(feature[_ ]flag|cds[_ ]?(modul|enabled|disabled))"` → 0 Hits.
- `grep -rE "(stenosis_pct|vulnerability_markers)"` → 12 Hits in Schemas, Types, App.tsx — Pivot ist im Code NICHT vollzogen.

## Gap-Summary

| # | Gap | Schweregrad | Owner | ETA |
|---|-----|-------------|-------|-----|
| G1 | `ResearchSplashGate` Komponente fehlt | hoch | Codex GPT-5.5 | 2d |
| G2 | UI-Watermark + Export-Watermark fehlt | mittel | Codex GPT-5.5 | 1d |
| G3 | CDS-Feature-Flag-Gate (Backend + Frontend) fehlt | **kritisch** | Codex GPT-5.5 + Kimi K2.6 | 3d |
| G4 | Splash-Confirmation-Event in Audit-Log fehlt | mittel | Codex GPT-5.5 | 0.5d |
| G5 | Begriffe-Substitution Backend-Schemas (Befund 3 §G) | hoch | Codex GPT-5.5 | 2d |

**Gesamt-Aufwand:** ~8.5d Codex/Kimi-Sprint. Lou-Review-Aufwand ~1d. Phase-A-Woche-1+2-Sprint, vor Stakeholder-Versand abgeschlossen sein.

## Safety

Keine Patientendaten berührt, kein Live-Code geändert. Audit ist read-only, dokumentarisch.

## Next

1. Codex-Build-Prompt schreiben (siehe `Stride V2/Codex_Prompt_Disclaimer_Build_v1.md`).
2. Stride-V2-Re-Frame-Prompts für die 7 Office-Doks generieren (siehe `Stride V2/Stride_V2_ReFrame_Prompts_v1.md`).
3. Lou stößt Codex-Sprint an, parallel Stride-V2-Doks-Update.
4. Re-Audit nach Codex-Sprint Ende, vor Stakeholder-Versand.
