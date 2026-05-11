# Execution Plan — Dual-Track Carotis-AI (Aroob Dr. med. + Lou Bachelor)

**Datum:** 2026-05-10
**Version:** v1.0 — supersedes `strategie_pivot_minimum_effort_2026-05-10.md` §2 (Drei-Säulen-Modell wird beibehalten, aber Authorship-Frame ist jetzt Dual-Track)
**Vorgänger-Anker:**
- Regulatory Pivot: `memory/domain/zweckbestimmung_master_2026-05-06.md`
- Reuse-Strategie + Quellen: `memory/domain/strategie_pivot_minimum_effort_2026-05-10.md`
**Status:** Aktiv. Wartet auf Rohde-Mail + Margaritoff-Mail-Versand.

---

## 0. Authoritative Roles (verbindlich, nicht verhandelbar)

| Person | Rolle | Promotion/Abschluss | Aufwand realistisch |
|--------|-------|---------------------|---------------------|
| **Aroob (Dr. med. Aroob Alrawashdeh)** | Klinische Promovendin | Dr. med., Klinikum Dortmund, Doktorvater Rohde | 80–150h über 18–24 Monate |
| **Lou (Laith Alshdaifat)** | Tech Lead + Co-Investigator | Bachelor HAW Hamburg in Welle 2 (Monat 6+) | ~6 Monate Part-Time-Code + ~2 Monate Bachelor-Schreiben |
| **Prof. Dr. Stefan Rohde** | Doktorvater Aroob, optional externer Bachelor-Co-Betreuer Lou | — | ~15h über 24 Monate |
| **Prof. Dr. Petra Margaritoff** | Bachelor-Erstprüferin Lou (Wunschkandidatin, DIN EN 62304) | — | ~10h Standard-Bachelor-Betreuung |

**Authorship-Regel:** Wer publiziert, nennt seine Beiträge ehrlich (ICMJE 4-Punkte-Test). Aroob = Erst-Autorin Klinik-Paper; Lou = Erst-Autor Methodenpaper; Co-Authorships beidseitig wo Beitrag substantiell. Keine Ghost-Authorship, kein Honorary-Authorship. **Compliance ist Schutz für Aroob, nicht Hindernis.**

---

## 1. Phasen-Struktur (24 Monate)

```
Monat  0   1   2   3   4   5   6   7   8   9  12  15  18  21  24
Phase  [A][--B--][----C----][D][--E--][--F--][G]
       Pivot Setup Tool+Aroob Bachelor Klinik Aroob
       fix  +Ethik Pilot     Lou        Paper Dispu
```

| Phase | Monate | Goal | Owner |
|-------|--------|------|-------|
| **A — Pivot-Finalisierung** | 0–1 | Stride-V2-Re-Frame, Rohde-Pitch raus, Aroob-Sync, Code-Disclaimer-Audit | Lou |
| **B — Setup + Ethik** | 1–3 | Ethikantrag eingereicht, Datenfreigabe Klinikum DO, Tool-Hardening | Aroob (Klinik) + Lou (Code) |
| **C — Tool-Reife + Pilot** | 3–6 | TotalSegmentator-Wrapper produktiv, ImageCAS-Reproduktion läuft, Pilot n=20–50 Klinikum DO | Lou (Tool) + Aroob (klinische Sichtung) |
| **D — Bachelor-Start Lou** | 6–9 | Bachelor offiziell angemeldet, Methodenpaper Säule A Manuskript-Draft | Lou |
| **E — Klinik-Hauptphase** | 9–18 | Aroob retrospektive Hauptauswertung n=200–500, Klinik-Paper Säule B Manuskript | Aroob (First) + Lou (Co) |
| **F — Submissions + Disputation** | 18–24 | Beide Paper submitted, Aroob Disputation, Lou Bachelor-Abgabe | beide |
| **G — Post-Doc / Promotion Lou** | 24+ | Optional Dr.-Ing. oder Dr. rer. medic. für Lou, Multi-Center-Erweiterung | Lou (optional) |

---

## 2. Agent-Fleet — disjunkte Ownership-Grenzen

Verbindliche File-Ownership pro Agent. Crossover nur via Integrations-Runde (siehe §3).

### 2.1 Cloud-Tier (begrenztes Token-Budget)

| Agent | Modell | Domain (read+write) | Hauptaufgabe |
|-------|--------|---------------------|--------------|
| **Claude Opus 4.7** | claude-opus-4-7 | `Stride V2/**`, `papers/manuscripts/**` (Drafting), `memory/domain/**`, ADRs in `docs/adr/**`, Stakeholder-Mails | Architektur-Entscheidungen, Long-Form-Writing, Re-Frame-Doks, Strategie-Updates |
| **Claude Sonnet 4.6** | claude-sonnet-4-6 | Code-Review aller Branches, `papers/**` Polishing, kürzere Office-Doks | Review-Layer vor Lou-Commit, Office-Polish |

### 2.2 Code-Implementation-Tier (€10/Monat-Plan, hohe Frequenz)

| Agent | Modell | Domain (read+write) | Hauptaufgabe |
|-------|--------|---------------------|--------------|
| **Codex GPT-5.5** | codex-5.5 in Copilot | `code/backend/**`, `deploy/**`, `code/scripts/**`, CI-Configs `.github/**`, Statistik-Notebooks `code/analysis/**` | Backend, FastAPI, Hetzner-Deploy, Statistik-Skripte, Reproduktion Guo 2024 |
| **GitHub Copilot Sonnet 4.6** | sonnet-4-6 in IDE | `code/frontend/**`, in-IDE pair programming für `code/**` | Frontend-React, in-line refactor, schnelle Iteration |
| **Kimi K2.6** | kimi-k26 lokal | `code/ml/**` (TotalSegmentator-Wrapper, MONAI-Bundle-Integration, HiResCAM, Trust-Score, Inferenz-Pipeline), Eval-Skripte `code/eval/**` | ML-heavy lifts, große Kontextfenster für Modell-Code, ImageCAS-Pipeline |

### 2.3 Lokaler Tier (unbegrenzt, schnell)

| Agent | Modell | Domain (read+write) | Hauptaufgabe |
|-------|--------|---------------------|--------------|
| **Hermes (Ollama)** | nous-hermes lokal | `memory/**` (alles außer `domain/strategy_*`), `tasks.jsonl`, Run-Logs `memory/runs/**` | Memory-Management, Skill-Routing, Tool-Use ohne Cloud-Token |
| **Caveman (Ollama)** | caveman lokal | Compression-Pipelines, Boilerplate-Generierung, `MEMORY.md`-Index-Pflege | Token-Optimierung, Routine-Schreiben |

### 2.4 Mensch-Layer (Lou)

- **Reviewer-of-Last-Resort:** kein Commit ohne Lou-Freigabe (siehe CLAUDE.md "Solo-Dev mit Claude — Freigabe-Gate")
- **Domain-Owner:** `Stride V2/**` (Office-Docs sind Mensch-Output, Modelle generieren nur Stride-Prompts)
- **Verbindungs-Arbeit:** Rohde-Mail-Versand, Margaritoff-Mail-Versand, Aroob-Sync persönlich, Klinikum-Dortmund-Anonymisierungs-Genehmigung, Ethikantrag-Einreichung

---

## 3. Integrations-Runde (wöchentlich, freitags)

**Ziel:** Disjunkte Parallel-Arbeit der Agents wieder zusammenführen. Verhindert Drift.

**Protokoll (60–90 min):**
1. **Lou** zieht alle Branches lokal (`git fetch --all`), führt `pytest` (Backend) + `npm test` (Frontend) + `pytest code/ml/tests/` (ML).
2. Bei Konflikten: Claude Opus rebased + dokumentiert in `memory/runs/<datum>_integration.md`.
3. **Smoke-Test:** Playwright `chromium_visual_smoke.spec.ts` gegen Live-Domain, danach lokaler ML-Inferenz-Smoke (1 ImageCAS-Sample → TotalSegmentator → HiResCAM → JSON-Output).
4. **Run-Log Schreiben** nach 5-Zeilen-Schema (CLAUDE.md §3) — Caveman generiert Boilerplate, Lou redigiert.
5. **MEMORY.md-Index Refresh:** Hermes prüft, ob neue Memories indiziert werden müssen.

**Stop-Regel:** wenn Smoke-Test 2 Wochen in Folge rot, Plan-Pause + Sonderbesprechung mit Claude Opus für Architektur-Re-Eval.

---

## 4. Phase A — Pivot-Finalisierung (Monat 0–1) — NÄCHSTE 4 WOCHEN

### Woche 1 (ab heute, 2026-05-10)

| Tag | Aktion | Owner | Output |
|-----|--------|-------|--------|
| Mo (heute) | Strategie-Pivot-Datei finalisieren (diese Datei) | Claude Opus | ✅ |
| Mo–Di | Code-Disclaimer-Audit Sprint Start: Splash-Gate-Check, Watermark-Render-Check, CDS-Feature-Flag-Status, Audit-Log-Verifikation | Codex GPT-5.5 + Lou | `memory/runs/2026-05-1x_disclaimer_audit.md` + Test-Suite Erweiterung |
| Di–Mi | Stride-V2-Re-Frame: alle 7 Office-Doks gegen Master-Zweckbestimmung 2026-05-06 abgleichen, "Diagnoseassistent" → "Workflow-Capture-Tool" überall ersetzen | Claude Opus generiert Stride-Prompts; Lou führt aus | 7 aktualisierte `Stride V2/*.docx` |
| Mi–Do | Rohde-Pitch-Mail v4 Drafting (Doppelpaket: Aroob Dr. med. + optional externe Co-Betreuung Lou-Bachelor) — auf Basis 2026-04-30 Reply-Kit + Pivot | Claude Opus | `Stride V2/Rohde_Mail_v4.md` + `.docx` |
| Do | Margaritoff-Mail Drafting (HAW Hamburg, Bachelor-Erstprüferin-Anfrage, Themen-Skizze 1 Seite) | Claude Opus | `Stride V2/Margaritoff_Mail_v1.md` + Skizze-PDF |
| Fr | **Integrations-Runde** + Wochen-Review | Lou | Alles grün, Mails versandbereit |

### Woche 2

| Tag | Aktion | Owner | Output |
|-----|--------|-------|--------|
| Mo | **Mail-Versand:** Rohde + Margaritoff (zeitversetzt 1 Tag) | Lou | Versand-Bestätigung |
| Mo–Di | Aroob-Brief vorbereiten: 2-Seiten-PDF erklärt Setup, ihre realen Aufgaben (80–150h, klar aufgeschlüsselt), Zeitplan, Authorship-Frame | Claude Opus | `Stride V2/Aroob_Setup_Brief_v1.pdf` |
| Di–Mi | Aroob-Sync (30–60 min Video-Call) | Lou | Aroob ja/nein/Bedingungen |
| Mi–Do | TotalSegmentator-Wrapper-Sprint Start: Skeleton im P0f-Backend einbauen, ICA-Inferenz auf 1 ImageCAS-Sample | Kimi K2.6 + Codex | `code/ml/totalseg_wrapper/` lauffähig |
| Do | ImageCAS Download-Skript + Pre-Processing-Pipeline (DICOM → NIfTI → 1.5mm Resampling) | Kimi K2.6 | `code/data/imagecas_loader.py` |
| Fr | **Integrations-Runde** | Lou | Smoke green, Aroob-Status klar |

### Woche 3

| Aktivität | Owner |
|-----------|-------|
| Rohde-Antwort-Erwartungs-Window — falls Antwort: Folgetermin scheduln | Lou |
| Margaritoff-Antwort-Erwartung — falls Antwort: Bachelor-Anmeldungs-Vorbereitung Modul-Stand HAW prüfen | Lou |
| TotalSegmentator-Wrapper produktiv auf 10 ImageCAS-Samples, Dice-Score gemessen | Kimi K2.6 |
| HiResCAM-Overlay an Wrapper-Output anschließen | Kimi K2.6 |
| Trust-Score-Service auf TotalSegmentator-Confidence kalibrieren | Codex |
| Erste E2E-Inferenz-Pipeline durch (DICOM-In → JSON-Out) | Codex + Kimi |

### Woche 4

| Aktivität | Owner |
|-----------|-------|
| Falls Rohde-Antwort positiv: Ethikantrag Klinikum DO Drafting (Aroob-First-Sign, Rohde-Sponsorship, Lou unterstützt redaktionell) | Aroob + Claude Opus support |
| Falls Margaritoff-Antwort positiv: Bachelor-Themen-Anmeldung HAW + Modul-Lückenschluss-Plan | Lou |
| ImageCAS-Reproduktion Guo 2024 Setup: Train/Val/Test-Splits, Eval-Metriken-Skript | Kimi K2.6 |
| Erstes internes Methodenpaper-Outline (Säule A) — Sektions-Struktur + Reuse-Quellen-Liste aus Strategie-Datei §9 | Claude Opus |
| **Phase-A-Review-Meeting** Lou + Claude Opus: Phase-B-Plan finalisieren | Lou |

---

## 5. Phase B — Setup + Ethik + Tool-Hardening (Monat 1–3)

### Aroob-Track (Klinik)

- Ethikantrag Klinikum Dortmund einreichen (Standard-Formular, Rohde-Sponsorship, retrospektive De-Identification nach DICOM PS 3.15)
- DeGIR/DGNR-Register-Abfrage formulieren (Subset Klinikum Dortmund 2019–2025, n geschätzt 200–500 Carotis-Fälle)
- Klinische Fragestellung schärfen (Vorschlag: "Konkordanz Junior- vs. Senior-Radiologe in Plaque-Beurteilung mit/ohne Workflow-Capture-Tool" — messbar, klein, fokussiert)
- Statistik-Plan-Vorgespräch mit Klinikum-DO-Methodiker oder externem Biostatistiker

### Lou-Track (Code)

- TotalSegmentator-Wrapper E2E auf ImageCAS produktiv (Kimi K2.6)
- HiResCAM produktiv auf Wrapper-Output (Kimi K2.6)
- Decision-Tree-Capture-Logger erweitert (Reading-Time, Click-Sequence, Heatmap-Aufmerksamkeit) — bereits 80% in P0f-Stack vorhanden, nur Telemetrie-Erweiterung (Codex)
- Audit-Log SQLite-Schema für klinische Datenerfassung erweitern (Codex)
- HL7/FHIR-Stub für Klinikum-DO-PVS-Integration (Codex) — wird in Phase C aktiviert
- Code-Disclaimer-Audit aus Phase A schließen (alle 4 Punkte: Splash-Gate, Watermark, CDS-Flag, Audit-Log) (Codex + Lou)
- Open-Source-Release-Vorbereitung: Repo-Cleanup, Lizenz (MIT oder Apache 2.0), Zenodo-DOI-Reservierung — Vorbereitung für Software-Paper später (Caveman + Lou)

### Integration

- Wöchentliche Integrations-Runde
- Monatlicher Aroob-Sync: Tool-Demo + Status

---

## 6. Phase C — Tool-Reife + Pilot (Monat 3–6)

### Lou-Track

- ImageCAS-Reproduktion komplett: Dice + Hausdorff + Inferenzzeit gegen Guo 2024 publizierte Werte (Kimi K2.6)
- CADS-Dataset-Augmentation (Hugging Face) — zweites Public-Dataset für Multi-Source-Robustness (Kimi K2.6)
- Methodenpaper Säule A — Manuskript-Draft v0.5 (Methods + Results auf Public-Data-Reproduktion) (Claude Opus + Codex für Tabellen)
- Software-Paper-Skizze (target: *JOSS* oder *SoftwareX*) — Lou Erst-Autor (Claude Opus draft)

### Aroob-Track

- Ethik-Vote (typisch 6–8 Wochen Bearbeitung)
- Pilot-Auswertung n=20–50 Klinikum-DO-Fälle: Aroob liest Fälle, nutzt Tool, Lou hilft technisch — keine klinische Statistik-Auswertung von Lou allein
- Klinik-Paper Säule B — Outline-Phase, Hypothesen-Sharpening
- Konferenz-Abstract DGNR-Frankfurt 03/2027 (falls verpasst, ASNR/ESNR später) — Aroob First Author

### Outputs Ende Phase C

- Funktionsfähiges Tool (P0f-Stack v2 mit ML-Layer)
- Methodenpaper Säule A v0.5
- Pilot-Daten n=20–50
- Open-Source-Release v0.1 auf GitHub
- 1 eingereichter Konferenz-Abstract

---

## 7. Phase D — Bachelor-Start Lou (Monat 6–9)

- **Bachelor-Anmeldung HAW Hamburg** mit Margaritoff als Erstprüferin
- Bachelor-Thema offiziell: *"Entwicklung und DIN-EN-62304-konforme Dokumentation eines lokal ausführbaren, erklärbaren Workflow-Capture-Tools für die Carotis-CTA-Begutachtung als Forschungsprototyp"*
- Schreibphase: 6–8 Wochen Vollzeit-äquivalent (Lou parallel zu Aroob-Tool-Support reduziert)
- Methodenpaper Säule A — finale Submission (target: *European Radiology* oder *Insights into Imaging*)

**Wichtig — Doppelverwertungs-Schutz:** Bachelorarbeit-Scope ist *Tool-Entwicklung + 62304-Audit*, nicht *retrospektive Patientenauswertung*. Aroobs Promotionsdaten gehen NICHT in den Bachelor. Sauberes Wand-Setup.

---

## 8. Phase E — Klinik-Hauptphase (Monat 9–18)

- Aroob: Hauptauswertung n=200–500 Klinikum-DO retrospektiv
- Lou: Tool-Wartung, Statistik-Skripte (Codex), Visualisierungen (Codex), Co-Author-Beitrag Manuskript (Claude Opus polishing)
- Klinik-Paper Säule B Manuskript-Draft v1 (Aroob writes lead, Lou methods+results-tabellen)
- Konferenz-Abstract ASNR oder ESNR oder ECR submission
- Multi-Center-Erweiterung optional: Sarah Specialty Hospital Jordanien als Validation-Cohort (steht in CLAUDE.md als geplanter Validierungspartner)

---

## 9. Phase F — Submissions + Disputation (Monat 18–24)

- Klinik-Paper Säule B → finale Submission (target: *Clinical Neuroradiology*, *European Journal of Radiology*, *RöFo*)
- Aroob Disputation Vorbereitung
- Lou Bachelor-Abgabe + Verteidigung
- Optional: drittes Paper (z.B. Multi-Center oder XAI-Eval) als Bonus für kumulativen Pfad falls relevant

---

## 10. Phase G — Optional Lou-Promotion (Monat 24+)

- Master oder Direkt-Promotion (Dr.-Ing. via TUHH/HAW-Kooperation, oder Dr. rer. medic. via TU Dortmund / RUB Bochum-Schiene)
- Multi-Center-Studie als Promotions-Kern
- DeGIR/DGNR-Register-Vollauswertung als deutscher KI-Register-Beitrag

---

## 11. Konkrete Agent-Zuordnung pro Deliverable (Phase A+B Snapshot)

| Deliverable | Primär-Agent | Reviewer | Mensch-Owner | Frist |
|-------------|--------------|----------|--------------|-------|
| Diese Strategie-Datei | Claude Opus | Claude Sonnet | Lou | ✅ heute |
| Code-Disclaimer-Audit-Report | Codex | Claude Sonnet | Lou | Woche 1 |
| Stride-V2-Re-Frame (7 Doks) | Claude Opus → Stride-Prompt | — | Lou (führt aus) | Woche 1 |
| Rohde-Mail v4 | Claude Opus | Claude Sonnet | Lou | Woche 1 |
| Margaritoff-Mail v1 | Claude Opus | Claude Sonnet | Lou | Woche 1 |
| Aroob-Setup-Brief | Claude Opus | Claude Sonnet | Lou | Woche 2 |
| TotalSegmentator-Wrapper Skeleton | Kimi K2.6 | Codex | Lou | Woche 2 |
| ImageCAS Loader | Kimi K2.6 | Codex | Lou | Woche 2 |
| HiResCAM-Pipeline-Anschluss | Kimi K2.6 | Codex | Lou | Woche 3 |
| Trust-Score Re-Calibration | Codex | Kimi K2.6 | Lou | Woche 3 |
| E2E ML-Inferenz-Smoke | Codex + Kimi | Claude Sonnet | Lou | Woche 3 |
| Ethikantrag-Draft | Claude Opus + Aroob (Klinik-Sprache) | Rohde | Aroob | Woche 4 |
| Methodenpaper-Outline Säule A | Claude Opus | Claude Sonnet | Lou | Woche 4 |
| Run-Logs (alle) | Caveman boilerplate → Lou redigiert | Hermes indiziert | Lou | täglich |
| MEMORY.md Index-Updates | Hermes | — | Lou | wöchentlich |

---

## 12. KPIs / Erfolgs-Metriken

| Phase | Hard-KPI | Soft-KPI |
|-------|----------|----------|
| A | Rohde + Margaritoff antworten innerhalb 14 Tagen | Aroob sagt "ja, ich bin dabei" |
| B | Ethikantrag eingereicht | Code-Disclaimer-Audit grün |
| C | TotalSegmentator-Dice ≥ 0.83 (Guo 2024-Vergleich) | Pilot n≥20 ausgewertet |
| D | Bachelor offiziell angemeldet | Säule-A-Manuskript submitted |
| E | Klinik-Auswertung n≥200 | Säule-B-Manuskript v1 |
| F | Beide Paper akzeptiert oder im Review | Aroob Disputation terminiert |

---

## 13. Risiken & Mitigation (Update)

| Risiko | Wahrsch. | Impact | Mitigation |
|--------|----------|--------|------------|
| Rohde sagt nein | mittel | hoch | Säule A (Public Data) bleibt Standalone-Pfad für Lou-Bachelor; Aroob sucht alternative Klinik (ggf. UKE Hamburg via UKE-Kooperation, schon angedockt) |
| Margaritoff zu busy | mittel | mittel | Tolg oder van Stevendaal als Fallback (beide HAW Medizintechnik) |
| Aroob hat doch keine Zeit (NVIDIA-Job-Last) | mittel | hoch | Bachelor + Methodenpaper sind eigenständig durchführbar; Klinik-Paper auf später schieben oder einen anderen Promovenden am Klinikum DO suchen |
| Ethikvotum negativ | niedrig | hoch | Anpassung Antrag → Vorgespräch mit Klinikum-DO-Ethik-Vorsitz vor Einreichung |
| Doppelverwertung Bachelor ↔ Aroob-Promotion | niedrig | hoch | Sauber getrennte Scopes von Tag 1 dokumentiert (Bachelor=Tool+62304, Aroob=Patientendaten+Klinik) — siehe §7 Doppelverwertungs-Schutz |
| Code-Disclaimer-Audit findet Lücken | mittel | mittel | Phase A löst es bevor irgendwas anderes startet |
| TotalSegmentator-Performance unter Erwartung | niedrig | mittel | Fine-Tuning auf ImageCAS-Subset oder Wechsel auf MONAI headneck_bones_vessels Bundle |
| Aroob-Authorship-Frame wackelt | niedrig | hoch | Real-Effort-Logging im `tasks.jsonl` mit Aroob-Initials, ICMJE-Beitrags-Statement im Manuskript-Methods |

---

## 14. Tool-Stack-Bestand & Lücken (heute)

**Bereits vorhanden (laut CLAUDE.md + P0f-Run17):**
- ✅ React 19 + Vite + TypeScript + Tailwind v4 Frontend
- ✅ FastAPI Backend
- ✅ ONNX Runtime
- ✅ HiResCAM (ADR-005)
- ✅ Trust Score Service (ADR-006)
- ✅ SQLite Audit-Trail
- ✅ Hetzner CX23 Deploy (`carotis.diggai.de`)
- ✅ Master-Demo-Token Backend
- ✅ Decision-Tree-Capture-Logger (Basis)
- ✅ Cornerstone.js DICOM-Viewer (oder OHIF)
- ✅ 101/101 pytest, 12/12 Vitest
- ✅ Engineering-Harness Tools (caveman, codeburn, browser-harness, designlang, skill-team-harness)

**Fehlt (Phase A+B):**
- ❌ TotalSegmentator-Wrapper im Backend
- ❌ ImageCAS-Loader-Pipeline
- ❌ HL7/FHIR-PVS-Stub aktiviert
- ❌ Splash-Gate UI-Verifikation (Audit-offen)
- ❌ Watermark-Render-Verifikation (Audit-offen)
- ❌ CDS-Modul-Feature-Flag explizit deaktiviert (Audit-offen)
- ❌ DICOM PS 3.15 De-Identification-Profil produktiv
- ❌ MONAI Bundle Import-Pipeline (optional Backup zu TotalSegmentator)

---

## 15. Nächste Aktion (heute, 2026-05-10)

1. Lou liest und gibt diese Datei frei (oder kommentiert).
2. Bei Freigabe: Strategie-Datei `strategie_pivot_minimum_effort_2026-05-10.md` mit Pointer auf diese Datei aktualisieren (Header-Note: "Authorship-Frame durch `execution_plan_dual_track_2026-05-10.md` v1.0 ersetzt").
3. Auto-Memory `project_carotis_minimum_effort_pivot.md` Ergänzung: "Zwei-Spuren-Plan v1.0 aktiv ab 2026-05-10."
4. Phase-A-Woche-1-Tasks in `tasks.jsonl` anlegen (8–10 Tasks).
5. Code-Disclaimer-Audit als erster Sprint Codex-anstoßen.

---

**Stand:** 2026-05-10. Dual-Track-Plan aktiv. Wartet auf Lou-Freigabe für Mail-Versand-Welle.
