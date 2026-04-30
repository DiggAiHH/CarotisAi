# Risk Register — Carotis-AI

> Risk-Management-Datei nach ISO-14971-Stil. Erste Version. Wird ab P1 in volles ISO-14971-Format überführt (Hazard-Identifikation, Risk-Estimation, Risk-Control-Measures, Verification).

| Feld | Wert |
|------|------|
| **Stand** | 2026-04-27 |
| **Phase** | P0 |
| **Verantwortlich** | Lou (technische Risiken), Aroob (klinische Risiken), Margaritoff (regulatorische Risiken) |
| **Review-Cadence** | bei jedem Phasen-Wechsel + bei jedem Anomaly-Triage-Fund |

---

## Severity / Likelihood-Skalen

**Severity** (potenzielle Auswirkung):
- **S1 = trivial:** Komfort-Verlust, kein klinischer Impact (z.B. UI-Ladezeit)
- **S2 = minor:** Workflow-Verlangsamung, kein Patientenrisiko (z.B. Modell muss neu geladen werden)
- **S3 = moderate:** klinische Verzögerung, kein direktes Patientenrisiko (z.B. Befund muss konventionell erstellt werden)
- **S4 = major:** Patientenrisiko, korrigierbar (z.B. fehlerhafter Vorschlag, vom Arzt aber abgefangen)
- **S5 = critical:** Patientenschaden möglich (z.B. Anonymisierungs-Leck mit Re-Identifizierungs-Risiko)

**Likelihood**:
- **L1 = sehr unwahrscheinlich** (< 1× pro Jahr)
- **L2 = unwahrscheinlich** (1–4× pro Jahr)
- **L3 = möglich** (1× pro Quartal bis 1× pro Monat)
- **L4 = wahrscheinlich** (mehrmals pro Monat)
- **L5 = häufig** (wöchentlich oder häufiger)

**Risk-Score = Severity × Likelihood** (1–25). Schwellen:
- 1–4: akzeptabel, monitoren
- 5–9: Risk Control Measure erforderlich
- 10–14: starke RCM, Quarterly-Review
- 15–25: STOP, vor Phasen-Wechsel adressieren

---

## Hazard-Register

### H-001 — Anonymisierungs-Leck mit Re-Identifizierungs-Risiko

| Feld | Wert |
|------|------|
| **Hazard** | Trotz DICOM PS 3.15 + k-Anonymity-Check verbleibt im Trainings-Datensatz eine Datei mit re-identifizierbarem PII |
| **Severity** | S5 |
| **Likelihood** | L1 |
| **Score** | 5 |
| **Status** | aktive RCM in `scripts/anonymize.py` (k-Anonymity ≥ 5 hard enforced) |
| **Risk Control Measures** | (1) DICOM PS 3.15 Basic Profile in `anonymize.py`, (2) k-Anonymity-Check ≥ 5 mit hartem Stop, (3) Audit-DB-Mapping nur lokal, (4) quartalsweise Penetration-Test durch Margaritoff oder externen Auditor |
| **Verification** | `scripts/test_anonymize.py::TestKAnonymity::test_below_threshold_rejects` |
| **Restrisiko** | akzeptabel nach RCM, weiter quartals-monitoren |

### H-002 — Modell schlägt falschen Stenosegrad vor → Arzt übernimmt unkritisch

| Feld | Wert |
|------|------|
| **Hazard** | KI-Vorschlag ist falsch, Arzt vertraut zu sehr und bestätigt ohne kritische Prüfung |
| **Severity** | S4 |
| **Likelihood** | L3 (über die Lebensdauer plausibel) |
| **Score** | 12 |
| **Status** | RCM in Design |
| **Risk Control Measures** | (1) Konfidenz-Anzeige ist immer prominent, (2) Grad-CAM-Heatmap zwingend angezeigt, (3) Abweichung von der KI > 10 % triggert Reasoning-Capture-Pflicht-Modus, (4) wöchentliche Performance-Reports (Sensitivity/Specificity) an Aroob, (5) bei Disagreement-Häufung > 15 % auto-Alert an Lou |
| **Verification** | wird in P5 (klinische Validierung) gemessen + dokumentiert |
| **Restrisiko** | dauerhafter Score 6–8 nach RCM (akzeptabel mit Monitoring) |

### H-003 — Daily-Learning-Loop führt zu Modell-Drift / Performance-Regression

| Feld | Wert |
|------|------|
| **Hazard** | Nächtliches inkrementelles Training verschlechtert das Modell statt zu verbessern |
| **Severity** | S4 |
| **Likelihood** | L3 |
| **Score** | 12 |
| **Status** | RCM in Design |
| **Risk Control Measures** | (1) Hold-Out-Test-Set vor jedem Deploy, (2) Auto-Rollback wenn Composite-Metric um > 0.5 % fällt, (3) Replay-Buffer mit historischen Daten verhindert Catastrophic Forgetting, (4) Wöchentliche manuelle Sanity-Checks, (5) Modell-Versionierung mit kompletter Reproducibility |
| **Verification** | wird in P4 (Implementation) als Unit-Tests + in P5 als Lernkurven dokumentiert |
| **Restrisiko** | Score 4–6 nach RCM |

### H-004 — Decision-Tree-Adoption < 30 % → Reasoning-Loss bekommt zu wenig Trainings-Signal

| Feld | Wert |
|------|------|
| **Hazard** | Befunder skippen die 30-Sek-UI, der Reasoning-Korpus wächst zu langsam, der Loss konvergiert nicht |
| **Severity** | S3 (kein Patientenrisiko, aber wissenschaftliche Hypothese unbeweisbar) |
| **Likelihood** | L4 (UX-Forschung zeigt: optionale Eingaben werden oft gemieden) |
| **Score** | 12 |
| **Status** | RCM in `05_DECISION_TREE_HARVESTING.md` Sektion 4 + 8 |
| **Risk Control Measures** | (1) UI optimiert für 30 Sek max, (2) wöchentliche Performance-Mails machen den Effekt sichtbar, (3) Pflicht-Modus für 4 Wochen / Quartal aktivierbar, (4) Default-Werte = AI-Vorschläge (Klick nur bei Widerspruch nötig), (5) Gamification-Badges |
| **Verification** | Adoption-Rate-Monitoring ab P5, monatlicher Bericht |
| **Restrisiko** | Score 4–6 nach RCM |

### H-005 — Edge-Server-Hardware-Ausfall → keine Befundung möglich

| Feld | Wert |
|------|------|
| **Hazard** | Edge-Server fällt aus, Carotis-AI nicht verfügbar, Workflow-Disruption |
| **Severity** | S3 (Befundung kann konventionell weitergehen, aber Workflow-Bruch) |
| **Likelihood** | L2 |
| **Score** | 6 |
| **Status** | RCM in P4 zu definieren |
| **Risk Control Measures** | (1) Fallback-Workflow dokumentiert (konventionelle Befundung ohne KI), (2) ggf. zweiter Edge-Server als Hot-Standby (P7-Skalierungs-Frage), (3) Wartungs-Vertrag mit Hardware-Lieferant |
| **Verification** | DR-Test (Disaster-Recovery) einmal vor P5-Start |
| **Restrisiko** | Score 3 nach RCM |

### H-006 — Modell lernt verzerrte Reasoning-Patterns von einzelnem Befunder (Bias)

| Feld | Wert |
|------|------|
| **Hazard** | In P3/P4 ist Aroob die Haupt-Labellerin → Modell lernt ihre individuellen Präferenzen, nicht die Konsens-Praxis |
| **Severity** | S4 |
| **Likelihood** | L3 |
| **Score** | 12 |
| **Status** | RCM in Design + ADR-0002 referenziert |
| **Risk Control Measures** | (1) Inter-Observer-Subset n=50 mit Zweit-Radiologe in P2, (2) Sarah-Hospital-Daten als kulturelles Korrektiv, (3) Cohen's Kappa Monitoring, (4) ab P5 Multi-Befunder-Capture (mehrere Klinikum-Radiologen, nicht nur Aroob), (5) Bias-Audit als Teil der EU-AI-Act-Doku |
| **Verification** | Bias-Audit-Skript + Cohen's Kappa Tests in P3 |
| **Restrisiko** | Score 4–8 nach RCM |

### H-007 — Rechtsstreit nach Patientenschaden mit "die KI hat es gesagt" als Verteidigung

| Feld | Wert |
|------|------|
| **Hazard** | Patientenschaden tritt auf, juristisch wird die KI mitverantwortlich gemacht; Klinikum / Aroob / Lou sind exponiert |
| **Severity** | S5 (juristisch + Reputations-Schaden) |
| **Likelihood** | L1 |
| **Score** | 5 |
| **Status** | RCM in Design — wesentliches Element |
| **Risk Control Measures** | (1) Audit-Trail jeder Inferenz + jeder Arzt-Entscheidung, (2) explizite Kennzeichnung in der UI: "KI-Vorschlag — Arzt entscheidet", (3) MDR-Class-IIa-Klassifikation als "assistives Werkzeug, kein autonomes System", (4) ärztliche Endkontrolle dokumentiert (HITL), (5) Forschungs-Software-Status in P0–P5 (Studienteilnehmer-Einwilligung explizit) |
| **Verification** | juristische Bewertung durch Anwalt für Medizinrecht in P1 |
| **Restrisiko** | Score 3 nach RCM (juristisch-üblich für CDSS) |

### H-008 — Rohde sagt nein → Promotion stockt

| Feld | Wert |
|------|------|
| **Hazard** | Prof. Rohde lehnt Betreuung ab; Promotion-Pfad bricht weg |
| **Severity** | S3 (kein klinisches, aber persönliches/zeitliches Risiko) |
| **Likelihood** | L2 (gering, weil Vorgespräche bereits positiv waren) |
| **Score** | 6 |
| **Status** | RCM aktiv in `06_ROHDE_MEETING_KIT.md` Sektion 6 |
| **Risk Control Measures** | (1) Plan B: Prof. Tolg als Erstgutachter HAW (kooperative Promotion), (2) Plan C: Prof. van Stevendaal HAW, (3) E-Mail in 24h nach Termin / Antwort, (4) Termin-Folge-Erinnerung in 2 Wochen falls keine Antwort |
| **Verification** | Outcome wird im Run-Log nach Termin dokumentiert |
| **Restrisiko** | Score 3 nach RCM |

### H-009 — Sarah Hospital Kooperation fällt weg (Politik / Logistik)

| Feld | Wert |
|------|------|
| **Hazard** | Sarah-Hospital kann nicht als Multi-Center-Validator dienen; transnationaler USP fehlt |
| **Severity** | S3 |
| **Likelihood** | L2 |
| **Score** | 6 |
| **Status** | RCM definiert in `04_MASTER_PLAN.md` Sektion 9 |
| **Risk Control Measures** | (1) Fallback: nur DE-Validierung mit erweiterter Stichprobe (n ≥ 800), (2) Methodisches Paper bleibt publikationsfähig auch ohne JO-Daten, (3) klinisches Paper wird Single-Center, weniger USP, aber publikationsfähig |
| **Verification** | wird in P5 evaluiert |
| **Restrisiko** | Score 3 nach RCM |

### H-010 — Stride / Office Agent halluziniert klinische Fakten in Stakeholder-Dokument

| Feld | Wert |
|------|------|
| **Hazard** | Office-Agent generiert eine falsche Behauptung in einem Dokument an Prof. Rohde; Glaubwürdigkeit beschädigt |
| **Severity** | S3 |
| **Likelihood** | L3 |
| **Score** | 9 |
| **Status** | RCM aktiv (Aroob-Review-Pflicht in T-009) |
| **Risk Control Measures** | (1) Aroob's Review-Pflicht jeder v2-Datei vor Versand, (2) Globaler Kontext-Block in `07_OFFICE_AGENT_PROMPTS.md` mit harten Constraints, (3) Plaintext-Backup-Mail (`Mail_Aroob_an_Rohde_DRAFT.txt`) als Vergleichs-Referenz, (4) Memory-Eintrag `fb_office_docs.md` (Modelle editieren docx nicht direkt) |
| **Verification** | Aroob-Sign-Off vor T-010 |
| **Restrisiko** | Score 3 nach RCM |

---

## Top-Risiken-Quadrant

```
Severity ↑
   S5 │      H-001●   H-007●
      │
   S4 │              H-002●  H-006●  H-003●
      │
   S3 │                      H-004●  H-005●  H-008●  H-009●  H-010●
      │
   S2 │
      │
   S1 │
      └──────────────────────────────────────────→ Likelihood
        L1      L2       L3        L4       L5
```

---

### H-011 — Freitext-PII-Leak im `free_text_notes`-Feld (P0b)

| Feld | Wert |
|------|------|
| **Hazard** | Arzt schreibt versehentlich Patientennamen, Telefonnummer, oder Klinik-Eigenheiten ins Freitext-Feld; PII gelangt in Trainings-Korpus |
| **Severity** | S5 |
| **Likelihood** | L3 (Freitext-Felder werden in Realität oft uneinheitlich befüllt) |
| **Score** | 15 |
| **Status** | RCM aktiv in P0b (K-24..K-26) |
| **Risk Control Measures** | (1) Live-Validation im Frontend (debounced 500 ms) gegen Backend-PII-Check, (2) Spacy DE-NER (`de_core_news_lg`) + Regex-Fallback für Telefonnummern, IDs, deutsche Namen, (3) Backend rejected mit HTTP 422 wenn PII gefunden — kein Speichern, (4) Audit-Event für jeden Reject (nur Span-Count, keine Inhalte), (5) Quartalsweise Audit der gespeicherten Notes durch externen NER-Lauf, (6) UI-Hint-Text vor jeder Eingabe, (7) `maxLength=2000` als Schutz vor Mass-Insertion |
| **Verification** | `pytest backend/tests/test_pii_detection.py` mit ≥ 20 DE-Namen-Beispielen + Regex-Edge-Cases. Zusätzlich: Quartals-Audit-Skript `audit_free_text_corpus.py` |
| **Restrisiko** | Score 5 nach RCM (S5 × L1) — bleibt durch quartalsweises Audit kontrollierbar |

---

## Lifecycle des Risk Registers

- **Bei jedem ADR:** prüfen, ob neue Hazards entstehen (siehe Sektion „Compliance-Impact" in jedem ADR)
- **Bei jedem Anomaly-Triage (P5+):** prüfen, ob Hazard H-002 / H-003 / H-006 sich verschärft
- **Bei Phasen-Wechsel:** komplette Spalten "Status" und "Restrisiko" reviewen
- **Vor MDR-Audit (P7):** in volles ISO-14971-Format überführen (Hazard-Identifikation-Method, Risk-Acceptance-Criteria, Verification-Records pro RCM)
