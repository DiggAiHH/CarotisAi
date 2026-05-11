# Promotionsskizze — Dr. med. Aroob Alrawashdeh

**Studientitel (Arbeitstitel):**
*"Reading-Time- und Decision-Tree-Pattern bei der retrospektiven Carotis-CTA-Begutachtung: eine Workflow-Beobachtungsstudie zur Unterscheidbarkeit der Befundungs-Pattern von Assistenzärztinnen/-ärzten und Fachärztinnen/-ärzten am Klinikum Dortmund."*

**Promovendin:** Dr. med. Aroob Alrawashdeh
**Doktorvater (angefragt):** Prof. Dr. med. Stefan Rohde, Direktor Klinik für Radiologie und Neuroradiologie, Klinikum Dortmund
**Technische Implementation (Co-Investigator, Co-Author):** L. Alshdaifat, HAW Hamburg, Medizintechnik
**Statushinweis:** Forschungsprototyp, kein Medizinprodukt im Sinne der MDR (EU 2017/745) bzw. § 3 Nr. 1 MPDG. Master-Zweckbestimmung vom 6. Mai 2026, Version `zweckbestimmung_2026-05-06`, liegt vor.

**Erstellt:** 11. Mai 2026 · Version 1.0

---

## 1. Forschungsfrage

Lässt sich das Befundungsverhalten bei der Carotis-CTA-Begutachtung — operationalisiert durch Lesezeit, Aufmerksamkeits-Pattern und Decision-Tree-Verzweigungen — systematisch und reproduzierbar zwischen Assistenzärztinnen/-ärzten und Fachärztinnen/-ärzten der Neuroradiologie unterscheiden, wenn ein strukturiertes Workflow-Capture-Tool eingesetzt wird?

## 2. Primäre Hypothese (verteidigungsfähig)

**H1:** Die mittlere Reading-Time pro Carotis-CTA-Fall und die Anzahl der durchlaufenen Decision-Tree-Verzweigungen unterscheiden sich signifikant (α = 0.05) zwischen Assistenzärztinnen/-ärzten und Fachärztinnen/-ärzten in der retrospektiven Befundung.

**H0:** Es besteht kein systematischer Unterschied in Reading-Time oder Decision-Tree-Pattern zwischen den beiden Erfahrungsgruppen.

## 3. Sekundäre Endpunkte

1. **Konkordanz innerhalb der Erfahrungsgruppe** — Übereinstimmung der Plaque-Beurteilung zwischen je zwei Assistenzärzt:innen und zwei Fachärzt:innen, gemessen über Cohens-κ auf strukturierten Decision-Tree-Knoten.
2. **Aufmerksamkeits-Pattern-Überlappung** — räumliche Überlappung der Lesezeit-Heatmap mit der durch das Forschungs-Referenz-Overlay (HiResCAM) hervorgehobenen Region (Jaccard-Index).
3. **Übereinstimmung mit dokumentiertem klinischem Verlauf** — sofern Outcome-Daten retrospektiv verfügbar sind (CAS-Indikation, dokumentierter Schlaganfall-Verlauf), Sensitivitäts-/Spezifitäts-Abschätzung der Reader-Beurteilung gegen dokumentierten Verlauf.

## 4. Studiendesign

| Parameter | Wert |
|---|---|
| Design | Retrospektive Beobachtungsstudie, anonymisiert |
| Setting | Klinikum Dortmund, Klinik für Radiologie und Neuroradiologie |
| Studienzeitraum-Quelle | Carotis-CTA-Aufnahmen 2019–2024 (vorhanden im PACS und DeGIR/DGNR-Subset) |
| Stichprobengröße | Primär n = 200 (Power-Berechnung siehe §5) |
| Pilot-Welle vorab | n = 30 zur Methoden-Validierung |
| Reader-Pool | 4 Assistenzärzt:innen + 4 Fachärzt:innen aus der Klinik |
| Reader-Aufwand pro Person | etwa 8 Stunden über 4–6 Sitzungen, retrospektiv |
| Werkzeug | Carotis-AI-Forschungsprototyp (Workflow-Capture + erklärbares Heatmap-Overlay, ohne quantitative Befund-Ausgabe) |
| Datenflussschutz | DICOM-De-Identifikation nach PS 3.15, lokale SQLite, kein Cloud-Transfer |

## 5. Power-Berechnung (Primär-Endpunkt)

Auf Basis von Voritz-Daten der Literatur (Frontiers Neurol. 2024, Guo et al.: Diagnosezeit ~6 s vs. Radiologen mehrere Minuten) und allgemeiner Workflow-Studien-Heuristik:

- Erwartete Differenz Reading-Time zwischen Assistenz und Facharzt: ca. 30–60 s pro Fall
- Erwartete Standardabweichung: ca. 60 s pro Fall (Workflow-Heterogenität)
- Effect Size Cohen's d ≈ 0.4–0.6 (moderater Effekt)
- Power 0.80, α = 0.05 zweiseitig
- Resultierend: n pro Gruppe ≈ 64–100 Reader-Lesungen
- Bei 4 Readern pro Gruppe und 25 Fällen pro Reader → 100 Lesungen pro Gruppe → **200 Reader-Sitzungen gesamt**, basierend auf etwa 50 unique Fall-IDs (jeder Fall doppelt gelesen)

Die exakte Power-Berechnung wird im Statistik-Plan vor Studienbeginn finalisiert. Methodische Beratung über die Sektion Biomedizinische Physik wird angefragt.

## 6. Realistischer Zeitplan und Risiken

| Monat | Phase | Aktivität | Risiko-Hotspot |
|---|---|---|---|
| 0 | Anbahnung | Rohde-Mail, Aroob-Sync, Ethik-Vorgespräch | gering |
| 1–3 | Setup | Ethikantrag einreichen, IT-Anfrage Klinikum für PACS-Auszug | **Ethikkommission 2–6 Monate Bearbeitung** |
| 3–6 | Pilot | n = 30 Pilot-Fälle anonymisiert, 2 Reader pro Gruppe, Methoden-Stabilisierung | Reader-Verfügbarkeit |
| 6–12 | Hauptphase | n = 200 Reader-Sitzungen, Workflow-Tool-Einsatz, Datensammlung | **Reader-Disziplin (Assistenzärzt:innen mit 60-h-Woche)** |
| 12–18 | Auswertung | Statistik, Manuskript-Draft, ggf. Korrektur-Welle | Statistik-Methodik-Klärung |
| 18–24 | Submission | Manuskript-Einreichung *Clinical Neuroradiology* oder *RöFo*, Peer-Review | **Reviewer-Lotterie 3–9 Monate** |
| 24–30 | Revision | Reviewer-Antworten, Annahme, Druck | gering |
| 30–36 | Dissertation | Dissertationsschrift, Disputation, Promotionsurkunde | gering |

**Erwartete Gesamtdauer von Heute bis Promotionsurkunde:** 30–36 Monate. Realistisch innerhalb der zulässigen Promotionsfrist (Klinikum-DO / TU Dortmund Rahmen: meist 4 Jahre nach Annahme).

### 6.1 Top-3-Risiken und Mitigation

1. **Ethik-Bearbeitungszeit:** Vorgespräch mit Ethikkommissions-Vorsitz vor formaler Einreichung, um Nachforderungen zu antizipieren. Antrag minimal-invasiv halten (retrospektiv, anonymisiert, kein Eingriff).
2. **Reader-Disziplin:** Reader-Sitzungen blockweise organisieren, im Klinik-Pool als Fortbildungs-Slot framen, Reader-Aufwand realistisch auf 8 Stunden pro Person begrenzen. Vergütung über Klinik-üblichen Rahmen prüfen.
3. **Negatives Ergebnis:** Falls H0 nicht abgelehnt werden kann (keine Differenz zwischen Erfahrungsgruppen messbar), ist die Arbeit dennoch verteidigungsfähig — der methodische Beitrag (reproduzierbare Workflow-Capture-Pipeline) und der Sekundärendpunkt (Konkordanz innerhalb Erfahrungsgruppe) tragen die Dissertation. Eingeplant durch Sekundär-Endpunkte mit eigenständiger Aussagekraft.

## 7. Translations- und Realwelt-Relevanz

Workflow-Studien dieses Typs führen typischerweise zu:

- **Publikation** in *Clinical Neuroradiology*, *European Journal of Radiology* oder *RöFo* (Impact Factor 2–4, etabliertes Format)
- **Methodisches Werkzeug** als Open-Source-Plattform (MIT-Lizenz) als Folgeprodukt — wird von anderen Forschungsgruppen zitierbar
- **Curriculum-Beitrag** für die Assistenzärzt:innen-Ausbildung in der Klinik (objektivierbare Reading-Pattern-Charakterisierung als Lehrhilfe)
- **Kein** kommerzielles Medizinprodukt — Translation ins Patientenversorgung erfolgt nicht direkt, sondern über die fachliche Diskussion der Befundungs-Pattern

Erwartung an die Realwelt: die Studie verändert nicht den klinischen Workflow der Klinikum-DO unmittelbar. Sie liefert eine methodische Referenz für die Charakterisierung radiologischer Befundungs-Pattern, die in Lehre, Qualitätssicherung und Folgestudien aufgegriffen wird. Das ist der typische Wirkradius einer klinisch-retrospektiven Dr.-med.-Arbeit in der Neuroradiologie und ist als solcher anerkannt.

## 8. Was die Studie nicht ist

- **Keine** Diagnose-KI. Das Werkzeug erzeugt keine Befunde.
- **Keine** prospektive Interventionsstudie. Es wird retrospektiv ausgewertet.
- **Keine** Sensitivitäts-/Spezifitäts-Studie eines AI-Diagnostik-Modells (das wäre regulatorisch eine andere Studie nach MDR).
- **Kein** Medizinprodukt-Pilot. Die § 11 MPDG-Optionalität bleibt einer späteren institutionellen Entscheidung des Klinikums vorbehalten und ist nicht Teil der Promotion.

## 9. Authorship und Beitrags-Klärung (ICMJE)

| Person | Substantieller Beitrag | Manuskript-Schreibung | Final approval | Accountability |
|---|---|---|---|---|
| Aroob Alrawashdeh | klinisches Studiendesign, Reader-Koordination, Datenerhebung, Auswertungs-Lead, Manuskript-Erstautorin, Disputation | Erst-Draft, Revision | ja | ja |
| L. Alshdaifat | technische Implementation, Workflow-Tool-Bereitstellung, Statistik-Pipeline, methodische Reproduzierbarkeit | Methods + Results-Tabellen, Co-Author-Review | ja | ja |
| S. Rohde | institutionelles Sponsoring, klinische Supervisor-Rolle, Senior-Review | finale Manuskript-Review | ja | ja |

Authorship-Vereinbarung erfüllt alle vier ICMJE-Kriterien für jede genannte Person. Erst-Autorenschaft liegt eindeutig bei der Promovendin.

## 10. Was als nächstes ansteht

1. **Heute:** Rohde-Mail mit dieser Skizze als Anhang versenden.
2. **Innerhalb 2 Wochen:** Antwort von Rohde, ggf. Erst-Gespräch.
3. **Bei Zusage:** Ethik-Vorgespräch (etwa Monat 1).
4. **Parallel:** Carotis-AI-Forschungsprototyp final auf Forschungs-Sprache (Stride-V2-Re-Frame), Splash-Gate und Watermark deployen (Codex-Sprint läuft).
5. **Phase B Start:** sobald Ethikvotum vorliegt.

---

**Anhang verfügbar auf Anfrage:**
- Master-Zweckbestimmung `zweckbestimmung_2026-05-06`
- Code-Status-Bericht (Live-Smoke gegen carotis.diggai.de am 11.05.2026)
- Methodenpaper Säule A v0.0 Skeleton (Public-Data-Reproduktion, läuft parallel als Lou-First-Author-Paper)
- Vollständige Quellen- und Datensatz-Liste
