# memory/ — Carotis-AI Langzeit-Memory

> Diese Hierarchie ist die zweite Hälfte des Engineering-Harness. Was in `CLAUDE.md` nicht reinpasst (zu spezifisch, zu lang, zu kurzlebig), gehört hierher. Index: `MEMORY.md` im Root.

---

## Struktur

```
memory/
├── README.md          # diese Datei
├── domain/            # stabiles Wissen (User, Project, Refs, Feedback)
├── runs/              # pro Modell-Session ein Eintrag (siehe Format unten)
├── decisions/         # anonymisierte Arzt-Entscheidungs-Trees (P5+)
├── anomalies/         # KI-Mensch-Diskrepanzen + Wochen-Triage (P5+)
└── archive/           # obsolet gewordene Memorys (nicht löschen — verschieben)
```

---

## domain/

Stabile Fakten, die mehrere Wochen gelten. Beispiele:

- `user_role.md` — wer ist Lou, was kann er, wie tickt er
- `project_carotis.md` — was ist das Projekt, was ist drin, was ist nicht drin
- `project_status_p0.md` — aktuelle Phase + Block (wird bei Phasen-Wechsel verschoben nach archive/)
- `refs_repos.md` — Pointer auf GitHub-Repos
- `refs_papers.md` — Pointer auf 08_RESEARCH_ATTENTION_2020-2026.md
- `refs_regulatory.md` — Pointer auf Gesetze und Normen
- `fb_office_docs.md` — Feedback-Memory: Office-Files werden nicht direkt editiert
- `fb_local_first.md` — Feedback-Memory: Local-First ist nicht-verhandelbar

Pro Datei: einleitendes Frontmatter (name, description, type, last_updated), dann der Inhalt. Format wie in `01_HARNESS.md` definiert.

---

## runs/

**Pflicht-Eintrag pro Modell-Session.** Format:

```markdown
# Session <YYYY-MM-DD> · <Modell> · <Thema>

**Goal:** <was sollte erreicht werden>
**Done:** <was wurde tatsächlich gemacht — Liste der Tasks oder Files>
**Surprised by:** <was war anders als erwartet — wichtigste Zeile für die nächste Session>
**Avoided:** <was hätten wir fast gemacht, war aber falsch — siehe Pre-Flight-Check>
**Next:** <konkrete nächste Action>
**Memory updates:** <welche memory-Files wurden geändert>
```

Dateinamens-Konvention: `<YYYY-MM-DD>_<modell-kurz>_<thema-kebab>.md`
Beispiele:
- `2026-04-27_opus47_harness_v1.md`
- `2026-04-28_sonnet_stride_prompt_g.md`
- `2026-05-12_haiku_i18n_sync.md`

---

## decisions/

**Ab P5 (klinische Validierung)**: anonymisierte Decision-Trees nach dem JSON-Schema in `05_DECISION_TREE_HARVESTING.md`.

Dateinamens-Konvention: `<YYYY-MM-DD>_<case_id_short_8chars>.json`

**Wichtig:** Niemals wird hier ein Original-Patient-Identifier reingeschrieben. Wenn beim Review ein Verdacht auf Re-Identifizierungs-Risiko entsteht (z.B. extrem seltene Diagnose-Kombination + bekannter Studientag): sofortige Eskalation an Lou + Margaritoff-Konsultation, Datei in `decisions/_quarantined/` verschieben.

---

## anomalies/

**Ab P5**: jede Diskrepanz zwischen AI-Vorschlag und Arzt-Entscheidung.
Plus: wöchentliche Triage-Reports von Opus 4.7.

Dateinamens-Konvention:
- `<YYYY-MM-DD>_<case_id_short>_disagreement.json` für Einzelfälle
- `<YYYY-MM-DD>_triage_week<N>.md` für die wöchentliche Synthese

---

## archive/

Wenn ein Memory obsolet wird (z.B. P0 abgeschlossen → Status-Memory veraltet):
1. Datei nach `memory/archive/<original_pfad>` verschieben
2. Pointer-Zeile in `MEMORY.md` streichen
3. **Nicht löschen.** Manchmal will man verstehen, warum etwas früher entschieden wurde.

---

## Hygiene

- `MEMORY.md` (Index) muss < 200 Zeilen bleiben → wenn voll: alte runs in monatliche Roll-ups konsolidieren
- `runs/` darf wachsen, aber alle 6 Monate: Lou + Opus konsolidieren in `runs/_summaries/<jahr>_<monat>.md`
- `domain/` hat keine Größenbegrenzung — bleibt der primäre Lookup
- `decisions/` und `anomalies/` haben harte Lifecycle-Regeln aus dem Datenvertrag (P1)

---

**Letzte Aktualisierung:** 2026-04-27
