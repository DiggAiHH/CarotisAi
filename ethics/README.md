# ethics/ — Ethik- und Datenschutz-Paket

> Templates für den Ethikantrag bei der Ethikkommission der Ärztekammer Westfalen-Lippe (zuständig für das Klinikum Dortmund), Patienten­information, Einwilligungs­erklärung und DSGVO-Folgen­abschätzung.
>
> **Status: P1-ready.** Diese Templates müssen vor Einreichung von Aroob, Lou und idealerweise Prof. Margaritoff (DIN EN 62304) und einem Anwalt für Medizinrecht reviewed werden. Alle eckigen Klammern `[…]` sind Platzhalter für Fall-spezifische Werte.

---

## Übersicht

| Datei | Empfänger | Status |
|-------|-----------|--------|
| `ethikantrag_skelett.md` | Ethikkommission der Ärztekammer Westfalen-Lippe | Skelett — Aroob füllt aus, Margaritoff reviewt |
| `patienteninformation.md` | Patienten (für Studieneinschluss) | Skelett — Aroob + Anwalt reviewen |
| `einwilligungserklaerung.md` | Patienten (zur Unterschrift) | Skelett — Aroob + Anwalt reviewen |
| `dpia_skelett.md` | Datenschutz­beauftragte:r Klinikum Dortmund | Skelett — Lou + Datenschutz-Office reviewen |

---

## Reihenfolge

1. **DPIA zuerst** — die Folgen­abschätzung muss bei Hochrisiko-Verarbeitung VOR dem Studienstart abgeschlossen sein (DSGVO Art. 35).
2. **Patienten­information + Einwilligung** — die müssen mit dem Ethikantrag eingereicht werden, also gemeinsam fertigstellen.
3. **Ethikantrag** — verweist auf alle drei anderen Files als Anlagen.
4. **Datenvertrag (AVV)** zwischen Klinikum Dortmund und Lou/HAW — separates Dokument (nicht in `ethics/`, sondern in `regulatory/contracts/` ab P1).

---

## Wer tut was

| Person | Rolle | Aktionen |
|--------|-------|----------|
| **Aroob** | Studienleiterin | Klinische Inhalte, Studiendesign, Ein-/Ausschluss­kriterien |
| **Lou** | Co-Studienleiter (technisch) | Datenfluss-Diagramm, Anonymisierungs-Beschreibung, technische Sicherheits­maßnahmen |
| **Prof. Rohde** | Wissenschaftlicher Betreuer / PI | Co-Antragsteller, Klinik-Verantwortlich |
| **Prof. Margaritoff** | Wissenschaftliche Beratung | Review der DIN-EN-62304-Konformitäts-Aussagen |
| **Datenschutz-Office Klinikum Dortmund** | Behörde | DPIA-Approval, AVV-Verhandlung |
| **Anwalt Medizinrecht** | externe Beratung | Review Patienten­information + Einwilligung (haftungs-kritisch) |

---

## Frist-Schätzung

- DPIA-Erstellung: 2 Wochen (mit Datenschutz-Office)
- Ethikantrag-Erstellung: 1 Woche (Aroob + Lou)
- Kommissions-Bearbeitungszeit: typisch 6–10 Wochen für Westfalen-Lippe
- Gesamt P1-Dauer: 8–12 Wochen ab Rohde-Approval

---

**Letzte Aktualisierung:** 2026-04-27
