# Datenschutz-Folgenabschätzung (DPIA) — Carotis-AI

> Skelett für die DPIA nach DSGVO Art. 35. Zu erstellen mit dem Datenschutz-Office des Klinikums Dortmund. Hochrisiko-Verarbeitung gemäß Art. 35 Abs. 3 (besondere Kategorien personen­bezogener Daten + neue Technologie) → DPIA verpflichtend vor Studienstart.

---

## Identifikation

| Feld | Wert |
|------|------|
| **Verantwortlicher** | Klinikum Dortmund (für die Patientendaten am Standort) |
| **Auftragsverarbeiter** | Lou Alshdaifat / DiggAI (für die Anonymisierungs-Pipeline und das Modell-Training) — separater AVV |
| **Studienleiterin** | Aroob Alrawashdeh, Ärztin in Weiterbildung |
| **Datenschutz-Beauftragte:r** | [Name DSB Klinikum Dortmund] |
| **Datum der DPIA** | [zu ergänzen] |
| **Versions-Nr.** | 0.1 (Skelett) |

---

## 1. Beschreibung der geplanten Verarbeitung

### 1.1 Zwecke
- Entwicklung und Validierung eines KI-basierten Clinical Decision Support Systems für die Carotis-Stenose-Diagnostik
- Wissenschaftliche Veröffentlichung der Forschungsergebnisse
- Promotionsarbeit von Aroob Alrawashdeh

### 1.2 Verarbeitete Datenkategorien
- **Besondere Kategorien (DSGVO Art. 9):** medizinische Bilddaten (CT-Angiographie der Halsschlagader), klinische Befunde, Demographika
- **Identifizierende Daten:** Name, Geburtsdatum, Patientennummer (NUR vor Anonymisierung)
- **Pseudonymisierte Daten:** anonymisierte Bilddaten + anonymisierte Befunde + Decision-Trees mit case_id (Hash) und physician_role_hash

### 1.3 Datenquellen
- Klinikum-PACS (retrospektiv: anonymisierte Studien der letzten 5 Jahre)
- Klinikum-PACS (prospektiv: aktuell anfallende CTA-Studien)
- Sarah Specialty Hospital, Amman, JO (separat, mit eigener DPIA in JO; nur anonymisierte Daten kommen ggf. ins gemeinsame Modell)

### 1.4 Empfänger
- **Innerhalb Klinikum:** Aroob Alrawashdeh, Prof. Rohde, autorisierte Klinik-IT
- **Externe Auftragsverarbeiter:** Lou Alshdaifat / DiggAI (Anonymisierungs-Pipeline + Modell-Training auf HAW-Workstation)
- **Wissenschaftliche Beratung:** Prof. Margaritoff, Prof. Tolg, Prof. van Stevendaal, Dr. Islam Shdaifat — erhalten ausschließlich anonymisierte aggregierte Daten oder Modell-Outputs

### 1.5 Speicherdauer
- Original-Identifikatoren (Klinik-Mapping): nach Anonymisierung gelöscht (max. 30 Tage Frist für Korrektur-Möglichkeit)
- Anonymisierte Bilder: 10 Jahre nach Studienabschluss
- Audit-Trail: 25 Jahre (regulatorische Anforderung MDR)
- Modell-Bundles (ohne Patientendaten): dauerhaft, mit Hash + Reproducibility

---

## 2. Notwendigkeits- und Verhältnismäßigkeits-Prüfung

### 2.1 Erforderlichkeit
Die Verarbeitung anonymisierter CTA-Bilder ist **notwendig**, weil:
- Die wissenschaftliche Frage (Reduktion der Inter-Observer-Variabilität durch KI) kann ohne klinische Realwelt-Daten nicht beantwortet werden
- Synthetische / öffentlich verfügbare Datensätze decken die Carotis-Bifurkation in der erforderlichen Qualität nicht ausreichend ab
- Anonymisierte Daten sind das mildeste Mittel — keine Re-Identifizierung möglich

### 2.2 Verhältnismäßigkeit
- Es werden NUR Daten verarbeitet, die für die wissenschaftliche Frage relevant sind (Bilddaten + minimale Demographika für Stratifizierung)
- Anonymisierung erfolgt bevor die Daten den Klinikum-Verarbeitungs­bereich verlassen
- Local-First-Architektur stellt sicher, dass keine Cloud-Provider zwischen Patient und Datenfluss stehen
- DSGVO Art. 5 Datenminimierung ist durch das Anonymisierungs-Profile (DICOM PS 3.15 Basic) realisiert

---

## 3. Risiken für die Rechte und Freiheiten

### 3.1 Identifizierte Risiken

| Risiko | Eintrittswahrscheinlichkeit | Schadenshöhe | Bruttorisiko |
|--------|------------------------------|---------------|--------------|
| Re-Identifizierung trotz Anonymisierung (Linkage-Attacke mit externen Datenquellen) | sehr gering | hoch | mittel |
| Unbefugter Zugriff auf den Studien-Computer (Hacking, Insider) | gering | hoch | mittel |
| Versehentliches Hochladen identifizierender Daten ins Modell-Bundle | sehr gering | hoch | mittel |
| Verlust der Audit-Trail-Integrität | gering | mittel | gering |
| Falsche AI-Vorschläge führen zu fehlerhafter Befundung | mittel (Modell ist neu) | mittel (HITL fängt ab) | gering |

### 3.2 Bezugnahme auf Risk-Register
Detail in `regulatory/risk_register.md`. Insbesondere H-001 (Anonymisierungs-Leck) und H-007 (Rechtsstreit nach Patientenschaden).

---

## 4. Geplante Maßnahmen

### 4.1 Technische Maßnahmen
- **Anonymisierung:** DICOM PS 3.15 Basic Profile, alle 33 PII-Tags entfernt — implementiert in `scripts/anonymize.py` mit pytest-Test-Coverage
- **k-Anonymity:** Mindest-Level k ≥ 5 für jede Quasi-Identifier-Kombination, hart enforced
- **Verschlüsselung:** Edge-Server-Disk LUKS-verschlüsselt, Modell-Bundles signiert (Sigstore)
- **Audit-Trail:** jede Inferenz + Arzt-Entscheidung wird mit Timestamp + Versions-Hash geloggt
- **Air-Gap:** Studien-Computer hat kein Internet-Anschluss; Modell-Updates kommen über signierte USB-Bundles
- **Salt-Rotation:** Anonymisierungs-Salt wird quartalsweise rotiert

### 4.2 Organisatorische Maßnahmen
- **Schulung:** alle Studienbeteiligten (Aroob, Lou, autorisierte Klinik-IT) durchlaufen DSGVO-Schulung des Klinikums vor Studienstart
- **AVV:** schriftlicher Auftrags­verarbeitungs­vertrag zwischen Klinikum Dortmund und Lou/HAW
- **Penetration-Tests:** quartalsweise durch Prof. Margaritoff oder externen Auditor
- **Incident-Response-Plan:** dokumentiert in `regulatory/incident_response.md` (zu erstellen in P1)
- **Patienten-Information + Einwilligung:** dokumentiert in `ethics/patienteninformation.md` und `ethics/einwilligungserklaerung.md`

### 4.3 Architektonische Maßnahmen (Privacy by Design)
- Local-First (siehe ADR-0001): kein Patientendaten-Pfad durch Cloud
- Decision-Tree-Schema validiert PII-Freiheit auf Schema-Ebene (`schemas/decision_tree.schema.json`)
- Modell-Trainings-Daten verlassen das Klinikum nur als anonymisierte Aggregate

---

## 5. Konsultation der Aufsichts­behörde

- **Erforderlichkeit:** wahrscheinlich nicht erforderlich nach DSGVO Art. 36, weil die identifizierten Risiken durch die in Sektion 4 beschriebenen Maßnahmen auf ein angemessenes Restrisiko reduziert werden
- **Trotzdem:** vor Studienstart wird die Datenschutz-Beauftragte des Klinikums die Einschätzung formell bestätigen
- **Falls erforderlich:** Konsultation der Landesbeauftragten für Datenschutz und Informationsfreiheit NRW vor Studienstart

---

## 6. Periodisches Review

Diese DPIA wird reviewed:
- bei jedem Phasen-Wechsel (P1 → P2 → ... → P7)
- bei jedem Anomaly-Triage-Fund mit potenziellem Datenschutz-Impact
- mindestens jährlich
- bei jedem ADR mit „Compliance-Impact: DSGVO" (siehe `regulatory/adr/`)

Reviewer: Datenschutz-Beauftragte:r Klinikum Dortmund + Lou + Aroob.

---

## 7. Genehmigung

| Rolle | Name | Unterschrift | Datum |
|-------|------|--------------|-------|
| Verantwortlicher (Klinikum) | [Geschäftsführung] | _____________ | _____________ |
| Datenschutz-Beauftragte:r | [Name] | _____________ | _____________ |
| Studienleitung | Aroob Alrawashdeh | _____________ | _____________ |
| Auftragsverarbeiter | Lou Alshdaifat | _____________ | _____________ |

---

**Version:** Skelett 2026-04-27
**Status:** Vor Einreichung beim Ethik-Antrag MUSS gemeinsam mit dem Datenschutz-Office Klinikum Dortmund finalisiert werden. Skelett-Inhalte sind als Diskussions-Grundlage gedacht, nicht als finale Position.
