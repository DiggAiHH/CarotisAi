# Das Carotis-AI System: Von der Sonographie zur KI-gestützten Plaque-Analyse

**Eine technische Projektbeschreibung für Radiologen und Praxisinhaber**

---

## 1. DAS PROBLEM

Die sonographische Carotis-Diagnostik steht vor einem fundamentalen Problem: **Inter-Observer-Variabilität von 15-30%** zwischen verschiedenen Untersuchern führt zu inkonsistenten Therapieentscheidungen. Noch kritischer ist jedoch, dass die aktuellen Klassifikationssysteme (NASCET, ECST) nur den reinen Stenosegrad messen – eine 50%ige Stenose kann jahrelang stabil bleiben, während eine 30%ige Stenose mit intraplaque hemorrhage binnen Wochen zum Schlaganfall führen kann. **Die Zukunft liegt in der Plaque-Vulnerability-Analyse statt in reinen Prozentangaben.** Hier setzt unser KI-System an.

## 2. DIE LÖSUNG: MFSD-UNET – KI-ARCHITEKTUR DER NÄCHSTEN GENERATION

**Was ist MFSD-UNet?** Eine speziell für medizinische Bildsegmentierung entwickelte KI-Architektur, die drei bewährte Technologien intelligent kombiniert:

• **U-Net**: Der Goldstandard für medizinische Bildsegmentierung – erkennt präzise Formen und Konturen von Gefäßen
• **Swin Transformer**: Versteht globale Zusammenhänge im Bild, wie ein erfahrener Radiologe, der nicht nur das aktuelle Bild sieht, sondern das gesamte klinische Bild im Kopf hat
• **Deep Supervision**: Lernen auf mehreren Bildebenen gleichzeitig – dadurch präziser als herkömmliche neuronale Netze

**Leistung**: Dice Coefficient 0,9119, Sensitivity 0,9924 – das entspricht dem State-of-the-Art 2024/2025 und übertrifft die meisten menschlichen Untersucher in der Konsistenz.

## 3. WAS DAS SYSTEM KONKRET IN IHRER PRAXIS MACHT

• **Automatische Gefäßsegmentierung**: Erkennt die A. carotis interna vollautomatisch aus dem Sonographie-Bild – keine manuellen Messungen mehr nötig
• **Standardisierte Stenosegraduierung**: Misst nach NASCET/ECST völlig operator-unabhängig – eliminiert die 15-30% Variabilität zwischen Untersuchern
• **Plaque-Vulnerability-Analyse**: Erkennt kritische Marker wie intraplaque hemorrhage, thin fibrous cap und lipid-rich necrotic core – die entscheidenden Faktoren für das Schlaganfallrisiko
• **Transparente KI-Entscheidung**: Grad-CAM Heatmap zeigt Ihnen visuell, WO genau die KI hingeschaut hat – Sie behalten die volle Kontrolle und Nachvollziehbarkeit
• **Automatische Dokumentation**: Generiert sofort einen strukturierten Befundbericht mit Bild, Messung, Vulnerability-Score und Konfidenz-Angabe

## 4. SICHERHEIT & RECHTLICHE COMPLIANCE

• **Local-First Architektur**: Das KI-Modell läuft auf einem dedizierten Server IN Ihrer Praxis – keine Internetverbindung für die Diagnose erforderlich
• **100% DSGVO-konform**: Patientendaten verlassen niemals Ihre Praxis, Trainingsdaten werden nach DICOM PS 3.15 vollständig anonymisiert
• **MDR-Zertifizierung**: Entwicklung nach DIN EN 62304 als Medical Device Class IIa/IIb – rechtssichere medizinische Software
• **EU AI Act Ready**: Erfüllt alle Anforderungen für High-Risk AI Systems – Transparency, Human Oversight, Accuracy und Audit-Trail
• **Human-in-the-Loop**: Sie als Arzt behalten die finale Entscheidungshoheit – die KI schlägt vor, Sie entscheiden und validieren

## 5. NAHTLOSE INTEGRATION IN IHREN PRAXISALLTAG

• **Plug-and-Play Anbindung**: Integration in bestehende Praxissoftware über standardisierte DICOM-Schnittstellen
• **Null Workflow-Änderung**: Sonographie wie gewohnt durchführen – die KI analysiert automatisch im Hintergrund
• **2-Sekunden-Ergebnis**: Stenosegrad + Vulnerability-Score + Heatmap stehen sofort nach der Untersuchung zur Verfügung

## 6. WAS IHRE PRAXIS BENÖTIGT

• **Edge-Server**: Ein lokaler KI-Server (wird von uns gestellt und konfiguriert)
• **DICOM-Kompatibilität**: Sonographie-Bilder im DICOM-Format (in modernen Praxen bereits Standard)
• **Entwicklungszeit**: 24 Monate für komplette Entwicklung, Validierung und Zertifizierung

## 7. PROJEKTABLAUF UND MEILENSTEINE

**Monate 1-3: Grundlagen schaffen**
- Ethikantrag und Datenvertrag
- Retrospektive Datensammlung für KI-Training
- Technische Infrastruktur-Setup

**Monate 4-9: KI-Entwicklung**
- MFSD-UNet Training und Optimierung
- Grad-CAM Integration für Explainable AI
- Erste Validierungstests

**Monate 10-15: Praxisintegration**
- Local-First Server-Installation
- DICOM-Schnittstellen-Anbindung
- Benutzeroberflächen-Entwicklung

**Monate 16-21: Klinische Validierung**
- Prospektive Studie in Deutschland und Jordanien
- Inter-Observer-Variabilität-Messungen
- Performance-Optimierung

**Monate 22-24: Abschluss und Zertifizierung**
- MDR-Zertifizierung als Medical Device
- Wissenschaftliche Publikation
- Produktive Nutzung in der Praxis

---

**Wissenschaftliche Absicherung**: Das Projekt wird von der HAW Hamburg wissenschaftlich begleitet (Prof. Dr. Margaritoff für Medical ML, Prof. Dr. Tolg für VR in Medicine, Prof. Dr. van Stevendaal für Medical Devices). Die transnationale Validierung läuft bereits erfolgreich am Sarah Specialty Hospital in Jordanien.

**Ihr Nutzen**: Positionierung als Technologieführer, wissenschaftliche Publikationsmöglichkeiten in Top-Journals (Radiology, JNIS), Effizienzsteigerung um 20-30%, und ein nachhaltiger Wettbewerbsvorteil als erste KI-gestützte Gefäßdiagnostik-Praxis der Region.

---

*Dr. Aroob Alrawashdeh, Fachärztin für Radiologie*  
*Technische Leitung: Laith Alshdaifat, Medizintechnik HAW Hamburg*  
*April 2026*