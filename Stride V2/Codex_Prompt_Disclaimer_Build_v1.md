# Codex Sprint Prompt — Disclaimer-Build (Phase A Woche 1+2)

**Adressat:** Codex GPT-5.5 (primär) + Kimi K2.6 (G3-Backend-Schema-Migration) via GitHub Copilot Chat in IDE
**Auftraggeber:** Lou (`shdaifatss@gmail.com`)
**Quelle:** `memory/runs/2026-05-10_disclaimer_audit.md` Gaps G1–G5
**Master-Referenz:** `memory/domain/zweckbestimmung_master_2026-05-06.md`
**Ergebnis-Erwartung:** alle 5 Gaps geschlossen, neuer Run-Log unter `memory/runs/<datum>_codex_disclaimer_build.md`, alle Tests grün.

---

## Pre-Flight (Codex Pflicht)

```bash
cat ULTRAPLAN.md
cat CLAUDE.md
cat MEMORY.md
ls -t memory/runs/ | head -3
cat memory/domain/zweckbestimmung_master_2026-05-06.md
cat memory/runs/2026-05-10_disclaimer_audit.md
git status --short --branch
git remote -v
```

Stop-Regel: bei roten Tests *vor* Beginn → Lou pingen.

---

## G1 — `ResearchSplashGate` Komponente

**Ort:** `code/frontend/src/components/ResearchSplashGate/`

**Anforderung:**
- Neue React-Komponente, Pflicht-Klick beim Start, *vor* `AuthGate` in `App.tsx` einfügen.
- Wording wörtlich aus Master-Zweckbestimmung §E:
  > Sie sind im Begriff, Carotis-AI zu starten — einen Forschungsprototyp zur Erfassung von Workflow- und Entscheidungspfad-Daten in der Carotis-CTA-Begutachtung.
  >
  > Mit der Bestätigung erklären Sie:
  > 1. Ich nutze dieses Werkzeug ausschließlich zu Forschungszwecken.
  > 2. Ich treffe alle klinischen Entscheidungen eigenständig und stütze sie nicht auf die Ausgaben dieses Werkzeugs.
  > 3. Ich werde keine Werkzeug-Ausgaben in Patientenakten als diagnostische Aussagen übernehmen.
- Drei Checkboxen (alle erforderlich) + "Ich bestätige" + "Abbrechen".
- "Abbrechen" → Sitzung-Ende-Screen ("Bitte schließen Sie das Fenster.")
- "Ich bestätige" → Bestätigung wird mit `sessionStorage` gespeichert (Sitzungs-skopiert, nicht persistent), Nutzer kommt zum AuthGate.
- POST `/api/v1/audit/splash-confirmation` mit Payload `{ session_id, confirmed_at, role_hash, version: "zweckbestimmung_2026-05-06" }` — kein PII.
- TailwindCSS-Styling im bestehenden `slate-950`/`slate-700`-Design der AuthGate.
- Tests: Vitest `ResearchSplashGate.test.tsx` deckt: alle 3 Boxen erforderlich, Abbruch-Pfad, Confirmation-API-Call, sessionStorage-Persistenz.
- Integration: `App.tsx` Wrapper-Reihenfolge `<ResearchSplashGate><AuthGate>{children}</AuthGate></ResearchSplashGate>`.

**Backend-Endpoint:**
- Neuer Route `code/backend/app/api/routes/audit.py` POST `/splash-confirmation` → `audit_service.log_event(event_type="splash_confirmation", ...)`. PII-Strip-Pipe nutzen.
- pytest `code/backend/tests/test_splash_confirmation.py` — 200 + Audit-Event-Anlage, 422 bei fehlenden Feldern.

**Akzeptanzkriterium:** Cold-Open der App zeigt Splash → 3 Boxen + Bestätigung → AuthGate → Demo-Token. Audit-Tabelle hat Eintrag mit Wording-Version-String.

---

## G2 — Watermark UI + Export

**UI-Statusleiste-Watermark:**
- Neue Komponente `code/frontend/src/components/Watermark/Watermark.tsx`.
- Fixiert am unteren Bildschirmrand, halbtransparent (`bg-amber-500/10 text-amber-200`), sichtbar auf jedem Screen.
- Text: "RESEARCH USE ONLY · Forschungsverwendung · Kein Medizinprodukt"
- Mount-Stelle: in `App.tsx` als Sibling neben dem Haupt-Content, immer sichtbar nach Splash+AuthGate.
- Vitest `Watermark.test.tsx` — Text-Match.

**Export-Watermark:**
- Wenn Backend Reports/PDFs/JSON-Exports generiert (suche in `code/backend/app/services/` nach Export-Funktionen): Header-Zeile in jedem Export setzen.
- Für JSON-Exports: Top-Level-Key `_disclaimer: "RESEARCH USE ONLY · Kein Medizinprodukt"`.
- pytest erweitern, dass Disclaimer in jedem Export-Output enthalten.

**Akzeptanzkriterium:** Screenshot-Smoke der Live-Domain zeigt Watermark unten. JSON-Export enthält `_disclaimer`-Feld.

---

## G3 — CDS-Feature-Flag-Gate (KRITISCH)

**Backend (Kimi K2.6 lead):**

- Neue Datei `code/backend/app/core/feature_flags.py`:
  ```python
  from pydantic_settings import BaseSettings

  class FeatureFlags(BaseSettings):
      cds_module_enabled: bool = False  # Master-Zweckbestimmung 2026-05-06: deaktiviert
      stenosis_quantification_exposed: bool = False  # nicht UI, nur Backend-intern
      vulnerability_markers_in_ui: bool = False  # ditto

      class Config:
          env_prefix = "FEATURE_"

  feature_flags = FeatureFlags()
  ```

- `code/backend/app/schemas/inference.py` aufteilen:
  - `InferenceResponse` (öffentlich, was UI bekommt): nur `case_id`, `audit_id`, `captured_at`, `model_version`, `model_sha`, `heatmap_b64`, `confidence_bucket`, `trust_score`, `calibrated`. KEIN `stenosis_pct_nascet`, KEIN `vulnerability_markers`.
  - `InternalInferenceRecord` (nur Backend, Audit, Forschung): behält die quantitativen Felder mit Kommentar `# RESEARCH USE — never returned to UI when feature_flags.cds_module_enabled is False`.

- API-Route `inference.py` filtert die Response durch das Feature-Flag. Wenn `cds_module_enabled is False` → öffentliche Variante.
- `audit.py` Schema bleibt mit `ai_stenosis_pct` für interne Auswertung — das ist ok, weil Audit nicht UI ist.
- pytest erweitern: `test_inference_no_cds.py` — bei default-flags ist `stenosis_pct_nascet` NICHT in der API-Response.

**Frontend (Codex GPT-5.5 lead):**

- `code/frontend/src/types/index.ts` `InferenceResponse` vom Server-Schema neu generieren — quantitative Felder als optional markieren oder ganz entfernen.
- `code/frontend/src/components/AiPanel/AiPanel.tsx` — alle UI-Elemente, die Stenose-% oder Vulnerability-Marker rendern, prüfen und hinter ein `if (featureFlags.cdsEnabled)`-Gate stecken (default: false).
- `code/frontend/src/App.tsx` `DEMO_CASES`-Array umbauen: keine `stenosis_pct_nascet`-Werte, keine `vulnerability_markers`-Dictionary mehr in den Demo-Cases. Stattdessen `attention_heatmap_label` oder `workflow_summary` als forschungs-neutrale Felder.
- `code/frontend/src/lib/i18n` Strings prüfen: keine Vorkommen von "Stenose %", "NASCET", "Plaque-Vulnerability". Ersetzen nach Master-Zweckbestimmung §G.
- Vitest erweitern: `test_no_stenosis_in_ui.test.tsx` — DOM enthält weder "%" noch "NASCET" noch "Vulnerability".

**Akzeptanzkriterium:** `curl https://api.carotis.diggai.de/api/v1/inference/<case_id>` liefert eine Response **ohne** `stenosis_pct_nascet` und **ohne** `vulnerability_markers`. Live-UI zeigt keine quantitativen Stenose-Werte mehr. Forschungs-Heatmap-Overlay bleibt erhalten.

---

## G4 — Splash-Confirmation-Audit-Event

- Bereits in G1 enthalten. Verifizieren dass:
  - `AuditEvent` Tabelle einen `event_type` Eintrag `splash_confirmation` hat
  - `payload_redacted` enthält `version`, `session_id`, `role_hash` (gehashter Demo-Token), `confirmed_at`
  - Read-Endpoint `/audit/events?type=splash_confirmation` listet Confirmations

**Akzeptanzkriterium:** Nach 1 App-Start + Confirmation existiert genau 1 Audit-Event vom Typ `splash_confirmation`.

---

## G5 — Begriffe-Substitution-Sweep

`grep -rE "(Diagnose|Befund|Stenose-Messung|Vulnerability|automatische Quantifizierung|Klinikum-Pilot|Anwender|Nutzer)"` auf `code/frontend/src` und `code/backend/app/api` und Auswertung gegen Master-Zweckbestimmung §G:

| Alt | Neu |
|---|---|
| Diagnoseassistent | Workflow- und Decision-Tree-Capture-Tool |
| Stenose-Messung | Aufmerksamkeits-Heatmap |
| KI-Befund | Forschungs-Referenz-Overlay |
| Plaque-Vulnerability-Score | Forschungsmerkmals-Aggregat (im Backend, nicht UI) |
| automatische Quantifizierung | strukturierte Datenerfassung |
| Klinikum-Pilot | Forschungsbeobachtung |
| Validierung gegen Goldstandard | Übereinstimmungs-Forschung |
| Anwender / Nutzer | Forscher / Forschungsteilnehmer |
| Befund-Output | Forschungs-Datensatz |

**Akzeptanzkriterium:** Grep nach den "Alt"-Begriffen in `code/frontend/src` und `code/backend/app/api` liefert null Hits (außer in Test-Daten / Audit-Schemas wo es um historische Vergleichswerte geht — da bleibt Backend-only OK).

---

## Definition of Done für den Sprint

- [ ] Alle 5 Gaps mit Akzeptanz-Kriterium grün
- [ ] `pytest` 100% grün, `npm test` 100% grün
- [ ] Playwright-Live-Smoke gegen `https://carotis.diggai.de/` zeigt: Splash erscheint, Watermark sichtbar, keine Stenose-% in UI
- [ ] Run-Log nach 5-Zeilen-Schema in `memory/runs/<datum>_codex_disclaimer_build.md`
- [ ] PR-Beschreibung verlinkt auf `memory/runs/2026-05-10_disclaimer_audit.md`
- [ ] Lou-Freigabe-Gate vor Merge

## Stop-Regeln (CLAUDE.md-konform)

- Patientendaten anfassen → STOP
- Modell-Training auf nicht-anonymisierten Daten → STOP
- Code-Änderung ohne Pre-Flight → STOP
- Run-Ende ohne Run-Log → STOP

---

**Lou kopiert diesen Prompt in Codex-Chat (Copilot Pro+) und startet den Sprint.**
