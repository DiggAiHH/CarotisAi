# Regulatorischer Rahmen: EU AI Act, MDR und DSGVO im Überblick

**KI-gestützte Carotis-Diagnostik: Rechtssichere Implementierung nach deutschem und europäischem Recht**

---

## 1. MDR 2017/745 (Medical Device Regulation)

**Klassifizierung nach Rule 11 Annex VIII:**
- Software zur Diagnose/Überwachung = **Class IIa** (assistive Diagnose, kein autonomes Handeln)
- Unser MFSD-UNet System: Class IIa-konform durch Human-in-the-Loop Design
- **DIN EN 62304 Compliance:** Vollständige Software-Lebenszyklus-Dokumentation mit Risk Management, Validation und Verification
- **Audit-Trail:** Jede KI-Entscheidung wird dokumentiert und ist nachvollziehbar

## 2. EU AI Act (High-Risk AI System)

**Artikel 10 (Data Governance):**
- Trainingsdaten aus Sarah Specialty Hospital und deutscher Praxis sind nach DICOM PS 3.15 vollständig anonymisiert
- Bias-Korrektur durch transnationale Validierung (Deutschland-Jordanien)

**Artikel 13 (Transparency):**
- **Explainable AI:** Grad-CAM Heatmaps zeigen visuell, WO die KI ihre Entscheidung getroffen hat
- Der Arzt sieht transparent, WARUM die KI zu diesem Ergebnis kam

**Artikel 14 (Human Oversight):**
- **HITL-Design (Human-in-the-Loop):** Die KI schlägt vor, der Arzt bestätigt
- Keine autonome Diagnose - finale Entscheidungshoheit bleibt beim Arzt

**Artikel 15 (Accuracy/Robustness):**
- Automatische Self-Checks beim System-Startup
- Batch-Code (.exe/.dmg) garantiert vorhersehbares, reproduzierbares Verhalten

## 3. DSGVO (Datenschutz-Grundverordnung)

**Privacy by Design (Art. 25):**
- Das System wurde von Grund auf datenschutzkonform entwickelt
- Verschlüsselte Datenspeicherung und -verarbeitung

**Local-First Architektur:**
- **Patientendaten verlassen die Praxis niemals**
- Die KI kommt zur Praxis, nicht umgekehrt - keine Cloud-Übertragung

**Anonymisierung:**
- DICOM PS 3.15 De-Identification vor jedem Training
- Keine personenidentifizierbaren Informationen (PII) im System

**Recht auf Vergessenwerden (Art. 17):**
- Lokale Daten können jederzeit vollständig gelöscht werden
- Keine externen Abhängigkeiten oder Cloud-Speicher

## 4. BSI (Bundesamt für Sicherheit in der Informationstechnik)

**Keine externe Angriffsfläche:**
- Keine Cloud-Schnittstelle für Patientendaten
- Keine offenen APIs oder Internetverbindung für die Diagnose erforderlich

**System-Härtung:**
- Das System läuft als "geschlossene Einheit" (Batch-Code)
- Keine Installation von Drittanbieter-Software möglich

**Sichere Updates:**
- Alle Updates sind digital signiert und verschlüsselt
- Nur autorisierte Updates werden vom System akzeptiert

## 5. Zusammenfassung für die Praxis

**"Dieses KI-System erfüllt ALLE regulatorischen Anforderungen für den Einsatz von KI in der deutschen Medizin. Es ist nicht nur legal – es ist vorbildlich."**

✅ **MDR-konform** als Class IIa Medical Device  
✅ **EU AI Act Ready** mit vollständiger High-Risk AI Compliance  
✅ **100% DSGVO-konform** durch Local-First Architektur  
✅ **BSI-Sicherheitsstandards** durch geschlossene System-Architektur  
✅ **Rechtssichere Dokumentation** mit Audit-Trail und Explainable AI  

**Rechtliche Absicherung:** Die Entwicklung erfolgt unter wissenschaftlicher Begleitung der HAW Hamburg (Prof. Dr. Margaritoff für Medical ML, Prof. Dr. van Stevendaal für Medical Devices) und gewährleistet höchste regulatorische Standards.

---

*Erstellt für: Facharztpraxis Gefäßmedizin*  
*Datum: April 2026*  
*Basis: MFSD-UNet Carotis-Diagnostik System*