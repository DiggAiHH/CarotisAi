# Carotis-AI - Gespraechsstand fuer Dr. Aroob

**Stand:** 2026-05-11  
**Ziel:** 15-Minuten-Briefing fuer das heutige Gespraech mit Dr. Aroob. Fokus: was ist gebaut, was ist der neue Frame, was darf man Prof. Rohde/Margaritoff sagen, was ist noch nicht fertig.

---

## 1. Kurzfassung

Carotis-AI ist nicht mehr nur ein Konzept fuer einen KI-Diagnoseassistenten. Der belastbare Stand ist jetzt:

> **Forschungsprototyp fuer Carotis-CTA-Workflow, Decision-Tree-Capture und erklaerbare Aufmerksamkeits-Heatmaps. Kein Medizinprodukt, keine klinische Entscheidungsgrundlage, keine automatische Befundausgabe.**

Der alte MDR-Class-IIa-Pfad bleibt als Langfrist-Option, ist aber fuer die Promotion und Lous Bachelorarbeit zu schwer. Der neue Ansatz ist pragmatischer: erst Forschungswerkzeug, Ethik, retrospektive Auswertung, Workflow-Daten und Publikation. Klinische CDS-Funktionalitaet wird technisch deaktiviert oder hinter Feature-Flags gehalten.

---

## 2. Was Aroob heute wissen muss

| Thema | Neuer Stand |
|---|---|
| Projekt-Frame | Forschungsprototyp statt Medizinprodukt/Diagnoseassistent |
| Zweck | Workflow-, Reading-Time-, Annotation- und Decision-Tree-Daten erfassen |
| KI-Rolle | Heatmap/Overlay als Forschungs-Referenz, nicht Diagnose oder Therapieempfehlung |
| Datenschutz | Local-first bleibt unverhandelbar; keine Patientendaten in Cloud oder externe APIs |
| Demo | `https://carotis.diggai.de/` und `https://api.carotis.diggai.de/` laufen auf Hetzner, Fly.io ist kein Ziel mehr |
| Daten | Nur synthetische Demo-DICOMs online; echte Daten erst nach Rohde, Ethik, DSGVO |
| Kritische offene Luecke | Code muss noch final sichtbar auf Forschungsprototyp getrimmt werden: Splash-Gate, Watermark, CDS-Flag, UI-Begriffe |

---

## 3. Full Stack - Backend

**Vorhanden:**

- FastAPI Edge-Backend mit Health-, Inference-, Decision-Tree-, Audit- und Demo-Endpunkten.
- SQLite lokal, append-only AuditEvent-Mechanik.
- DICOM-Anonymisierung nach DICOM PS 3.15 in der Pipeline.
- ONNX Runtime fuer lokale Inferenz.
- Grad-CAM/HiResCAM-Komponenten fuer erklaerbare Heatmaps.
- Confidence Calibration / Trust Score Service als Forschungsmetrik.
- Demo-Token-Gate inklusive Master-Demo-Token fuer kontrollierte Demos.
- Hetzner-Deployment mit Caddy, TLS und Frontend+Backend auf einem Server.

**Neu im Worktree angelegt, aber noch Integrations-/Verifikationsbedarf:**

- `code/backend/app/core/feature_flags.py` fuer Forschungsprototyp/CDS-Gating.
- `code/backend/app/api/routes/splash_confirmation.py` fuer Audit-Logging der Forschungsbestaetigung.

**Nicht als fertig verkaufen:**

- Quantitative Stenose- und Plaque-Marker sind noch in Schemas/UI vorhanden.
- Der Splash-Confirmation-Endpoint ist im aktuellen `app/main.py` noch nicht eingebunden.
- `research_prototype: true` im Health-Response ist laut Master-Zweckbestimmung gewuenscht, aber noch nicht durchgehend verifiziert.

---

## 4. Full Stack - Frontend

**Vorhanden:**

- React 19 + Vite + TypeScript + Tailwind v4.
- Drei-Spalten-Demo: Fallliste, DICOM/CTA-Viewer, AI-Panel.
- Synthetische Demo-Faelle mit Download der erzeugten DICOM-Dateien.
- AuthGate fuer Demo-Token.
- Walkthrough/Tour fuer Rohde-Demo.
- AiPanel mit Confidence/Trust/XAI-Demo.
- DecisionForm fuer aerztlichen Override und Decision-Tree-Capture.
- Mobile/desktop UI-Smoke wurde gegen Live-Domain verifiziert.

**Neu im Worktree angelegt, aber noch Integrations-/Verifikationsbedarf:**

- `ResearchSplashGate` Komponente mit 3 Pflicht-Checkboxen aus der Zweckbestimmung.
- `Watermark` Komponente mit "RESEARCH USE ONLY - Forschungsverwendung - Kein Medizinprodukt".

**Nicht als fertig verkaufen:**

- `App.tsx` rendert aktuell noch `AuthGate` direkt, nicht `ResearchSplashGate -> AuthGate -> Watermark`.
- Demo-Fallkarten und AI-Panel zeigen noch Stenose-Prozent und Vulnerability-Marker. Das widerspricht dem Forschungsprototyp-Frame, solange die CDS-Feature-Flags nicht sauber greifen.
- Cornerstone3D bleibt fuer echte Produktions-DICOM-Interaktion P3/Pilot-Arbeit; die Demo ist synthetisch und fuer Gespraech/Walkthrough gedacht.

---

## 5. Der neue Ansatz in einem Satz

**Alt:** "Wir bauen eine KI, die Carotis-Stenose quantifiziert."  
**Neu:** "Wir bauen ein lokales Forschungswerkzeug, das sichtbar macht, wie Radiologen Carotis-CTA-Faelle lesen, begruenden und annotieren; KI-Heatmaps dienen nur als Forschungs-Overlay."

Das ist fuer Rohde und Aroob besser, weil:

- weniger MDR-/Produkthaftungsdruck am Anfang,
- realistischer fuer eine Dr.-med.-Promotion,
- sauberer fuer Ethikkommission und Datenschutz,
- trotzdem wissenschaftlich stark: Decision-Tree-Harvesting + Workflow-Analyse + XAI,
- Lou kann parallel eine getrennte Bachelor-Schiene bauen: Tool-Entwicklung + DIN-EN-62304-Dokumentation, ohne Aroobs Patientendaten fuer seine Arbeit zu verwenden.

---

## 6. Dual-Track Plan

| Track | Owner | Ergebnis |
|---|---|---|
| Aroob Dr. med. | Aroob + Rohde | klinische Forschungsfrage, Ethik, retrospektive/pilotierte Auswertung, Klinik-Paper |
| Lou Bachelor | Lou + Margaritoff | lokales Workflow-Capture-Tool, Software-Doku, Methodik-/Software-Paper |
| Gemeinsame Schnittstelle | beide | Tool erzeugt Forschungsdaten fuer Aroobs Projekt, bleibt aber sauber dokumentiert und local-first |

**Saubere Trennung:** Bachelor = Tool + Engineering/62304. Aroob-Promotion = klinische Fragestellung + Patientendaten + Auswertung. Keine Doppelverwertung.

---

## 7. Was du Aroob heute sagen kannst

1. "Der wichtigste Pivot ist regulatorisch: Wir nennen es nicht mehr Diagnoseassistent, sondern Forschungsprototyp fuer Workflow- und Decision-Tree-Capture."
2. "Die Demo ist online und technisch greifbar, aber sie nutzt nur synthetische Daten."
3. "Die klinische Entscheidung bleibt voll bei Aerzten. Das Tool gibt keine Therapieempfehlung und soll keine Befunde in Patientenakten schreiben."
4. "Vor Rohde-Versand muss der Code-Disclaimer-Sprint fertig werden: Splash-Gate, Watermark, CDS-Feature-Flags, Audit-Log."
5. "Aroobs realer Aufwand soll klein und klar bleiben: klinische Bewertung, Fragestellung, Rohde-Kommunikation, spaeter Fallauswertung. Nicht Software bauen."
6. "Lou kann das technische System und seine Bachelorarbeit parallel tragen, ohne Aroobs Promotionsdaten in die Bachelorarbeit zu ziehen."

---

## 8. Risiken ehrlich benennen

| Risiko | Was dazu sagen |
|---|---|
| Demo sieht aktuell noch nach Diagnose-Tool aus | Wird vor Stakeholder-Versand technisch umgestellt; Audit vom 10.05 hat die Luecke sauber dokumentiert |
| Aroob ist aktuell nicht als Dortmund-Mitarbeiterin zu formulieren | Dortmund/Rohde-Bezug historisch und fachlich formulieren, nicht als aktuelle Anstellung behaupten |
| Rohde koennte "KI-Diagnose" ablehnen | Frame auf Forschungsbeobachtung, Workflow, Decision-Tree-Daten und Ethik senken |
| Ethik/DSGVO bleibt Arbeit | Ja, aber genau dafuer ist Local-First + Forschungsframe + anonymisierte retrospektive Daten gedacht |
| ML-Performance noch nicht klinisch bewiesen | Korrekt: Demo ist Prototyp, echte Validierung kommt erst nach P1/Pilot |

---

## 9. Heute konkrete Entscheidungen mit Aroob

1. Ist Aroob mit dem neuen Forschungsprototyp-Frame einverstanden?
2. Darf Rohde mit diesem reduzierten, sicheren Frame angeschrieben werden?
3. Soll Margaritoff parallel fuer Lous Bachelor-Track angefragt werden?
4. Wie wird Aroobs aktuelle Rolle exakt formuliert, damit nichts Falsches ueber Dortmund/NVIDIA im Text steht?
5. Wer gibt den finalen Go fuer Code-Disclaimer-Sprint und danach Rohde-Mail?

---

## 10. Naechste technische To-dos vor externem Versand

1. `ResearchSplashGate` in `App.tsx` vor `AuthGate` integrieren.
2. `Watermark` dauerhaft in der App rendern.
3. `splash_confirmation.router` in `app/main.py` registrieren.
4. Health-Response um Forschungsprototyp-Marker erweitern.
5. Public Inference Response/UI von Stenose-Prozent und Vulnerability-Marker entkoppeln oder strikt hinter Feature-Flags verstecken.
6. Tests: Backend focused + Frontend Vitest + Playwright Live-Smoke.

**Status fuer heute:** Gespraechsbereit, aber noch nicht stakeholder-send-ready, solange Punkt 1-6 nicht verifiziert sind.
