# Carotis-AI — Forschungsprojekt-Sachstandsbericht

**Adressatin:** Dr. med. Aroob Alrawashdeh
**Verfasser:** L. Alshdaifat (technische Implementation und Recherche)
**Datum:** 10. Mai 2026
**Zweck:** Sachstandsbericht und Skizze des vorgesehenen klinischen Validierungsbeitrags

---

## 1. Projektüberblick

Carotis-AI ist ein lokal ausführbarer Forschungsprototyp zur strukturierten Erfassung ärztlicher Entscheidungspfade, Lese- und Annotationszeiten sowie Workflow-Charakteristika in der neuroradiologischen Begutachtung von Carotis-Computertomographie-Angiographie-Aufnahmen (Carotis-CTA).

Das Werkzeug ist ausdrücklich ein wissenschaftlicher Forschungsprototyp und kein Medizinprodukt im Sinne der Verordnung (EU) 2017/745 (MDR) bzw. § 3 Nr. 1 MPDG. Es erzeugt keine automatischen Befunde, keine quantitativen Stenose-Werte und keine Therapieempfehlungen. Die ärztliche Beurteilung, Diagnose und Behandlungsentscheidung verbleiben ausschließlich beim behandelnden Arzt. Die vollständige Zweckbestimmung liegt als gesondertes Dokument vor (Anhang A).

---

## 2. Was bisher entwickelt wurde

Die technische Plattform ist in einem lauffähigen Stand und unter `https://carotis.diggai.de/` (Frontend) bzw. `https://api.carotis.diggai.de/` (Backend) erreichbar. Die Infrastruktur ist auf einem dedizierten europäischen Server (Hetzner) gehostet, TLS-verschlüsselt, mit lokalem Audit-Log und ohne externe Cloud-Abhängigkeiten für Patientendaten.

Funktional umfasst die Plattform aktuell:

- **DICOM-Viewer** mit Cornerstone.js für die Darstellung von CTA-Aufnahmen
- **Erklärbare KI-Komponente** (HiResCAM-basierte Aufmerksamkeits-Heatmap als reine Visualisierungsschicht — keine Befundausgabe)
- **Workflow-Capture-Logger** zur Erfassung von Reading-Time, Klick-Sequenzen und Entscheidungspfad-Verzweigungen
- **Confidence-Calibration und Trust-Score-Service** (Platt/Isotonic-Scaling, Composite-Score)
- **DICOM-Anonymisierungs-Pipeline** nach DICOM PS 3.15 De-Identification Profiles
- **Audit-Trail** in lokaler SQLite-Datenbank
- **Splash-Gate-Bestätigungsdialog** mit Forschungs-Use-Only-Erklärung beim Start

Die Backend- und Frontend-Tests sind aktuell zu 100 % grün (101 von 101 pytest, 12 von 12 Vitest), ein End-to-End-Smoke-Test gegen die Live-Domain wurde erfolgreich durchgeführt.

---

## 3. Erkenntnisse aus systematischer Quellen-Recherche (Mai 2026)

Im Vorfeld der klinischen Anbindung wurde eine strukturierte Sichtung internationaler radiologischer Fachpublikationen, regulatorischer Datenbanken und öffentlicher Datenrepositorien durchgeführt. Sichtungsbasis umfasste unter anderem AuntMinnie / AuntMinnie Europe (radiologische Fachpresse), Frontiers in Neurology, MICCAI-Proceedings, ESCR-Konsensus-Dokumente, FDA AI/ML-Enabled Medical Devices-Liste sowie deutsche und europäische Leitlinien-Register (AWMF, DGNR, DeGIR).

### 3.1 Bereits zugelassene KI-Werkzeuge mit Carotis-/Hals-Gefäß-Bezug (FDA-Clearances 2023–2025)

- **Qure.ai qER-CTA** — Erkennung von Large-Vessel-Occlusion in der A. carotis interna und im M1-Segment der A. cerebri media
- **Elucid PlaqueIQ** — bildgestützte Plaque-Analyse
- **Circle Cardiovascular Imaging cvi42 | Plaque** — Plaque-Analyse auf CCTA
- **HeartFlow Plaque (Next Gen)** — methodisch übertragbar, primär koronar
- **Caristo Diagnostics CaRi-Plaque** — methodisch übertragbar, primär koronar

### 3.2 Methodisch relevante Baseline-Studien

- **Guo et al. 2024, *Frontiers in Neurology*** (DOI 10.3389/fneur.2024.1480792) — Deep-Learning-Modell für Carotis-Plaque-Detektion auf CTA, Single-Center, dokumentierte Diagnosezeit etwa 6 Sekunden im Vergleich zu signifikant längeren Radiologen-Lesezeiten. Die Autoren benennen die Single-Center-Limitation explizit und verweisen auf den Bedarf an Multi-Center-Reproduktion.
- **ESCR Konsensus 2022, *European Radiology*** — State-of-the-Art-Empfehlungen zur Carotis-CT/MR-Bildgebung und -Befundung.
- **AWMF S3-Leitlinie 004-028** — Extrakranielle Carotisstenose, Diagnostik, Therapie und Nachsorge (Aktualisierung 2025).

### 3.3 Öffentlich verfügbare Datensätze und Modelle

- **ImageCAS** (1.000 CTA-Fälle mit Dual-Annotator-Konsensus, MIT-Lizenz) als Reproduktions- und Validierungs-Basis.
- **CADS-Dataset** (167 anatomische CT-Strukturen, Hugging Face) als Augmentations-Quelle.
- **TotalSegmentator** (Wasserthal et al., MIT-lizenziert) — segmentiert 104 anatomische Strukturen einschließlich der Aa. carotides internae links und rechts ohne weiteres Training.
- **MONAI Bundle `headneck_bones_vessels`** — Hals-Gefäß-Strukturen.

### 3.4 Deutscher klinischer Anschlusspunkt

- Das **DeGIR/DGNR-Register** dokumentiert nach derzeitigem Stand 9.817 Carotis-Stenting-Fälle aus deutschen Zentren und ist ein etablierter retrospektiver Datenkorpus.
- Die **Klinik für Radiologie und Neuroradiologie am Klinikum Dortmund** unter Direktor Prof. Dr. med. Stefan Rohde verfügt über eine bestehende KI-Forschungs-Kooperation mit der Universitätsklinik Hamburg-Eppendorf auf anonymisierten Daten und hat eine Publikationshistorie auf DeGIR/DGNR-Register-Daten (zuletzt zur Strahlenexposition beim Carotis-Stenting 2019–2021, *Clinical Neuroradiology* 2024). Die Sektion Biomedizinische Physik der Klinik betreut etablierte Promotionsverfahren mit Abschlüssen 2024–2025.

---

## 4. Aktueller Projektstand (10. Mai 2026)

Die technische Aufbauphase (intern als P0f bezeichnet) ist abgeschlossen. Die Plattform ist online erreichbar, in einem definierten und reproduzierbaren Zustand und hat einen Master-Demo-Zugang für autorisierte Nutzer. Der Übergang in die nächste Phase (Setup, Ethik-Vorbereitung, Tool-Hardening und klinische Anbindung) steht aus und ist von der formellen Einbindung des Klinikum Dortmund abhängig.

---

## 5. Vorgesehener klinischer Validierungsbeitrag

Das Projekt ist an einem Punkt, an dem eine klinisch-fundierte Bewertung der bisherigen Recherche-Ergebnisse und eine Schärfung des methodisch-klinischen Pfades benötigt wird. Konkret sind folgende klinische Beiträge vorgesehen:

1. **Klinische Plausibilitäts-Prüfung der Recherche-Befunde** — Einschätzung, welche der unter §3 identifizierten Baseline-Studien und Werkzeuge methodisch und klinisch tragfähig sind und welche klinische Fragestellung am Klinikum Dortmund am sinnvollsten anschließt.
2. **Schärfung der retrospektiven Studien-Fragestellung** — Auswahl einer fokussierten, klar messbaren klinischen Hauptfrage (etwa: Konkordanz Junior- gegenüber Senior-Reader bei der Plaque-Beurteilung mit und ohne Workflow-Capture-Tool; oder Reading-Time-Reduktion in der Carotis-CTA-Begutachtung; oder retrospektive Subgruppen-Analyse innerhalb des Klinikum-Dortmund-DeGIR-Subsets).
3. **Klinische Validierung an einer Pilot-Stichprobe** im weiteren Projektverlauf (n etwa 20–50 retrospektive Klinikum-Dortmund-Fälle, anonymisiert, nach Ethikvotum).
4. **Klinische Erst-Autorenschaft** auf der daraus entstehenden retrospektiven Workflow- und Decision-Tree-Capture-Studie. Inhaltliche Hauptverantwortung für die klinische Methodik, die Diskussion und die Disputation.
5. **Zeitlicher Rahmen** entsprechend der typischen klinisch-retrospektiven Promotionspfade in Deutschland: 18 bis 24 Monate ab Ethikvotum bis zur Disputation.

Die genaue Aufgabenverteilung, Authorship-Vereinbarung gemäß ICMJE-Kriterien sowie die Aufwandsabschätzung können nach einem ersten Sync-Gespräch konkretisiert werden.

---

## 6. Nächste Schritte

### 6.1 Nächster Schritt für Aroob

Vereinbarung eines **30- bis 45-minütigen Sync-Calls** in dieser oder kommender Woche. Inhalte:

- Durchgang dieses Sachstandsberichts und der Zweckbestimmung
- Erste Diskussion einer klinischen Hauptfragestellung
- Abstimmung der Anbindungs-Strategie an Prof. Rohde / Klinikum Dortmund
- Klärung des zeitlichen Rahmens und der Erwartungen

### 6.2 Parallel-Schritt für Lou

Abschluss des **Code-Disclaimer-Audits** (Verifikation der Splash-Gate-Bestätigung, der Watermark-Anzeige, des deaktivierten Befund-Moduls und des Audit-Logs gegen die Master-Zweckbestimmung) sowie die finale Anpassung der sieben Stakeholder-Dokumente in der Forschungsprototyp-Sprache, sodass der Stakeholder-Versand nach dem Sync-Call sauber aufgesetzt ist.

### 6.3 Drei daran anschließende Schritte (gemeinsam, in dieser Reihenfolge)

1. **Anbindung Prof. Rohde / Klinikum Dortmund** durch eine schriftliche Projektvorstellung mit aktuellem Stand, Zweckbestimmung und Skizze der retrospektiven Klinikum-Dortmund-Kooperation. Versand erst nach gemeinsamer Freigabe.
2. **Vorbereitung eines Ethikantrags** am Klinikum Dortmund für die retrospektive Auswertung anonymisierter Carotis-CTA-Fälle, einschließlich Definition der DeGIR-Subset-Eingrenzung und der DICOM-De-Identification-Pipeline. Klinisch-inhaltliche Federführung bei Aroob, institutionelle Sponsorship durch Prof. Rohde, redaktionelle und technische Unterstützung durch Lou.
3. **Pilot-Auswertung an einer kleinen retrospektiven Klinikum-Dortmund-Stichprobe** (n etwa 20–50) nach Ethikvotum. Parallel dazu wird ein Methoden-Reproduktionspaper auf den öffentlichen Datensätzen ImageCAS und CADS vorbereitet, das die technische Plattform unabhängig validiert und als zitierfähige Referenz für die spätere klinische Studie dient.

---

## 7. Anhang (auf Anfrage verfügbar)

- A — Master-Zweckbestimmung (regulatorische Einordnung, Splash-Gate-Wording, Eigenherstellungs-Hinweis nach § 11 MPDG)
- B — Vollständige Quellenliste mit Studien-DOIs, Datensatz-URLs und Tool-Referenzen
- C — Tool-Architektur-Skizze und Komponenten-Übersicht
- D — Zugang zur Online-Demo (Master-Demo-Token nach persönlicher Bestätigung)

---

*Dieser Sachstandsbericht ist als interne, vorläufige Arbeitsgrundlage für ein erstes Sync-Gespräch erstellt und nicht zur Weiterleitung an Dritte bestimmt. Bei Fragen zu einzelnen technischen oder regulatorischen Punkten bitte direkt zurückmelden.*
