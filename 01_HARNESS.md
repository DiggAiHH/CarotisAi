# 01_HARNESS — Carotis-AI Engineering Harness

> **Zweck:** Diese Datei sagt dir (und jedem AI-Modell), **welches Modell** für **welche Aufgabe** zuständig ist und **wie** sie auszuführen ist. Ziel: Schwere Denkarbeit einmal mit Opus, danach billige Modelle (Haiku/Sonnet) für die Ausführung.

---

## Goldene Regel

**Planung ≠ Ausführung.**
Wenn du ein neues Feature/Refactoring/Datenmodell anfängst, **immer mit Opus 4.7 planen**. Output ist eine Liste atomarer Tasks (`tasks.jsonl`). Diese Tasks sind so detailliert, dass **Haiku 4.5** sie ohne Nachfragen ausführen kann.

**Bei medizinischen / regulatorischen Entscheidungen (DSGVO, MDR, Ethik) NIE ohne Opus arbeiten.** Falsche Pseudo-Codes hier kosten nicht Build-Zeit, sondern Patientensicherheit.

---

## Modell-Routing-Matrix

| Aufgabentyp | Modell | Begründung |
|---|---|---|
| Architektur-Entscheidungen, ADRs | **Opus 4.7** | Tiefes Tradeoff-Denken |
| Roadmap-Planung, Phasen-Splitting | **Opus 4.7** | Globale Sicht über das Projekt |
| Datenmodell für Decision-Tree-Capture | **Opus 4.7** | Schema-Design hat Datenrisiko |
| Schema-Migrationen entwerfen | **Opus 4.7** | Datenrisiko — keine Fehler erlaubt |
| Brainstorming neuer Features | **Opus 4.7** | Divergent thinking |
| Regulatorische Texte (Ethikantrag, EU AI Act-Doku) | **Opus 4.7** | Compliance-Risiko |
| Anschreiben + Exposé an Stakeholder | **Opus 4.7** | Politische Sensibilität, Tonality |
| Schwere Refactorings (Multi-File) | **Sonnet 4.6** | Code-intensives Editieren |
| Bug-Debugging mit Stacktrace | **Sonnet 4.6** | Code-Lese-Schwere |
| Neue Komponente nach Spec implementieren | **Sonnet 4.6** | Spec → Code mit etwas Eigeninitiative |
| Test-Suiten schreiben (nicht trivial) | **Sonnet 4.6** | Erfordert Verständnis des SUT |
| Office-Dokument-Drafts (.docx, .pptx) | **Sonnet 4.6** | Lange Form, aber klare Struktur |
| i18n-Keys synchronisieren | **Haiku 4.5** | Mechanisches Pattern-Matching |
| Atomare Edits (Zeile X durch Y) | **Haiku 4.5** | Pseudo-Code in Task ist exakt |
| Datei-Renames, Imports updaten | **Haiku 4.5** | Search/Replace |
| Boilerplate aus Template generieren | **Haiku 4.5** | Stempel-Arbeit |
| Verify/Build ausführen + Output lesen | **Haiku 4.5** | Bash + Lesen, kein Denken |
| MEMORY.md / Index-Updates | **Haiku 4.5** | Find-and-Replace in Markdown |

### Regel-of-thumb

- **Muss das Modell denken, abwägen, oder ist kein Pseudo-Code möglich?** → Sonnet/Opus.
- **Ist Pseudo-Code mit konkreter Datei + Zeilen vorhanden?** → Haiku.
- **Schreibt das Modell etwas, das einen Code-Pfad ändert (Tests, Config, Migrations)?** → mind. Sonnet, prüfe mit Build.
- **Berührt es Patientendaten oder regulatorische Texte?** → Opus, nie Haiku.

---

## Pre-Flight (Pflicht — JEDES Modell, JEDE Session)

```bash
# 1. Working memory laden
cat CLAUDE.md
cat MEMORY.md

# 2. Letzte 3 Run-Logs überfliegen
ls -t memory/runs/ | head -3 | xargs cat

# 3. Bei Code-Arbeit: existiert die Lösung schon?
grep -r "<feature-keyword>" memory/runs/ memory/domain/

# 4. Bei Modell-Arbeit: bekannte Anomalien?
ls memory/anomalies/ 2>/dev/null

# 5. tasks.jsonl prüfen, ob blockiert
cat tasks.jsonl | jq '.[] | select(.status == "in_progress")'
```

**Wenn Aufgabe bereits erledigt:** → nicht neu machen, bestehende Lösung erweitern.
**Wenn schon mal gescheitert (anomaly log):** → Begründung lesen, anderen Pfad wählen.
**Wenn neu:** → Eintrag in `tasks.jsonl` als `in_progress`, dann ausführen.

---

## Task-Schema (für Haiku-fähige Tasks)

Jeder Task in `tasks.jsonl` hat folgende Felder:

```json
{
  "id": "T-042",
  "title": "Anonymisierungs-Skript für DICOM-Dump aufrufen",
  "phase": "P2",
  "model": "haiku",
  "blocked_by": ["T-041"],
  "files": ["scripts/anonymize.py"],
  "pseudo_code": "...",
  "verify": "python scripts/anonymize.py --check",
  "dod": ["Output enthält 0 PII-Felder", "Hash-File geschrieben"],
  "registry_update": "memory/runs/<datum>_anonymize_batch.md anlegen"
}
```

### Pseudo-Code-Standard

- **Datei + Zeile + exakte Änderung.** Niemals "ähnlich wie X".
- **Imports zuerst** in eigenem Block.
- **Suchstring + Ersetzung** statt freier Beschreibung.
- **Verify-Befehl** der bestätigt, dass die Änderung richtig ist.

---

## Definition of Done (DoD) — pro Task-Typ

### Code-Edit-Task
- [ ] `npm run build` grün (zero TS errors)
- [ ] `npm run lint` grün
- [ ] Falls i18n-Key hinzugefügt: alle 3 Sprachen (de/en/ar) haben den Key
- [ ] Eintrag in `memory/runs/<datum>_<task-id>.md`

### Daten-Pipeline-Task
- [ ] Skript läuft ohne Exception auf Test-Sample
- [ ] Output enthält **0 PII-Felder** (Verify mit `dicom-anonymizer --report`)
- [ ] SHA-256-Hash der anonymisierten Files in `data/manifest.csv`
- [ ] Eintrag in `memory/runs/`

### Modell-Training-Task
- [ ] Trainings-Loss + Val-Loss + Dice + Sensitivity geloggt
- [ ] Modell-File mit Datum + Commit-Hash benannt: `model_<YYYYMMDD>_<short-sha>.onnx`
- [ ] Reproducibility: Seed gesetzt, Trainingsdaten-Manifest verlinkt
- [ ] Modell-Card geschrieben (`models/<name>/MODEL_CARD.md`)
- [ ] Eintrag in `memory/runs/` + ggf. `memory/anomalies/` wenn Performance unerwartet

### Office-Dokument-Update
- [ ] Stride-Prompt in `07_OFFICE_AGENT_PROMPTS.md` aktualisiert
- [ ] Ziel-Datei + Änderungs-Diff in der Antwort dokumentiert
- [ ] Lou bestätigt visuell vor dem Versand
- [ ] Eintrag in `memory/runs/`

### Stakeholder-Communication
- [ ] Empfänger korrekt (Klinikum Dortmund, Prof. Rohde, korrekte Anrede)
- [ ] Absender korrekt (Aroob als „Ärztin in Weiterbildung für Radiologie")
- [ ] Anhänge geprüft (Exposé + Tech-Doc + CV + Floy-Recherche)
- [ ] Wenn Rohde antwortet: Antwort in `memory/runs/<datum>_rohde_response.md` + nächste Aktion

### Regulatorisches Dokument (Ethikantrag, EU AI Act-Doku, MDR-Stuff)
- [ ] Opus 4.7 hat es geschrieben (NICHT Haiku, NICHT Sonnet ohne Review)
- [ ] Lou + Aroob haben es gelesen
- [ ] Bei Unsicherheit: Prof. Margaritoff (62304) bzw. Prof. Tolg konsultiert
- [ ] Versions-Header (Datum + Autor + Reviewer) im Dokument

---

## Workflow-Phasen (so läuft eine Session)

```
┌──────────────────────────────────────────────────────────────┐
│ Phase 1: PLANUNG (Opus 4.7)                                   │
│   - User: "Ich will Feature/Doc X"                            │
│   - Opus: liest CLAUDE.md, MEMORY.md, ROADMAP.md              │
│   - Opus: scannt memory/runs/ + memory/anomalies/             │
│   - Opus: erstellt 5–15 atomare Tasks → tasks.jsonl           │
└──────────────────────────────────────────────────────────────┘
                            ↓
┌──────────────────────────────────────────────────────────────┐
│ Phase 2: AUSFÜHRUNG (Haiku/Sonnet)                            │
│   - Modell liest tasks.jsonl + 01_HARNESS.md                  │
│   - Pre-Flight Check                                          │
│   - Tasks in dependency-order abarbeiten                      │
│   - Nach jedem Task: verify, dann memory/runs/ Eintrag        │
└──────────────────────────────────────────────────────────────┘
                            ↓
┌──────────────────────────────────────────────────────────────┐
│ Phase 3: VERIFIKATION (Sonnet)                                │
│   - Build + Lint + Test grün                                  │
│   - Manueller Smoke-Test                                      │
│   - Session-Log in memory/runs/<datum>_session.md             │
└──────────────────────────────────────────────────────────────┘
```

---

## Memory-Hierarchie (das Neue gegenüber Elbtronika)

```
CLAUDE.md         — wird in jede Session geladen, < 200 Zeilen, Working Memory
MEMORY.md         — Index, < 200 Zeilen, eine Zeile pro Memory-Datei
memory/
  ├── domain/     — stabiles Wissen (User, Project, Refs, Feedback)
  ├── runs/       — pro Session ein File: was getan, was gelernt, was nächstes
  ├── decisions/  — anonymisierte Arzt-Entscheidungs-Trees (P5+)
  ├── anomalies/  — KI-Mensch-Diskrepanzen + Lehren (P5+)
  └── archive/    — obsolet gewordene Memorys (statt löschen)
```

**Run-Log-Pflicht:** Jeder Modell-Run schließt mit einem Eintrag in `memory/runs/<YYYY-MM-DD>_<modell>_<thema>.md`. Format:

```markdown
# Session <YYYY-MM-DD> · <Modell> · <Thema>

**Goal:** <was sollte erreicht werden>
**Done:** <was wurde tatsächlich gemacht — Liste der Tasks oder Files>
**Surprised by:** <was war anders als erwartet — wichtigste Zeile für die nächste Session>
**Avoided:** <was hätten wir fast gemacht, war aber falsch — siehe Pre-Flight-Check>
**Next:** <konkrete nächste Action>
**Memory updates:** <welche memory-Files wurden geändert>
```

Diese Logs sind die **Engineering-Harness-Innovation für Carotis-AI**: jeder Run macht den nächsten klüger.

---

## Error-Recovery: Wann zurück zu Opus

Haiku/Sonnet **stoppt und eskaliert zu Opus** wenn:

1. **Build bricht** und der Stacktrace nicht eindeutig auf eine Zeile zeigt.
2. **Pseudo-Code matcht nicht** — die referenzierten Zeilen existieren nicht mehr.
3. **Dependencies fehlen** im npm/pip-Tree.
4. **Schema-Konflikt** — Task will Field hinzufügen das schon existiert.
5. **Memory-Konflikt** — Pre-Flight findet, dass Task in `memory/anomalies/` steht.
6. **Patientendaten betroffen** und der Task ist nicht explizit als Anonymisierungs-sauber markiert. **Sofortiger Stopp.**

Eskalations-Format:
```
## Eskalation an Opus
Task-ID: T-042
Problem: <kurze Beschreibung>
Gesehen: <Stacktrace / Diff / Output>
Versucht: <was schon ausprobiert>
Memory-Hinweis: <welche memory-Datei evtl. relevant>
```

---

## Was dieses Harness NICHT ersetzt

- **CLAUDE.md** (Top-level Projekt-Regeln, Stack, People, Critical Path)
- **05_DECISION_TREE_HARVESTING.md** (Schema und Workflow für Arzt-Entscheidungs-Capture)
- **memory/domain/refs_regulatory.md** (gesetzliche Quellen)

Dieses Harness ist die **Brücke** zwischen "ich will was machen" und "ein billiges Modell macht es jetzt — und schreibt auf, was es gelernt hat".
