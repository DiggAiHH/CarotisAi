# Auftragsverarbeitungsvertrag (AVV) — Carotis-AI Local-First

> Stand: 2026-04-29 | Phase: P1-Vorbereitung (blockiert bis Rohde-Go)
> Verantwortlich: Lou (Laith Alshdaifat) / HAW Dortmund | Review: Klinikum-Datenschutzbeauftragter
> Rechtsgrundlage: Art. 28 DSGVO / § 11 BDSG

---

## 1. PARTEIEN

**Auftraggeber (Verantwortlicher):**
Klinikum Dortmund gGmbH  
Beim Kreuztor 6, 44137 Dortmund  
Vertreten durch: Prof. Dr. med. Stefan Rohde (Medizinische Leitung)  
Datenschutzbeauftragter: [Name, Kontakt einfügen]

**Auftragsverarbeiter:**
Laith Alshdaifat (Lou) / Hochschule für Angewandte Wissenschaften (HAW) Dortmund  
[Adresse]  
E-Mail: [Lou's E-Mail]

---

## 2. GEGENSTAND UND DAUER

**Gegenstand:** Entwicklung, Betrieb und Wartung des Carotis-AI Systems — einer lokalen KI-Software zur Unterstützung der Carotis-Stenose-Diagnostik aus CTA-Bildern.

**Dauer:** Beginn mit Unterzeichnung dieses Vertrags; erstmalig befristet auf **3 Jahre** mit automatischer Verlängerung um jeweils 1 Jahr, sofern nicht 6 Monate vor Ablauf gekündigt wird.

**Kündigungsfrist:** 6 Monate zum jeweiligen Vertragsende.

---

## 3. ART, UMFANG UND ZWECKE DER VERARBEITUNG

### 3.1 Verarbeitete Daten

| Datenkategorie | Beispiele | Speicherort |
|---------------|-----------|-------------|
| **DICOM-Bilddaten** | CTA-Scans der Carotis-Arterien | Edge-Server (lokal, LUKS-verschlüsselt) |
| **Strukturierte Befundungsdaten** | Stenosegrad, Plaque-Typ, AI-Score | SQLite-Datenbank (lokal) |
| **Freitext-Begründungen** | Ärztliche Entscheidungsbegründungen (anonymisiert) | SQLite + JSON (lokal) |
| **Audit-Logs** | Zeitstempel, User-Hash, Modell-Version | SQLite (lokal, append-only) |
| **Metadaten** | SHA-256-Hashes, numerische Werte | SQLite (lokal) |

### 3.2 Zwecke

1. **Entwicklung:** Verbesserung des MFSD-UNet-Modells durch Training auf anonymisierten Daten.
2. **Inferenz:** Lokale KI-gestützte Befundungsunterstützung am Edge-Server.
3. **Qualitätssicherung:** Monitoring der Modell-Performance, Audit-Trail.
4. **Forschung:** Wissenschaftliche Publikation (nur aggregierte, anonymisierte Daten).

### 3.3 Wichtig: Keine Cloud-Verarbeitung

**Es findet ausschließlich lokale Verarbeitung statt.** Keine Patientendaten werden an Cloud-Dienste (AWS, Azure, Google Cloud, OpenAI, Anthropic etc.) übermittelt.

---

## 4. PFLICHTEN DES AUFTRAGSVERARBEITERS

### 4.1 Technisch-organisatorische Maßnahmen (TOMs)

Der Auftragsverarbeiter implementiert folgende TOMs:

| Maßnahme | Umsetzung | Bezug |
|----------|-----------|-------|
| **Pseudonymisierung** | DICOM PS 3.15 Basic Profile + k-Anonymity ≥ 5 | `scripts/anonymize.py` |
| **Verschlüsselung (Datenträger)** | LUKS Full-Disk-Encryption auf allen SSDs | Hardware-Spec Abschnitt 6 |
| **Verschlüsselung (Übertragung)** | TLS 1.3 für interne API-Kommunikation | `backend/app/main.py` |
| **Integrität** | SHA-256-Checksummen für Modelle und Audit-Events | `AuditEvent`-Tabelle |
| **Verfügbarkeit** | RAID 1 + stündliches Backup zu NAS + UPS | Hardware-Spec Abschnitt 5 |
| **Zugriffskontrolle** | X-API-Key (≥ 32 Zeichen), Rate-Limiting 20/min | `app/core/security.py` |
| **Trennung** | Container-basierte Isolation (Docker/Podman) | `docker-compose.yml` |
| **Audit-Trail** | Append-only SQLite-Tabelle, 10 Jahre Retention | `app/db/models.py` |

### 4.2 Personelle Maßnahmen

- Nur autorisierte Personen (Lou, ggf. HAW-IT) haben Zugriff auf den Edge-Server.
- SSH-Zugang nur via Key-Auth, kein Passwort-Login.
- Administrativer Zugriff nur über lokale Konsole oder Klinikum-Jumphost.

### 4.3 Unterauftragsverarbeitung

Unterauftragsverarbeitung ist nur mit vorheriger schriftlicher Zustimmung des Auftraggebers zulässig. Aktuell **keine** Unterauftragsverarbeiter vorgesehen.

---

## 5. RECHTE UND PFLICHTEN DES AUFTRAGGEBERS

### 5.1 Audit-Recht

Der Auftraggeber hat das Recht, einmal jährlich die Einhaltung der TOMs durch den Auftragsverarbeiter zu überprüfen. Die Überprüfung umfasst:

- Log-Einblick (keine Patientendaten, nur Metadaten)
- Konfigurations-Review
- Penetration-Test (durch Klinikum-IT oder beauftragten Dritten)

### 5.2 Meldepflichten

Der Auftragsverarbeiter meldet dem Auftraggeber unverzüglich (spätestens innerhalb von 24 Stunden):

- Verdacht auf Datenschutzverletzung
- Unautorisierten Zugriff auf den Edge-Server
- Verlust oder Beschädigung von Datenträgern
- Änderungen an der Sicherheitsarchitektur

---

## 6. BEENDIGUNG DES VERTRAGS

### 6.1 Daten-Rückgabe

Bei Vertragsende übergibt der Auftragsverarbeiter:

1. **Alle trainierten Modelle** (ONNX-Dateien + Metadaten) auf verschlüsseltem USB-Stick
2. **Audit-Trail-Export** (SQLite-Backup) als verschlüsseltes Archiv
3. **Dokumentation** (Schema, ADRs, Betriebshandbuch)

### 6.2 Daten-Löschung

Nach erfolgreicher Rückgabe und Verifikation durch den Auftraggeber löscht der Auftragsverarbeiter:

- Alle lokalen Kopien von DICOM-Daten
- Alle Modelle und Trainingsartefakte
- Alle SQLite-Datenbanken
- Alle Backups auf persönlichen Geräten

**Nachweis:** SHA-256-Liste der gelöschten Dateien + Bestätigungsschreiben.

### 6.3 Ausnahme: Anonymisierter Forschungskorpus

Mit schriftlicher Zustimmung des Auftraggebers darf der Auftragsverarbeiter einen **anonymisierten Forschungskorpus** (Decision-Tree-Daten ohne PII, nur aggregierte numerische Werte) für wissenschaftliche Publikationen behalten.

---

## 7. BESONDERE KLAUSELN

### 7.1 k-Anonymity

Die Anonymisierung erreicht **k-Anonymity ≥ 5** für alle exportierten Datensätze. Der Salt wird alle 12 Monate rotiert.

### 7.2 Modell-Update-Verfahren

Neue Modellversionen werden nur via:
- **USB-Lieferung** mit SHA-256-Verifikation, ODER
- **Geschützter Klinikum-Intranet-Pfad**

übermittelt. Kein Download aus dem Internet.

### 7.3 EU AI Act Compliance

Das Carotis-AI System fällt unter **Kategorie: High-Risk AI System (Medizinprodukt)** gemäß Art. 6(1) EU AI Act.

- **Frist:** Vollständige Compliance bis 2. August 2027.
- **Maßnahmen:**
  - Risk Management System (vorhanden: `regulatory/risk_register.md`)
  - Daten-Governance (vorhanden: Anonymisierungs-Pipeline)
  - Technische Dokumentation (vorhanden: ADRs)
  - Logging (vorhanden: Audit-Trail)
  - Menschliche Aufsicht (vorhanden: Arzt bestätigt jede AI-Empfehlung)
  - Robustheit (vorhanden: Auto-Rollback bei Performance-Verlust)

---

## 8. ANHANG

### Anhang A: Technische Sicherheitsmaßnahmen

Siehe `regulatory/adr/` (ADR-001 bis ADR-005) sowie `scripts/anonymize.py`.

### Anhang B: Hardware-Spezifikation

Siehe `regulatory/hardware_spec.md`.

### Anhang C: Datenschutz-Folgenabschätzung (DPIA)

Siehe `ethics/dpia_skelett.md`.

---

## 9. UNTERSCHRIFTEN

| Rolle | Name | Datum | Unterschrift |
|-------|------|-------|-------------|
| Auftraggeber (Klinikum) | Prof. Dr. med. Stefan Rohde | | |
| Auftraggeber (DSB) | [Klinikum-DSB] | | |
| Auftragsverarbeiter | Laith Alshdaifat | | |
| Auftragsverarbeiter (HAW) | [HAW-Rechtsabteilung] | | |

---

*Dieser Vertrag ist eine Vorlage und bedarf der rechtlichen Prüfung durch die Rechtsabteilung des Klinikums Dortmund und der HAW Dortmund.*
