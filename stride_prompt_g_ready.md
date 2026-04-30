# STRIDE PROMPT G — Kopieren & Einfügen

> **Vorher:** Öffne Stride / Microsoft 365 Copilot. Lade `Ki_Tools_Marktanalyse.docx` hoch.
> **Danach:** Output speichern als `KI_Tools_Marktanalyse_v2.docx`

---

## SCHRITT 1: Globalen Kontext einfügen

Kopiere das Folgende in die Stride-Chat-Eingabe (erste Nachricht):

```
SETTING-UPDATE:
- Empfänger: Prof. Dr. med. Stefan Rohde, Klinikum Dortmund (Direktor / Klinik für Radiologie und Neuroradiologie)
- Absender: Aroob Alrawashdeh, Ärztin in Weiterbildung für Radiologie, Klinikum Dortmund
- Institution: durchgehend "Klinikum Dortmund" (NIE "Praxis")
- Aroob's Titel: "Ärztin in Weiterbildung für Radiologie" (NIE "Fachärztin")
- Bestehende Beziehung: Aroob war 01.01.2023 – 30.06.2023 schon einmal bei Prof. Rohde tätig. Er hat freundliche Gespräche geführt, eine Floy-Recherche als Hausaufgabe gegeben, und prüft, ob die Idee zur Promotion taugt.
- Heute ist der 27. April 2026.
- Sprache: Deutsch, formell, akademisch-präzise. Engineering-Begriffe korrekt.
- Tonalität: respektvoll und Engineering-selbstbewusst. KEIN Bittstellertum. KEINE Übertreibungen ("revolutionär", "weltweit erste", etc.). Konkrete Fakten.

KEYWORDS, die in jedem Dokument vorkommen müssen:
- "Engineering Harnessing" als Methodik
- "Local-First Edge AI"
- "Decision-Tree Harvesting"
- "Daily Learning Loop"
- "MFSD-UNet" (Modell-Architektur)
- "Klinikum Dortmund"
- "Human in the Loop"
- "DSGVO-konform by Design"
- "EU AI Act, Art. 10/13/14/15"
- "MDR Class IIa"
- "DIN EN 62304"
- "Plaque-Vulnerability-Marker (IPH, ThinCap, LRNC)"

Output für jedes Dokument:
1. Vollständiger aktualisierter Text in Word-importierbarem Format
2. Eine Diff-Liste am Ende (was wurde geändert vs. v1)
3. Speichern als <originalname>_v2.docx (NICHT überschreiben)
```

---

## SCHRITT 2: Prompt G einfügen

Warte bis Stride den globalen Kontext bestätigt hat. Dann kopiere:

```
Erweitere die Floy-Recherche Ki_Tools_Marktanalyse.docx um ein abschließendes Kapitel "Gap-Analyse: Warum Floy für die Carotis-Diagnostik nicht reicht".

INHALT des neuen Kapitels:

1. Floy-Schwerpunkt: CT-Thorax (Lungennoduli, Pneumonie). Carotis-Diagnostik ist KEIN dokumentierter Use-Case in der Floy-Produktdokumentation.

2. Architektur: Floy ist cloud-basiert (laut Produktdokumentation und Blog). Damit problematisch unter:
   • DSGVO Art. 9 (Gesundheitsdaten — strenge Cloud-Anforderungen)
   • EU AI Act Art. 10 (Data Governance bei High-Risk AI)
   • BSI-Empfehlungen für Krankenhausinformations-Systeme

3. Erklärbarkeit: Floy bietet primär Bounding-Boxes und Konfidenz-Werte. Keine Grad-CAM-Heatmaps, keine SHAP-Analyse, kein expliziter Reasoning-Capture. Damit nur teilweise EU-AI-Act-Art-13-konform.

4. Multi-Center / Transnational: Floy hat keinen dokumentierten Use-Case für Multi-Center-Studien mit Differenz zwischen DE und MENA-Region (relevant für die geplante Sarah-Hospital-Kooperation).

5. Lock-In: Floy-Lizenzmodell ist proprietär; bei Anbieter-Wechsel sind Trainings-Investitionen und Workflow-Anpassungen verloren.

6. Tabelle (Floy vs. Carotis-AI):
   | Kriterium | Floy | Carotis-AI |
   |-----------|------|------------|
   | Architektur | Cloud | Local-First Edge |
   | DSGVO | erhöhte Anforderungen | by Design konform |
   | Carotis-Spezialisierung | nicht dokumentiert | Kern-Use-Case |
   | Erklärbarkeit (XAI) | Bounding-Box + Konfidenz | Grad-CAM + SHAP + Reasoning-Capture |
   | EU AI Act | teilweise konform | proaktiv konform |
   | Decision-Tree-Harvesting | nein | ja, als Trainings-Loss |
   | Multi-Center-DE/JO | nein | ja, transnational designed |
   | Lock-In | hoch | null (Open-Source-Stack + ONNX) |
   | Lizenzkosten | wiederkehrend | einmalig (HAW-Förderung) |

FAZIT: Floy ist eine valide Lösung für die Anwendungsfälle, für die sie gebaut wurde (CT-Thorax). Für die Carotis-Diagnostik im Klinikum Dortmund unter Berücksichtigung von DSGVO und EU AI Act ist eine maßgeschneiderte Lösung sowohl regulatorisch sauberer als auch wissenschaftlich publikations-stärker.

Speichere als: KI_Tools_Marktanalyse_v2.docx
```

---

## SCHRITT 3: Review-Checkliste

Nachdem Stride fertig ist, prüfe:

- [ ] Datei heißt `KI_Tools_Marktanalyse_v2.docx`
- [ ] Neues Kapitel "Gap-Analyse" ist vorhanden
- [ ] Tabelle Floy vs. Carotis-AI ist vollständig (10 Zeilen)
- [ ] "Klinikum Dortmund" kommt mindestens 1x vor
- [ ] Diff-Liste am Ende des Dokuments

Wenn alles passt: **Speichern** und weiter zu Prompt H.
