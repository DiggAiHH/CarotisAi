# STRIDE PROMPT D — Kopieren & Einfügen

> **Vorher:** Öffne Stride. Lade `Ki_Carotis_Diagnostik.docx` hoch.
> **Danach:** Output speichern als `Tech_Description_Klinikum_v2.docx`

---

## SCHRITT 1: Globalen Kontext einfügen

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

## SCHRITT 2: Prompt D einfügen

```
Aktualisiere die technische Projektbeschreibung Ki_Carotis_Diagnostik.docx für Prof. Dr. med. Stefan Rohde am Klinikum Dortmund.

ÄNDERUNGEN:
- Setting: durchgehend "Klinikum Dortmund" statt "Praxis"
- Nutzer: "Radiologen und Ärzte in Weiterbildung am Klinikum"
- Datum: 2026-04-27

NEUER ABSCHNITT (am Ende, vor dem Zeitplan):

═══════════════════════════════════════════════════════
ENGINEERING HARNESSING IN DER MEDIZINTECHNIK

Traditionelle Medizinsoftware-Entwicklung dauert 3–5 Jahre von der Idee bis zur regulatorischen Zulassung. Unser Engineering-Harnessing-Framework reduziert diese Zeit auf 24 Monate, ohne Qualitätskompromiss, durch:

• Modell-Routing: Architekturentscheidungen werden einmal mit hochwertigen AI-Modellen (Anthropic Claude Opus 4.7) getroffen; Routine-Implementation läuft mit kostengünstigeren Modellen (Sonnet 4.6, Haiku 4.5) — bei vollständiger Audit-Trail-Dokumentation.

• Memory-Hierarchie: Jeder AI-gestützte Entwicklungs-Run hinterlässt strukturierte Lehren in einer projekt-eigenen Memory-Bibliothek. Der nächste Run beginnt nicht bei Null — er beginnt mit dem konsolidierten Wissen aller vorherigen.

• Regulatory-by-Design: DIN EN 62304, EU AI Act und DSGVO sind keine nachträglichen Hürden, sondern integrale Architektur-Prinzipien — dokumentiert von Phase 0 an.

• Decision-Tree-Harvesting in der klinischen Validierung: ab Phase 5 lernt das System täglich aus den anonymisierten Entscheidungs-Begründungen der Befunder. Performance-Vergleich vor/nach jedem Lern-Schritt; Auto-Rollback bei Verlust.

Diese Methodik ist nicht Carotis-spezifisch. Nach erfolgreicher Validierung in der Carotis-Diagnostik kann sie auf andere radiologische Fragestellungen übertragen werden — was dem Klinikum Dortmund eine reproduzierbare Plattform für weitere KI-Promotionen bietet.
═══════════════════════════════════════════════════════

Speichere als: Tech_Description_Klinikum_v2.docx
```

---

## SCHRITT 3: Review-Checkliste

- [ ] Datei heißt `Tech_Description_Klinikum_v2.docx`
- [ ] Engineering-Harnessing-in-der-Medizintechnik-Abschnitt vorhanden
- [ ] "Klinikum Dortmund" durchgehend
- [ ] Diff-Liste am Ende
