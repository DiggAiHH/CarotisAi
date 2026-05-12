# Agent Handoff Protocol — Carotis-AI
> v1.0 — 2026-05-12 | Lou Alshdaifat  
> Gilt für: **Kimi K2.6 Coding Agent (VS Code)** ↔ **Claude Sonnet 4.6 (Cowork)**

---

## Ground Rule #0 — No Donkey Work

> Ein Fehlerpattern, das in einer Session aufgetreten ist, wird NIEMALS als **erster Versuch** in der naechsten Session wiederholt.

Konkret: Wenn Agent A eine Methode versucht hat und sie ist gescheitert → Agent B liest den Failure-Log und waehlt die bekannte funktionierende Alternative. Nicht "mal probieren".

---

## Rollenverteilung

| Was | Wer | Werkzeug |
|-----|-----|----------|
| Code schreiben, Refactorn, Boilerplate, Ruff-Fixes | **Kimi K2.6** | VS Code Inline / Chat |
| Architektur, ADR, Stakeholder-Dokumente, Memory | **Claude Sonnet 4.6** | Cowork Desktop |
| Git commit + push auf Windows | **Claude Sonnet 4.6** via PowerShell MCP | (Kimi uebergibt Commit-Message) |
| pytest ausfuehren | **Kimi K2.6** direkt im VS Code Terminal | (gibt Exit-Code zurueck) |
| Bash-Sandbox (Linux) | **NUR** fuer pip install, wget, curl | Nie fuer git, nie fuer Datei-Verifikation |

---

## Pre-Flight — Pflicht fuer JEDEN Agenten, JEDEN Run

```
1. cat CLAUDE.md            # Projekt-State, Stack, People
2. cat MEMORY.md            # Was war zuletzt? Was ist blocked?
3. cat 01_HARNESS.md        # Gelernte Muster (bekannte Failures)
4. ls -t memory/runs/ | head -5   # letzte Run-Logs ueberfliegen
5. Existiert die Loesung schon?
   grep -r "<feature-keyword>" memory/runs/
   ls code/scripts/<was-ich-schreiben-will>
```

**Regel:** Wer das Pre-Flight ueberspringt, baut mit 80% Wahrscheinlichkeit etwas nach, das schon existiert.

---

## Bekannte Failure-Muster (Stand 2026-05-12)

Diese Dinge wurden auf die harte Tour gelernt. **Nicht wiederholen.**

### F-01 — Git aus Linux-Bash
**Fehler:** `git commit` aus dem Bash-Sandbox auf OneDrive-Repo  
**Symptom:** Permission denied / `.git` read-only  
**Fix:** Immer PowerShell MCP:
```powershell
$git = "C:\Program Files\Git\cmd\git.exe"
& $git -C "C:\Users\tubbeTEC\OneDrive\z\Documents\Claude\Projects\Carotis AI" commit -m "..."
```

### F-02 — Bash stale cache
**Fehler:** `wc -l file.py` zeigt alte Version  
**Symptom:** Zeilen-Count stimmt nicht mit Read-Tool ueberein  
**Fix:** `Read`-Tool oder PowerShell `(Get-Content $file).Count` ist Wahrheitsquelle. `du -sh` ebenfalls unzuverlaessig → `ls -lh` nutzen.

### F-03 — pytest: DATABASE_URL nicht erzwungen
**Fehler:** `os.environ.setdefault("DATABASE_URL", ...)` reicht nicht  
**Symptom:** Tests schreiben in echte SQLite DB (`.data/carotis.db`), Isolation kaputt  
**Fix:** Ganz oben in `conftest.py`, **vor allen Imports**:
```python
import os
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"  # FORCED
```

### F-04 — asyncio.run() auf sync Funktion
**Fehler:** `await asyncio.run(service.check_only(...))` oder `asyncio.run(sync_func())`  
**Symptom:** `ValueError: a coroutine was expected`  
**Fix:** `check_only()` ist sync → direkt aufrufen: `svc.check_only(bytes)`  
Regel: Vor `await` oder `asyncio.run()` immer Signatur pruefen.

### F-05 — Datei neu erstellen, die schon existiert
**Fehler:** Script generieren ohne vorher zu pruefen ob es existiert  
**Beispiel:** `generate_demo_model.py` — existierte bereits vollstaendig  
**Fix:** `ls code/scripts/<name>` bzw. `Glob` immer als ersten Schritt.

### F-06 — anonymize.py Pfad falsch angenommen
**Fehler:** Script in `code/scripts/anonymize.py` suchen  
**Wahrheit:** Liegt in `Carotis AI/scripts/anonymize.py` (project_root = parents[4])  
**Fix:** `config.py` lesen → `project_root = Path(__file__).resolve().parents[4]`

### F-07 — OsiriX / externe DICOM-Quellen ohne Auth
**Fehler:** OsiriX-Download-Links direkt aufrufen  
**Symptom:** Redirect zu Premium-Login  
**Bekannte freie Quelle:** Zenodo record 16956 (CC BY-SA 4.0, direkter wget ohne Login)  
**Fix:** Fuer Tests: `code/tests/test_data/real_mri/` hat bereits 5 anonymisierte DICOMs.

### F-08 — web_fetch ohne Provenance
**Fehler:** `mcp__workspace__web_fetch` auf URL, die nicht in WebSearch-Resultat war  
**Symptom:** Provenance-Error  
**Fix:** Erst `WebSearch` → dann `web_fetch` auf die zurueckgegebenen URLs.

### F-09 — Fly.io Deploy
**Fehler:** Aenderungen auf Fly.io deployen wollen  
**Status:** Trial beendet, Billing blockiert. Fly.io ist **kein** DNS-Ziel.  
**Fix:** Hetzner CX23. Alles in `deploy/hetzner-backend.compose.yml` + `deploy/Caddyfile.backend`.

### F-10 — Write-Tool fuer neue Files in OneDrive
**Fehler:** `Write`-Tool direkt auf neuen Pfad in OneDrive-Ordner  
**Symptom:** `File has not been read yet. Read it first before writing to it.` — auch bei neuen Files  
**Fix:** PowerShell `Out-File`:
```powershell
$content | Out-File -FilePath "$repo\memory\runs\<name>.md" -Encoding utf8
```
Alternativ: Read eines bestehenden Files im selben Verzeichnis → dann Write funktioniert manchmal.

### F-11 — DEBUG=kimi-sdk:* bricht Pydantic Settings
**Fehler:** Geerbte Shell-Env `DEBUG=kimi-sdk:*` aus VS Code / npm-Session  
**Symptom:** Pydantic ValidationError beim Backend-Start: `DEBUG` erwartet bool, bekommt String  
**Fix:** Beim Smoke oder pytest explizit setzen: `$env:DEBUG = "true"` (PowerShell) oder `DEBUG=true python ...`  
Regel: Shell-Env vor Backend-Start immer prufen: `echo $env:DEBUG` darf nicht `kimi-sdk:*` sein.

---

## Handoff-Format: Kimi → Sonnet 4.6

Wenn Kimi einen Task abschliesst, liefert er **dieses Format** als Abschluss-Nachricht:

```
## Kimi-Run Abschluss — <DATUM> — <K-XX oder Task-Name>

### Erledigt
- [ → ✅] <was wurde gemacht> — <Datei(en)>

### Test-Status
pytest: <PASSED X / FAILED Y / SKIPPED Z>
Ruff: <clean / N errors (noqa gesetzt)>

### Neue Failure-Muster entdeckt
<Falls nichts: "keine neuen">
- F-XX: <kurze Beschreibung> | Fix: <einzeilig>

### Nicht erledigt / Blocker
- <was haengt, warum, was braucht Sonnet um weiterzumachen>

### Naechster Schritt fuer Sonnet 4.6
- <konkrete erste Aktion — nicht "weiter machen", sondern was genau>

### Commit-Message (fuer Sonnet / Lou)
feat(K-XX): <titel>

<body — was wurde warum gemacht>
```

---

## Handoff-Format: Sonnet 4.6 → Kimi

Wenn Sonnet einen Kimi-Task erstellt, liefert er dieses Format als erstes Kimi-Prompt:

```
## Kimi-Task — <DATUM> — <K-XX oder Task-Name>

### Kontext (3 Saetze max)
<Was ist der Hintergrund — keine Geschichte, nur was Kimi wissen muss>

### Pre-Flight (lesen bevor du tippst)
- CLAUDE.md → Stack-Abschnitt
- 01_HARNESS.md → Gelernte Muster
- memory/runs/<letzter-run>.md

### Scope — genau das, nichts mehr
- [ ] <Datei 1>: <was genau aendern>
- [ ] <Datei 2>: <was genau aendern>

### Out of Scope (nicht anfassen)
- <Datei X> — owned by Sonnet / anderen Task
- <Feature Y> — blocked by Rohde / P0

### Bekannte Failures die NICHT erster Versuch sein duerfen
- F-01 (Git aus Bash) → PowerShell
- F-03 (DATABASE_URL setdefault) → forced assignment
- <weitere falls relevant>

### Definition of Done
- pytest -q: 0 failed
- ruff check: 0 errors (noqa erlaubt fuer pre-existing)
- Kein neues File ohne Rueckfrage wenn Datei evtl. schon existiert

### Deliverable
Abschluss-Nachricht im Kimi→Sonnet-Format oben.
Kein Git-Push — Sonnet uebernimmt commit+push.
```

---

## Run-Log Pflicht

**Jeder Run** endet mit einem Eintrag in `memory/runs/`:

```
YYYY-MM-DD_<AgentName>-Run<N>_<slug>.md
```

Inhalt minimal:
```markdown
# Run: <AgentName> Run<N> — <DATUM>

## Task
<Was war der Auftrag>

## Ergebnis
<Was wurde geliefert>

## Neue Muster / Failures
<Oder: keine neuen>

## Naechster Schritt
<Wer macht was>
```

Ohne Run-Log ist der Run **nicht abgeschlossen** — auch wenn der Code gruen ist.

---

## Kommunikationsprinzip

> Ein Agent ist kein Assistent — er ist ein Kollege mit einer definierten Zustaendigkeit.

- Kimi fragt nicht "soll ich X machen?" wenn X im Scope steht → er macht es.
- Sonnet fragt nicht "welche Datei ist das richtige?" wenn `grep` es sagen kann → er liest.
- Kein Agent fasst zusammen was er getan hat (der andere kann die Diff lesen).
- Keine Entschuldigung fuer Fehler — nur: "F-XX entdeckt, Fix: <einzeilig>, weiter."

---

*Dieses Dokument wird nach jedem neuen Failure-Pattern um einen F-XX Eintrag erweitert.*  
*Owner: Lou Alshdaifat. Letzte Aenderung: 2026-05-12 (F-10: OneDrive Write-Tool, F-11: DEBUG env Pydantic).*
