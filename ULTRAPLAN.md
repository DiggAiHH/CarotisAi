# ULTRAPLAN - Carotis-AI Agent Pre-Flight Protocol

Version: 2026-05-01 v6 — "Harness The Whole Knowledge + Design Bridge"
Scope: verbindliches Co-Working-Protokoll fuer Codex, Copilot, Kimi, Claude/Opus/Sonnet/Haiku und lokale Agenten im Carotis-AI Workspace.

Dieses Dokument ist der Startpunkt fuer neue Agents. Es fasst zusammen, was in dieser Session praktisch funktioniert hat, was auf diesem Rechner kaputt ist, welche Tools wann genutzt werden und wo Agents stoppen muessen.

Update 2026-05-02: Skill-Team Harness v7 aktiv. Neue Codex-Skills (`browser-harness`, `caveman`, `compress`, `obsidian`, `remotion-best-practices`) sind in `memory/domain/skill_team_harness_2026-05-02.md` operationalisiert.

---

## 0. Agent Quickstart — 5 Minuten

Du bist ein neuer Agent. In 5 Minuten bist du einsatzbereit:

1. Lies diese Datei (ULTRAPLAN.md) komplett durch.
2. Pruefe die Stop-Regeln in §13 — wenn einer zutrifft, stoppe sofort.
3. Fuehre den Pre-Flight in §2 aus (CLAUDE.md, AGENTS.md, MEMORY.md, Run-Logs).
4. Pruefe Git-Status und Secrets (§2.6, §2.7).
5. Fuer Code-Arbeit: Verifiziere mit den Kommandos in §8 (Frontend) und §9 (Backend).
6. Schreibe pro Prompt einen Run-Log nach 5-Zeilen-Schema (§3).

Wenn du nicht weisst, welches Modell/Tool du bist → §10 Modellrouting.
Wenn du nicht weisst, welchen Skill du brauchst → §11 Skills-Inventar.
Wenn etwas kaputt ist → §14 Anomalien-Register.

---

## 1. Workspace

Root:

```text
c:\Users\tubbeTEC\OneDrive\z\Documents\Claude\Projects\Carotis AI
```

Repo:

```text
https://github.com/DiggAiHH/CarotisAi.git
branch: master
```

Wichtig:

- Carotis-AI ist ein eigenes Repo. Nicht in Anamnese-Repos pushen.
- Remote-URLs duerfen keine Tokens enthalten.
- `git remote -v` muss vor jedem Push geprueft werden.
- Aktive P0f-Deploy-Architektur: Hetzner bedient Frontend + Backend unter `carotis.diggai.de` und `api.carotis.diggai.de`; beide Domains zeigen auf `204.168.230.127`. Fly.io bleibt wegen Trial/Billing blockiert und ist aktuell kein DNS-Ziel.
- Netlify/Render sind fuer P0f nicht mehr Ziel.

---

## 2. Hard Pre-Flight

Vor jeder Arbeit:

1. `ULTRAPLAN.md` lesen (dieses Dokument).
2. `CLAUDE.md` lesen.
3. `AGENTS.md` lesen.
4. `MEMORY.md` lesen.
5. Letzte 3 Run-Logs lesen:

```powershell
Get-ChildItem memory\runs -File | Sort-Object LastWriteTime -Descending | Select-Object -First 3 Name
```

6. Bei Code-Arbeit bekannte Anomalien lesen:

```powershell
Get-ChildItem memory\anomalies -File
```

7. Git pruefen:

```powershell
git status --short --branch
git remote -v
```

8. Secrets scannen, bevor gepusht wird:

```powershell
rg -n "FlyV1|fm2_|github_pat_|BEGIN OPENSSH PRIVATE KEY|BEGIN RSA PRIVATE KEY|API_TOKEN=.*[A-Za-z0-9_-]{20,}" -g '!data/**' -g '!**/.git/**' -g '!**/node_modules/**' .
```

9. Wenn neue Skills/Connectoren genutzt werden: `memory/domain/skill_team_harness_compact_2026-05-02.md` lesen; fuer Detailarbeit `memory/domain/skill_team_harness_2026-05-02.md`.

---

## 3. Memory-Disziplin — 5-Zeilen-Run-Log Pro Prompt

**Kein Prompt endet ohne Run-Log.** Das ist die wichtigste Disziplin. Agents verlieren Kontext zwischen Sessions. Run-Logs sind die einzige Bruecke.

Explizite Naming-Referenz aus der Team-Regel:

```text
memory/runs/2026-04-28_Agentname_Model-RunNN_thema.md
```

### Pfad-Konvention

```text
memory/runs/YYYY-MM-DD_<Agentname>_<Model>-RunNN_<thema>.md
```

| Feld | Format | Beispiele |
|------|--------|-----------|
| `Agentname` | Welcher Coding-Agent hat gearbeitet | `Kimi`, `Codex`, `Copilot`, `Opus`, `Sonnet`, `Haiku`, `Claude` |
| `Model` | Modell + Version | `K26`, `GPT55`, `Sonnet46`, `Opus47`, `Haiku45` |
| `RunNN` | Laufende Nummer fuer diesen Agent+Model-Kombi | `Run01`, `Run02` ... |
| `thema` | 2-4 Worte, was gemacht wurde | `e2e_fix`, `frontend_fly`, `p0f_deploy` |

Beispiele:

```text
memory/runs/2026-04-30_Codex_GPT55-Run03_clean_repo_handoff.md
memory/runs/2026-04-30_Kimi_K26-Run01_frontend_fly.md
memory/runs/2026-04-30_Copilot_Sonnet46-Run02_p0f_fix.md
memory/runs/2026-04-30_Opus47_Opus47-Run01_adr_architecture.md
memory/runs/2026-04-30_Haiku_Haiku45-Run01_runlog_update.md
```

### Minimalformat (5 Zeilen)

```markdown
---
name: 2026-04-30_Kimi_K26-Run01_e2e_fix
type: run
---
## Goal
## Done
## Surprised by
## Avoided
## Next
```

Erweitert wenn noetig, aber niemals kuenzer als diese 5 Zeilen.

### Regeln

1. **Sofort nach Session-Ende schreiben.** Nicht "merken wir uns fuer spaeter". Spaeter existiert nicht.
2. **Faktisch, nicht spekulativ.** Was wurde getan, nicht was haette getan werden koennen.
3. **Fehler dokumentieren.** Was schlug fehl und warum. Nichts verschweigen.
4. **Verweise auf Dateien.** Welche Dateien wurden erstellt/veraendert/entfernt.
5. **Pointer in MEMORY.md setzen.** Jeder Run-Log bekommt eine Zeile in MEMORY.md.

### Prompt-Zyklus Pflicht (hart)

1. Ein Prompt = ein Run-Log.
2. Agentname muss den tatsaechlichen Coding-Agenten enthalten (`Copilot`, `Codex`, `Kimi`, `Opus`, `Sonnet`, `Haiku`).
3. Modellfeld muss die tatsaechliche Modellfamilie enthalten (`GPT53Codex`, `GPT55`, `Sonnet46`, `Opus47`, `Haiku45`, `K26`).
4. `RunNN` wird pro Agent+Modell fortlaufend hochgezaehlt.
5. Fehlt der Log, gilt der Prompt als nicht abgeschlossen.

### MEMORY.md Update

Nach jedem Run-Log folgende Zeile in MEMORY.md anhaengen:

```markdown
- **YYYY-MM-DD** — [Thema](runs/YYYY-MM-DD_Agent_Model-RunNN_thema.md) — Agent: Kimi/K26 — Status: ✅ Done
```

---

## 4. Tool-Matrix — Was Wann Wie

### 4.1 Shell — Wann und wie

**Nutzen fuer:**
- `git`, `gh`, `docker`, `npm`, `pytest`, `ssh`
- Datei-Listing und schnelle Reads
- Secret-Setzen via `gh secret set`
- Verifikation (typecheck, lint, test, build)

**PowerShell-Regeln (NICHT verhandelbar):**

| Nie verwenden | Stattdessen | Beispiel |
|---------------|-------------|----------|
| `&&` | `;` | `cd code; npm test` |
| `||` | `if (-not $?)` | `command; if (-not $?) { echo "fail" }` |
| `$PWD/...` | `$env:PWD` oder explizite Pfade | `cd code; $PWD` funktioniert, aber `$PWD/.venv` nicht |

**Timeout-Regeln:**
- Standard: 60s
- `npm install`, `docker build`, `pytest` volle Suite: 120s
- OneDrive-Pfade: +30s draufrechnen

**Python venv Quirk:**
- `code/.venv313` hat **Windows-Style** `Scripts\python.exe` (nicht `bin/python`)
- Der alte `code/.venv` hatte Linux-style `bin/` — das wurde bereinigt
- Immer pruefen:
  ```powershell
  Get-ChildItem code\.venv313
  ```

**Beispiel-Template fuer Backend-Tests:**

```powershell
cd "c:\Users\tubbeTEC\OneDrive\z\Documents\Claude\Projects\Carotis AI\code"
$env:PYTHONPATH="backend"
$env:DEBUG="true"
.\.venv313\Scripts\python.exe -m pytest tests\test_rohde_walkthrough_e2e.py -v --tb=short
```

### 4.2 ReadFile — Wann und wie

**Nutzen fuer:**
- Bestehende Dateien lesen (bis 1000 Zeilen)
- Partielles Lesen mit `line_offset` und `n_lines`
- Negative `line_offset` fuer Tail-Reads (Logs: `line_offset=-100`)

**Regeln:**
- IMMER `n_lines` setzen bei grossen Dateien. Nie blind die ganze Datei lesen.
- Mehrere Dateien parallel lesen (multi_tool_use.parallel).
- Bei unbekannten Dateien erst `Shell` mit `Select-String` oder `Get-Content -TotalCount 50`.

### 4.3 WriteFile — Wann und wie

**Nutzen fuer:**
- Neue Dateien erstellen
- Kleine Dateien komplett ueberschreiben (< 100 Zeilen)
- Markdown-, YAML-, Config-Dateien

**Regeln:**
- NIEMALS Secrets schreiben.
- Bei > 100 Zeilen: `overwrite` fuer ersten Block, dann `append`.
- Immer pruefen, ob Datei bereits existiert (nicht unbeabsichtigt ueberschreiben).

### 4.4 StrReplaceFile — Wann und wie

**Nutzen fuer:**
- Gezielte Edits in bestehenden Dateien
- Multi-Edit in einer Datei (Array von edits)
- Code-Aenderungen ohne Formatierung zu zerstoeren

**Regeln:**
- `old` String muss exakt matchen (inkl. Whitespace).
- Bei mehreren Aenderungen in derselben Datei: Array von edits nutzen.
- `replace_all: true` nur wenn ABSICHT alle Vorkommen ersetzen.
- Nach StrReplaceFile IMMER verifizieren (lesen oder testen).

### 4.5 Grep — Wann und wie

**Nutzen fuer:**
- Suchen nach Patterns in Code
- Finden von Funktionsdefinitionen, Imports, Config-Werten
- `output_mode: files_with_matches` fuer schnelles Scoping

**Regeln:**
- `pattern` ist ripgrep-Syntax (nicht grep).
- `-C 3` fuer Context um Matches.
- `head_limit: 20` bei vielen Matches.
- `glob: "*.py"` oder `type: py` fuer Dateityp-Filter.

### 4.6 Glob — Wann und wie

**Nutzen fuer:**
- Dateien finden nach Pattern
- Verzeichnisstruktur erkunden

**Regeln:**
- NIEMALS `**` am Anfang verwenden (wird abgelehnt).
- Stattdessen: `src/**/*.py`, `backend/app/**/*.py`.
- `include_dirs: false` wenn nur Dateien gebraucht werden.

### 4.7 Agent (Subagent) — Wann und wie

**Nutzen fuer:**
- Parallele Erkundung unabhaengiger Code-Bereiche
- Fokussierte Subtasks (z.B. "Finde alle Orte wo X verwendet wird")
- Read-only Research (`subagent_type: explore`)

**Regeln:**
- NIE fuer Aufgaben, die der Parent-Agent direkt erledigen kann.
- NIE fuer sequentielle Abhaengigkeiten.
- IMMER kompletten Kontext im Prompt mitgeben (Subagent sieht Parent-Kontext nicht).
- `run_in_background: true` nur wenn Ergebnis nicht sofort gebraucht wird.

### 4.8 GitHub CLI `gh` — Wann und wie

Funktioniert auf diesem Rechner:

```powershell
gh auth status
gh secret list --repo DiggAiHH/CarotisAi
gh secret set NAME --repo DiggAiHH/CarotisAi
gh pr create --repo DiggAiHH/CarotisAi
```

Regeln:
- Secrets niemals ausgeben.
- Secrets nur aus Datei/stdin in GitHub Secrets schreiben.
- PR statt direkter Merge auf `master`.
- Vor PR: `git status --short --branch`.

### 4.9 MCP / Playwright / Browser — Wann und wie

**Verfuegbare MCP-Server:**
- `playwright` — Browser-Automation
- `github` — GitHub API (Issues, PRs, Repos, Code-Search)
- `context7` — Library-Dokumentation (resolve-library-id + query-docs)

**Wann nutzen:**
- Playwright: Nur fuer tatsaechliche Browser-Automation (nicht fuer Doku lesen — FetchURL ist schneller).
- GitHub MCP: Wenn `gh` CLI nicht ausreicht (z.B. Code-Search ueber Repos, Issue-Management).
- Context7: Wenn Library-Doku gebraucht wird (Next.js, FastAPI, SQLAlchemy, etc.).

**Regeln:**
- `browser_navigate` + `browser_snapshot` fuer Seiten-Struktur.
- `browser_evaluate` fuer JS-Checks.
- `browser_take_screenshot` nur wenn User explizit fragt.
- `search_code` fuer GitHub-weite Code-Suche (nicht lokale Suche).

### 4.10 Verbindliche Tool-Call-Reihenfolge (Copilot/Codex Harness)

Diese Reihenfolge gilt fuer die meisten Engineering-Prompts. Nur bei gutem Grund abweichen und im Run-Log dokumentieren.

1. Kontext-Scope: `search_subagent` (quick/medium) fuer erste Orientierung.
2. Verifikation des Kontexts: `read_file` fuer exakte Dateien/Abschnitte.
3. Plan/Tracking: `manage_todo_list` bei mehrschrittigen Aufgaben.
4. Editieren: `apply_patch` (bevorzugt) fuer gezielte Aenderungen; nur bei Neudateien `create_file`.
5. Verifikation: `run_in_terminal` fuer typecheck/lint/tests/build.
6. Fehlercheck: `get_errors` falls IDE-Probleme vermutet werden.
7. Abschlusscheck: `get_changed_files` fuer Delta-Review vor Handoff.

Avoid:
- Kein blindes Multi-File-Rewrite ohne vorherigen Read.
- Keine destruktiven Git-Befehle (`reset --hard`, `checkout --`) ohne expliziten User-Wunsch.
- Kein Tool-Hopping ohne klares Exit-Kriterium.

### 4.11 Connector/Skill/Plugin Aktivierungsstrategie

Wichtig: Nicht "alle gleichzeitig" aktivieren. Immer minimal noetiges Set, dann erweitern.

Prioritaet:
1. Lokal (`search_subagent`, `read_file`, `run_in_terminal`) fuer schnelle, reproduzierbare Antworten.
2. Repo/PR-Connectoren (`github`, `gh`) nur wenn lokal nicht reicht.
3. Browser/Playwright nur fuer echte UI-/E2E-Verifikation.
4. Doku-Connector (`context7`) bei API-/Library-Unsicherheit.
5. Deep-Web-Recherche nur falls 1-4 keine belastbare Antwort liefern.

Skill-Regel:
- Skill nur aktivieren, wenn klarer Task-Fit vorliegt.
- Bei Skill-Nutzung immer lokale Verifikation nachziehen (Tests/Build/Readback).
- Keine Cloud-Connector fuer Patientendaten.
- Neue Codex-Skills seit 2026-05-02: `browser-harness`, `caveman`, `compress`, `obsidian`, `remotion-best-practices`. Operative Aufgaben und Stop-Regeln: `memory/domain/skill_team_harness_2026-05-02.md`.
- Default fuer externe UIs/Vaults/Provider ist read-only. Schreibaktionen, Deploys, DNS-Saves, Token-Operationen und Vault-Syncs nur mit explizitem User-Go.


### 4.12 Claude Design Browser Harness (claude.ai/design)

**Projekt-URL Pattern:**
```
https://claude.ai/design/p/<project-id>?file=<filename.html>
```
Carotis AI Prototype: `https://claude.ai/design/p/019de4bf-5dbc-7c47-b1fe-8a0466e64c9c?file=Carotis+AI.html`

**Chat Composer (für Prompts):**
```js
// Einfuegen — bevorzuge .fill() statt .type() fuer grosse Texte
await page.getByTestId('chat-composer-input').click();
await page.getByTestId('chat-composer-input').fill('dein prompt hier');
// Senden
await page.getByTestId('chat-send-button').click();
```

**Starter Chips (Kontext-Injection vor Tippen):**
- "Hi-fi design" — triggert high-fidelity design mode
- "Interactive prototype" — triggert React useState/useEffect interactions
- "Design System (design system)" — bindet das verknuepfte Design-System ein
- Chips per Snapshot-Ref anklicken: `[ref=e286]`, `[ref=e288]`, `[ref=e289]` (koennen variieren)

**Tweaks Panel:**
- Oeffnet sich automatisch bei erstem Prototype-Render und ueberlappt Column 3
- Schliessen: Klick auf "Tweaks" Toggle-Switch in der Toolbar (blaues Switch-Element, ~x=490, y=43)
- Falls Selector nicht greift: `page.mouse.click(490, 43)`
- Snapshot-Ref: `[ref=e739]` — `generic "Toggle tweak controls"`
- Inhalt: Accent Color Swatch, AI Panel Width Slider, Show Annotations Toggle, Heatmap Default On Toggle

**iframe-Struktur:**
- Prototype laeuft in Cross-Origin-iframe: `<project-id>.claudeusercontent.com`
- Parent-Frame: Claude Design UI (Toolbar, Tweaks, Chat)
- Prototype-Interaktionen (Tab-Bar, Buttons, Inputs) via `page.frames()` iterieren:
```js
const frames = page.frames();
for (const frame of frames) {
    try {
        const btn = await frame.$('button:has-text("Patients")');
        if (btn) { await btn.click(); break; }
    } catch(e) {}
}
```

**Generation-Complete-Signale (in dieser Reihenfolge):**
1. File-Tab erscheint oben: z.B. "Carotis AI.html"
2. "Verifier agent check completed" Zeile im Chat
3. Claude-Nachricht: "Fixed — [...]. Everything should be working as expected."
4. Console-Errors bleiben ggf. (non-blocking React dev warnings)

**Wait-Strategie fuer grosse Prototypen:**
```
15s → 30s → 45s → 60s (warten auf file-tab erscheinen)
Danach: warten auf "verifier" text im Chat
```

**Verifier Agent:**
- Laeuft automatisch nach jeder Generation
- Fangt und fixt Runtime-Errors (React-Hooks, Destructuring-Fehler, etc.)
- **Beispiel aus Run03**: `const { showAnnotations } = useTweaks()` war falsch → auto-korrigiert
- Kein manueller Trigger noetig
- Ausgabe: "Verifier agent check completed" + Auto-Fix-Nachricht

**Dateien in einem Projekt:**
- Claude Design generiert mehrere Komponenten-Dateien (nicht monolithisch)
- z.B. `tweaks-panel.jsx`, `DicomViewer.jsx`, `Carotis AI.html`
- Alle unter dem gleichen Projekt-Tab sichtbar

**Prototype-Code downloaden (manuell):**
- Im Claude Design Toolbar: Edit-Button → zeigt Quellcode der aktiven Datei
- Oder: HTTP-GET direkt auf iframe-URL (cross-origin blockiert, nur via Browser DevTools)

**Dialog-Handling:**
- `beforeunload`-Dialog kann beim Screenshot aufpoppen
- Dismiss mit: `await page.once('dialog', d => d.dismiss())`

**Anti-Patterns:**
- ❌ `mcp_microsoft_pla_browser_type` ohne Iframe-Frame-Kontext fuer prototype-interne Elemente
- ❌ Tweaks Panel ignorieren — blockiert AI Panel Screenshot
- ❌ Zu frueh screenshotten (vor Generation-Complete-Signalen)
- ❌ `fill()` mit > 2000 Zeichen auf manchen Browsern — stattdessen in chunks aufteilen
- ❌ Mobile-first Layout auf Desktop testen ohne Viewport-Check (Viewport < 1024px zeigt Tabs statt 3-Spalten)

### 4.13 Playwright E2E Smoke Patterns

**Sichtbare Screenshots in CI:**
```ts
import { test, expect } from "@playwright/test";

test("visual smoke", async ({ page }, testInfo) => {
  await page.goto("http://localhost:3000");
  const screenshot = await page.screenshot();
  await testInfo.attach("screenshot", {
    body: screenshot,
    contentType: "image/png",
  });
});
```
- Niemals `require("fs")` in ESM-Playwright-Tests — `testInfo.attach()` ist nativ.

**AuthGate Backend-Dependency:**
- AuthGate validiert Token gegen `/api/v1/demo/whoami` — ohne Backend bleibt es auf "Server nicht erreichbar".
- **Workarounds**: (a) Backend starten, (b) `VITE_SKIP_AUTH=true` fuer E2E-Build, (c) Mock-Service-Worker.

**Token-Gate Login Helper:**
```ts
async function loginIfGateVisible(page: Page) {
  try {
    await page.waitForSelector('[data-testid="demo-token-input"]', { timeout: 3000 });
    await page.fill('[data-testid="demo-token-input"]', "test-token-" + Date.now());
    await page.click('[data-testid="token-submit"]');
    await page.waitForSelector("[data-testid='main-app']", { timeout: 5000 });
  } catch {
    // Gate nicht sichtbar — bereits eingeloggt oder Skip-Auth
  }
}
```

**Viewport-Matrix fuer Responsive-Test:**
```ts
const viewports = [
  { name: "desktop", width: 1280, height: 720 },
  { name: "mobile", width: 375, height: 667 },
];
for (const vp of viewports) {
  test(`smoke ${vp.name}`, async ({ page }) => {
    await page.setViewportSize({ width: vp.width, height: vp.height });
    // ...
  });
}
```
---

## 5. Tool-Anti-Patterns — Was Zu Vermeiden

| Anti-Pattern | Warum schlecht | Stattdessen |
|--------------|----------------|-------------|
| Groesse Datei mit WriteFile ueberschreiben | Verliert Formatierung, Comments, unbeabsichtigte Aenderungen | StrReplaceFile mit gezielten edits |
| Shell `sed` oder `awk` fuer Datei-Edits | Nicht portabel, zerstoert Encoding | StrReplaceFile oder WriteFile |
| `&&` in PowerShell | Parser-Error | `;` oder `if ($?)` |
| `$PWD/...` in PowerShell-Expression | Parser-Error bei `/` in Pfad | `cd code; .\.venv313\Scripts\python.exe` |
| Python-Imports auf Modul-Level ohne Env-Setup | `create_app()` bricht bei fehlenden env vars | `os.environ` setzen VOR dem Import |
| Test-DB teilen zwischen Tests | UNIQUE-Fehler, flaky Tests | Unique Tokens/IDs pro Test, oder DB reset |
| `application/octet-stream` fuer DICOM-Uploads | Inference-Service erwartet `application/dicom` | Korrekten MIME-Type setzen |
| Leeres Dict `{}` fuer `vulnerability_markers` | Schema required 4 spezifische Keys | Alle Keys mit Werten senden |
| `AsyncClient(app=app)` | Deprecated in httpx | `AsyncClient(transport=ASGITransport(app=app))` |
| Frontend-Tests mit `--run` bei jsdom/WASM | Haengt sporadisch | Timeout 120s oder einzeln laufen |
| Secrets in Chat oder Run-Logs | Kompromittierung | GitHub Secrets, nie in Text |
| `Math.random()` in `useRef` | Instabile IDs bei Re-Renders | `crypto.randomUUID()` |
| `URL.createObjectURL()` ohne `revokeObjectURL()` | Memory Leak in Browser | Ref mit Cleanup in useEffect |
| `parents[4]` Pfad-Resolution | Bricht wenn Datei verschoben | `get_settings().project_root` |
| `import os` inside Method | Schlechte Praxis, unnoetig | Modul-Level import |
| FastAPI 0.115.5 + Starlette 1.0.0 | `TypeError: Router.__init__() got unexpected keyword argument 'on_startup'` | FastAPI auf >=0.136.1 upgraden |
| sklearn Import-Reihenfolge | `_import_sklearn()` gab vertauschte Tupel | `(LogisticRegression, IsotonicRegression)` statt `(Isotonic, Logistic)` |
| `dependencies.py` dupliziert `security.py` | Inkonsistente Auth-Behavior | Re-export aus `security.py` |
| Hardcoded URLs in CSP/Middleware | Nicht konfigurierbar | `csp_connect_src` aus Config |

---

## 6. Aktuelle Secrets

Gesetzt in GitHub Repo `DiggAiHH/CarotisAi`:

```text
ACME_EMAIL
ADMIN_API_KEY
API_KEY
ANONYMIZATION_SALT
HETZNER_SERVER_IP
HETZNER_SSH_PRIVATE_KEY
HETZNER_SSH_USER
```

Noch blockiert:

```text
FLY_API_TOKEN
```

Unklar/Alt:

```text
CAROTISAI
```

Regel: Kein Agent liest oder printed Secret-Werte. Nur Existenz pruefen.

---

## 7. Deploy-Architektur P0f

Trigger-Regel fuer neue Agenten: Wenn der User "Deploy", "mach online", "bring carotis online", "DNS", "INWX", "carotis erreichbar" oder aehnlich sagt, lies zuerst:

```text
CLAUDE.md Phase P0f
memory/domain/p0f_deploy_state_compact_2026-05-02.md
memory/runs/2026-05-04_Codex_GPT55-Run15_dns_hetzner_proxy.md
deploy/Caddyfile.backend
deploy/hetzner-backend.compose.yml
```

Aktueller Fallback:

```text
api.carotis.diggai.de -> Hetzner 204.168.230.127
carotis.diggai.de     -> Hetzner 204.168.230.127
```

Historischer Zielplan, derzeit durch Fly-Billing blockiert:

```text
carotis.diggai.de -> Fly.io
config: deploy/fly.frontend.toml
dockerfile: deploy/Dockerfile.frontend-fly
```

Backend:

```text
api.carotis.diggai.de -> Hetzner 204.168.230.127
compose: deploy/hetzner-backend.compose.yml
caddy: deploy/Caddyfile.backend
server path: /opt/carotis-ai
```

DNS in INWX:

```text
api.carotis     A      204.168.230.127
carotis         A      204.168.230.127
```

Nicht setzen, solange Fly 502 liefert:

```text
carotis         CNAME  carotis-ai-frontend.fly.dev
```

Falls Fly-Billing spaeter repariert wird und wieder Fly als Frontend-Ziel genutzt werden soll, erst Fly-App/Cert pruefen:

```powershell
fly certs show carotis.diggai.de --config deploy/fly.frontend.toml
```

---

## 8. Windows PowerShell Quirks

Dieser Rechner laeuft Windows mit PowerShell als Default-Shell. Folgende Quirks sind fuer Agenten relevant:

1. **Keine `&&` / `||`**: PowerShell verwendet `;` fuer Sequenzierung. Bei bedingter Ausfuehrung:
   ```powershell
   command1; if ($?) { command2 }
   ```
   oder `try/catch` fuer Fehlerbehandlung.

2. **OneDrive-Pfade sind langsam**: `C:\Users\tubbeTEC\OneDrive\...` haben Latenz bei vielen Dateioperationen. Timeouts in Shell-Kommandos erhoehen (60s -> 120s bei `npm install`, `docker build`, `pytest`).

3. **Python venv Path**: `code/.venv313` hat Windows-style `Scripts\python.exe`. Der alte `code/.venv` mit Linux-style `bin/` wurde bereinigt.
   ```powershell
   Get-ChildItem code/.venv313
   ```

4. **Python 3.14 bricht bei pydantic-core**: System-Python ist 3.14.0. `pydantic-core==2.27.1` hat keine Wheels fuer 3.14 und bricht beim Build (Rust-Compiler noetig). Fuer Backend-Arbeit immer Python 3.13.12 via uv nutzen:
   ```powershell
   & "C:\Users\tubbeTEC\AppData\Roaming\uv\python\cpython-3.13.12-windows-x86_64-none\python.exe" --version
   ```

5. **Pfad-Trennzeichen**: In PowerShell-Expressions mit `/` als Operator vorsichtig sein. In Strings ist `/` okay, aber in Expressions kann es als Division interpretiert werden. Besser `\` verwenden oder Strings quoten.

6. **Env-Var Export**: Kein `export`, sondern `$env:VAR="value"`.
   ```powershell
   $env:DEBUG="true"
   $env:PYTHONPATH="backend"
   ```

7. **Process-Substitution**: Kein `<(...)` oder `>(...)`. Stattdessen temporaere Dateien oder Pipes.

8. **Single Quotes**: PowerShell expandiert `$var` in double quotes. In single quotes nicht. Bei Regex-Patterns mit `$` single quotes verwenden.

9. **`rg` (ripgrep) Quotes**: In PowerShell einfache Quotes `'pattern'` oder Escaping verwenden fuer Regex.

10. **Docker Desktop**: Muss laufen fuer lokale Container-Tests. Compose-Dateien sind Linux-Format, Docker Desktop uebersetzt.

---

## 9. Python Auf Diesem Rechner

Verfuegbar:

```text
Python 3.14 system default
Python 3.13.12 via uv path:
C:\Users\tubbeTEC\AppData\Roaming\uv\python\cpython-3.13.12-windows-x86_64-none\python.exe
```

Aktive venv:

```text
code/.venv313 (Windows-Style, Scripts/python.exe)
```

Wichtig:

- Backend `.venv313` funktioniert mit allen Dependencies.
- Fuer Backend-Tests immer `.venv313` nutzen.
- Wenn neu gebraucht:

```powershell
cd "c:\Users\tubbeTEC\OneDrive\z\Documents\Claude\Projects\Carotis AI\code"
& "C:\Users\tubbeTEC\AppData\Roaming\uv\python\cpython-3.13.12-windows-x86_64-none\python.exe" -m venv .venv313
& .\.venv313\Scripts\python.exe -m pip install -r backend\requirements.txt
```

Test mit sauberem `DEBUG`:

```powershell
cd "c:\Users\tubbeTEC\OneDrive\z\Documents\Claude\Projects\Carotis AI\code"
$env:PYTHONPATH="backend"
$env:DEBUG="true"
.\.venv313\Scripts\python.exe -m pytest tests -p no:warnings
```

Bekanntes Ergebnis (Stand 2026-05-01):

```text
120 passed, 11 skipped, 0 failed
```

Alle Tests sind gruen. sklearn wurde installiert (1.8.0) und der Import-Bug fixiert.

Ohne `DEBUG=true` koennen Config-Tests scheitern, wenn die Shell `DEBUG=release` geerbt hat.

### pytest.ini Konfiguration

```ini
[pytest]
filterwarnings =
    error
    ignore::DeprecationWarning:passlib
    ignore::DeprecationWarning:pydicom
    ignore::DeprecationWarning:starlette
    ignore::DeprecationWarning:fastapi
```

`ignore::DeprecationWarning:fastapi` ist noetig fuer FastAPI 0.136.1 + Starlette 1.0.0.

---

## 10. Frontend Verifikation

Pfad:

```powershell
cd "code\frontend"
```

Kommandos:

```powershell
npm run typecheck
npm run lint
npm run build
```

Vitest (optional, kann haengen):

```powershell
npm test -- --run
```

Bekannte Ergebnisse:

- Typecheck: gruen.
- Lint: gruen.
- Build: gruen, aber Vite/Cornerstone WASM-Warnungen und grosse Chunks sind bekannt.
- Vitest: 29 passed (6 files) ist aktuelle Baseline.
- Playwright E2E: `chromium_visual_smoke.spec.ts` 1 passed (18.5s) — Desktop + Mobile Screenshot.

Playwright E2E-Smoke (neu):

```powershell
npm run e2e
```

Expected Baseline (2026-05-01): Desktop+Mobile Smoke gruen, kein Blank Screen am Token-Gate.

Warnungen nicht reflexiv fixen, wenn sie aus Cornerstone/WASM kommen und Build erfolgreich ist.

---

## 11. Backend Verifikation

Pfad:

```powershell
cd "code"
```

Kommandos:

```powershell
$env:PYTHONPATH="backend"
$env:DEBUG="true"
.\.venv313\Scripts\python.exe -m pytest tests -p no:warnings
.\.venv313\Scripts\python.exe -m ruff check backend\app tests
.\.venv313\Scripts\python.exe -m black --check backend\app tests
```

E2E-Tests spezifisch:

```powershell
$env:PYTHONPATH="backend"
$env:DEBUG="true"
.\.venv313\Scripts\python.exe -m pytest tests\test_rohde_walkthrough_e2e.py -v --tb=short
```

Smoke-Tests spezifisch:

```powershell
$env:PYTHONPATH="backend"
$env:DEBUG="true"
.\.venv313\Scripts\python.exe -m pytest tests\test_smoke.py -v --tb=short
```

Wenn `pytest` ohne Einschraenkung auch `ml/` sammelt, koennen fehlende ML-Extras blockieren:

```text
monai
timm
mlflow
```

Dann fuer Backend-Arbeit gezielt `pytest tests` nutzen.

---

## 12. E2E-Test-Wissen — Lessons From S15

`tests/test_rohde_walkthrough_e2e.py` ist das Muster fuer E2E-Tests in diesem Projekt.

### Korrektes E2E-Test-Setup

```python
import os

# 1. Env-Vars VOR allen app-Imports setzen
os.environ["API_KEY"] = "a" * 32
os.environ["ADMIN_API_KEY"] = "b" * 32
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"
os.environ["ONNX_MODEL_PATH"] = "/nonexistent/model.onnx"
os.environ["ANONYMIZATION_SALT"] = "s" * 16
os.environ["DEBUG"] = "true"

# 2. ERST dann importieren
from app.main import create_app
from app.schemas.inference import PredictionResponse
```

### Inference-Service mochen

```python
from unittest.mock import AsyncMock, MagicMock

mock_svc = MagicMock()
mock_svc.model_loaded = True
mock_svc.predict = AsyncMock(return_value=PredictionResponse(...))
app.state.inference_service = mock_svc
```

### ASGITransport (nicht veraltetes app=)

```python
from httpx import ASGITransport, AsyncClient

async with AsyncClient(
    transport=ASGITransport(app=app),
    base_url="http://test",
    follow_redirects=True,
) as client:
    yield client
```

### Unique Tokens und IDs pro Test

```python
import uuid

def _make_token() -> str:
    return f"test-{uuid.uuid4().hex}"
```

Jeder Test bekommt eigenen Token, eigene case_id, eigene physician_role_hash. Nie wiederverwenden.

### DecisionTreeRequest Schema (exakt)

```python
payload = {
    "case_id": "d" * 64,  # exakt 64 hex chars
    "captured_at": "2026-04-30T12:00:00Z",
    "physician_role_hash": "b" * 64,  # exakt 64 hex chars
    "ai_prediction": {
        "stenosis_pct_nascet": 65.0,
        "confidence": 0.85,
        "vulnerability_markers": {
            "intraplaque_hemorrhage": 0.0,     # REQUIRED
            "thin_fibrous_cap": 0.0,           # REQUIRED
            "lipid_rich_necrotic_core": 0.0,   # REQUIRED
            "systolic_motion_anomaly": 0.0,    # REQUIRED
        },
        "model_version": "v0.3.2",
        "model_sha": "abc123d",
    },
    "physician_decision": {
        "stenosis_pct_nascet": 65.0,
        "confirmed_markers": [],
        "rejected_markers": [],
        "added_markers": [],
    },
    "agreement_with_ai": {
        "verdict": "full_agreement",
        "delta_pct": 0.0,
        "trust_score_for_this_case": 4,
    },
    "anonymisation": {
        "method": "DICOM_PS_3.15_basic",
        "salt_version": "v2026-04",
        "audit_id": "AT-001",
        "k_anonymity_min": 5,
    },
}
```

### Audit-Trail Auth (beide Keys)

```python
res = await client.get(
    "/api/v1/audit/trail",
    headers={"X-API-Key": TEST_API_KEY, "X-Admin-Key": ADMIN_API_KEY},
)
```

---

## 13. Modellrouting

| Aufgabe | Modell / Agent | Wann genau |
|---|---|---|
| Architektur, ADR, regulatorische Texte | Opus 4.7 | Wenn Trade-offs, Stakeholder-Kommunikation, regulatorische Entscheidungen |
| Code-Implementierung, Debugging, Bugfix | Codex GPT-5.5 / Sonnet 4.6 | Wenn Code geschrieben, refactored oder getestet werden muss |
| Atomare Edits, Run-Logs, i18n, Rename | Haiku 4.5 | Wenn exakte Datei+Zeile bekannt, kein Denken noetig |
| Bulk-Prompts, Office-Drafts, Stride-Prompts | Kimi K2.6 | Wenn viele Dateien gleichzeitig, klare Grenzen |
| PR-Review und Regression-Risiko | Codex / Sonnet | Vor Merge, Code-Review |
| Deep Research, Literatur, Marktanalyse | Opus 4.7 | Wenn gruendliche Recherche mit Quellen noetig |

Subagenten:

- Nur wenn der User explizit parallele Agenten/Subagenten will.
- Disjunkte Datei-Ownership definieren.
- Nicht denselben Stack doppelt bearbeiten lassen.
- Danach Integrationsrunde lokal.

---

## 14. Skills Und Connectors — Vollstaendiges Inventar

Verfuegbare Skills in dieser Umgebung (Stand 2026-04-30). Skill nur einsetzen, wenn Aufgabe klar passt oder User ihn nennt. `SKILL.md` lesen, nicht blind aus Beschreibung handeln. Keine Connector-/Provider-Aktion mit Patientendaten.

### Code-Qualitaet & Patterns

| Skill | Pfad | Zweck | When-to-Use |
|-------|------|-------|-------------|
| `coding-standards` | `.claude/skills/coding-standards` | Universal TS/JS/React/Node Best Practices | Code-Review oder neuer Code |
| `python-patterns` | `.claude/skills/python-patterns` | Pythonic Idioms, PEP 8, Type Hints | Python-Refactoring oder neue Module |
| `java-coding-standards` | `.claude/skills/java-coding-standards` | Java/Spring Boot Naming, Immutability | Java-Code-Arbeit |
| `golang-patterns` | `.claude/skills/golang-patterns` | Idiomatic Go Patterns | Go-Code-Arbeit |
| `backend-patterns` | `.claude/skills/backend-patterns` | Node.js/Express/Next.js API Patterns | Backend-API-Design |
| `frontend-patterns` | `.claude/skills/frontend-patterns` | React/Next.js State, Performance, UI | Frontend-Architektur |
| `vercel-react-best-practices` | `.claude/skills/vercel-react-best-practices` | Vercel Engineering React/Next Performance | React-Komponenten-Optimierung |
| `vercel-composition-patterns` | `.claude/skills/vercel-composition-patterns` | Compound Components, Render Props | Boolean-Prop-Proliferation |
| `jpa-patterns` | `.claude/skills/jpa-patterns` | JPA/Hibernate Entity Design, Queries | Spring Data/JPA-Arbeit |
| `django-patterns` | `.claude/skills/django-patterns` | Django Architecture, DRF, ORM, Caching | Django-Arbeit |
| `springboot-patterns` | `.claude/skills/springboot-patterns` | Spring Boot REST, Services, Async | Spring Boot-Arbeit |
| `postgres-patterns` | `.claude/skills/postgres-patterns` | PostgreSQL Schema, Queries, Indexing | DB-Design oder Query-Optimierung |
| `clickhouse-io` | `.claude/skills/clickhouse-io` | ClickHouse Analytics, Data Engineering | Analytische Workloads |

### Testing & Verification

| Skill | Pfad | Zweck | When-to-Use |
|-------|------|-------|-------------|
| `python-testing` | `.claude/skills/python-testing` | pytest, TDD, Fixtures, Mocking, Coverage | Neue Python-Features oder Bugs |
| `golang-testing` | `.claude/skills/golang-testing` | Table-Driven Tests, Benchmarks, Fuzzing | Go-Tests |
| `django-tdd` | `.claude/skills/django-tdd` | pytest-django, Factory Boy, Mocking | Django-Feature-Entwicklung |
| `springboot-tdd` | `.claude/skills/springboot-tdd` | JUnit 5, Mockito, MockMvc, Testcontainers | Spring Boot-Feature-Entwicklung |
| `tdd-workflow` | `.claude/skills/tdd-workflow` | TDD mit 80%+ Coverage | Feature, Bugfix oder Refactoring |
| `verification-loop` | `.claude/skills/verification-loop` | Comprehensive Verification | Vor Release oder PR |
| `springboot-verification` | `.claude/skills/springboot-verification` | Build, Static Analysis, Tests, Security | Vor Spring Boot-Release |
| `django-verification` | `.claude/skills/django-verification` | Migrations, Linting, Tests, Security | Vor Django-Release |
| `eval-harness` | `.claude/skills/eval-harness` | Eval-Driven Development (EDD) | Komplexe Features mit Eval-Kriterien |

### Security

| Skill | Pfad | Zweck | When-to-Use |
|-------|------|-------|-------------|
| `security-review` | `.claude/skills/security-review` | Security Checklist fuer Auth, Input, Secrets | Bei sensiblen Features |
| `security-scan` | `.claude/skills/security-scan` | Scan `.claude/` Config auf Vulnerabilities | Bei Agent-Konfig-Aenderungen |
| `django-security` | `.claude/skills/django-security` | Django Auth, CSRF, SQL Injection, XSS | Django-Auth oder Security-Hardening |
| `springboot-security` | `.claude/skills/springboot-security` | Spring Security Auth, Validation, Secrets | Spring Security-Arbeit |

### Content & Media

| Skill | Pfad | Zweck | When-to-Use |
|-------|------|-------|-------------|
| `article-writing` | `.claude/skills/article-writing` | Long-Form Content, Guides, Blog Posts | Artikeln > 1 Absatz |
| `content-engine` | `.claude/skills/content-engine` | Social Posts, Threads, Scripts, Calendars | Multi-Platform Content |
| `crosspost` | `.claude/skills/crosspost` | Multi-Platform Distribution | Cross-Platform Posting |
| `x-api` | `.claude/skills/x-api` | X/Twitter API OAuth, Tweets, Threads | X-API-Integration |
| `fal-ai-media` | `.claude/skills/fal-ai-media` | Image/Video/Audio Generation via fal.ai | Media-Generation |
| `video-editing` | `.claude/skills/video-editing` | AI-Assisted Video Editing Pipeline | Video-Bearbeitung |
| `videodb` | `.claude/skills/videodb` | Video Ingest, Understand, Act | Video-Analyse oder -Processing |
| `frontend-slides` | `.claude/skills/frontend-slides` | HTML Presentations from PPT or scratch | Praesentations-Erstellung |

### Research & Intelligence

| Skill | Pfad | Zweck | When-to-Use |
|-------|------|-------|-------------|
| `deep-research` | `.claude/skills/deep-research` | Multi-Source Research mit Firecrawl/Exa | Gruendliche Recherche |
| `market-research` | `.claude/skills/market-research` | Market Sizing, Competitor Analysis | Business-Entscheidungen |
| `exa-search` | `.claude/skills/exa-search` | Neural Search via Exa | Web/Code/Company-Recherche |
| `iterative-retrieval` | `.claude/skills/iterative-retrieval` | Progressive Context Retrieval | Subagent-Orchestrierung |

### DevOps & Cloud

| Skill | Pfad | Zweck | When-to-Use |
|-------|------|-------|-------------|
| `microsoft-foundry` | `.agents/skills/microsoft-foundry` | Deploy/Evaluate Azure Foundry Agents | Azure Foundry Arbeit |

### Agent Infrastructure

| Skill | Pfad | Zweck | When-to-Use |
|-------|------|-------|-------------|
| `skill-creator` | Kimi intern | Guide fuer effektive Skills | Skill-Erstellung |
| `find-skills` | `.claude/skills/find-skills` | Discover und Install Agent Skills | Wenn User nach Skill fragt |
| `continuous-learning` | `.claude/skills/continuous-learning` | Extract Patterns zu Skills | Nach jeder Session |
| `continuous-learning-v2` | `.claude/skills/continuous-learning-v2` | Instinct-Based Learning | Nach jeder Session |
| `strategic-compact` | `.claude/skills/strategic-compact` | Manuelle Context Compaction | Bei langen Sessions |
| `dmux-workflows` | `.claude/skills/dmux-workflows` | Multi-Agent Orchestration mit tmux | Parallele Agent-Workflows |

### Investor & Business

| Skill | Pfad | Zweck | When-to-Use |
|-------|------|-------|-------------|
| `investor-materials` | `.claude/skills/investor-materials` | Pitch Decks, Memos, Financial Models | Fundraising-Material |
| `investor-outreach` | `.claude/skills/investor-outreach` | Cold Emails, Warm Intros, Follow-ups | Investor-Kontakt |

### Kimi-spezifisch

| Skill | Pfad | Zweck | When-to-Use |
|-------|------|-------|-------------|
| `kimi-cli-help` | Kimi intern | Kimi Code CLI Usage, Config, Troubleshooting | Bei Fragen zu Kimi selbst |

### Installierte Codex-Skills (2026-05-02)

| Skill | Pfad | Zweck | When-to-Use |
|-------|------|-------|-------------|
| `browser-harness` | `.codex/skills/browser-harness` | CDP-Browsersteuerung, Screenshots, UI-Smokes | Demo, Claude Design, Provider-UI read-only, responsive Checks |
| `caveman` | `.codex/skills/caveman` | Tokenarme, technische Kommunikation | Status, Triage, Handoff, Run-Logs; nicht fuer Security/Legal-Unklarheit |
| `compress` | `.codex/skills/compress` | Prosa-Memory-Kompression mit Backup | Nur Summary-first fuer Kern-Memorys; keine Code/Config/JSON/Env-Dateien |
| `obsidian` | `.codex/skills/obsidian` | Vault-Read/Search/Note-Entwuerfe mit Wikilinks | Backlinks, P0f-Notizen, Run-Log-Index; Vault-Writes nur mit Freigabe |
| `remotion-best-practices` | `.codex/skills/remotion-best-practices` | Remotion Video in React | Rohde-Demo-Video, 30fps Sequencing, lokale Assets, keine CSS-Animation |

Matrix + 50 Aufgaben: `memory/domain/skill_team_harness_2026-05-02.md`.

### MCP-Connectors (Nicht-Skills)

| Connector | Server | Zweck | When-to-Use |
|-----------|--------|-------|-------------|
| `github` | GitHub MCP | Repos, Issues, PRs, Code-Search, Commits | Wenn `gh` CLI nicht reicht |
| `playwright` | Playwright MCP | Browser-Automation, Screenshots, Evaluate | Echte Browser-Tests |
| `context7` | Context7 MCP | Library-Doku Query (Next.js, FastAPI, etc.) | Wenn Library-Doku gebraucht |
| `carotis-obsidian` | Lokaler MCP | Vault-CRUD, Backlinks, Search | Memory-Disziplin, Run-Logs |
| `carotis-graphify` | Lokaler MCP | Knowledge-Graph, Tags, Mermaid | Vault-Analyse |
| `carotis-hermes` | Lokaler MCP | Hermes-Proxy, Skills, Reflection | AI-Bridge zu Ollama |
| `carotis-browser` | Lokaler MCP | Playwright-Browser-Automation | Web-Recherche |
| `carotis-combined` | Lokaler MCP | Alle 4 Server in einem Prozess | Ressourcen-sparend |

---

## 15. Verbote

Niemals:

- Patientendaten in Cloud, Chat, Browser, GitHub, Fly, Hetzner-Logs oder externe APIs.
- Secrets in Dateien, Chat oder Remote-URLs.
- Direkt nach `master` pushen, wenn Branch-Schutz/PR gefordert ist.
- Office-Dokumente direkt editieren, wenn Stride-Prompt gefordert ist.
- `git reset --hard` oder `git checkout --` auf fremde Aenderungen ohne expliziten Wunsch.
- Docker/SSH/Fly Provider-Aktionen vortaeuschen, wenn Tool/Auth fehlt.

---

## 16. Stop-Regeln

Sofort stoppen und User konkret sagen, was er tun muss, wenn:

- SSH-Zugang fehlt.
- Fly Token fehlt oder kompromittiert ist.
- DNS nur in Provider-UI setzbar ist.
- Secret benoetigt wird.
- Testumgebung Python 3.14 statt 3.13 nutzt und Dependencies nicht bauen.
- Remote auf falsches Repo zeigt.

Aktueller Stop-Stand 2026-05-01:

```text
BLOCKER 1: root@204.168.230.127 erlaubt aktuellen SSH-Zugang nicht.
ACTION: Public Key aus deploy/hetzner_deploy_key.pub in /root/.ssh/authorized_keys eintragen.
STATUS: Befehle in Hetzner Web-Konsole eingegeben, Verifikation ausstehend.

BLOCKER 2: FLY_API_TOKEN fehlt und alter Token ist kompromittiert.
ACTION: Alten Fly Token loeschen, neuen erzeugen, als GitHub Secret FLY_API_TOKEN setzen.
STATUS: ✅ GELÖST — Neuer Org Deploy Token "carotis-ai-github-actions" erstellt und via gh secret set in DiggAiHH/CarotisAi gesetzt.

BLOCKER 3: flyctl fehlt lokal.
ACTION: Fly App/Cert entweder ueber GitHub Actions mit FLY_API_TOKEN oder nach Installation von flyctl ausfuehren.
STATUS: FLY_API_TOKEN vorhanden — GitHub Actions Deploy-Workflow kann jetzt laufen.

BLOCKER 4: INWX Hauptdomain zeigte auf Fly-CNAME und Fly lieferte 502.
ACTION: `carotis CNAME carotis-ai-frontend.fly.dev` wurde durch `carotis A 204.168.230.127 TTL 300` ersetzt.
STATUS: ✅ GELÖST — `carotis.diggai.de` und `api.carotis.diggai.de` zeigen auf Hetzner und liefern 200.
```

---

## 17. Bekannte Anomalien (Anomalien-Register)

Dauerhafte Bugs und Workspace-Quirks, die nicht Sessions-uebergreifend geloest werden koennen.

| ID | Anomalie | Schwere | Workaround | Fix-Target |
|----|----------|---------|------------|------------|
| A-01 | `&&` / `||` invalid in PowerShell | 🔴 hoch | `;` oder `if ($?)` verwenden | N/A (OS-Limitation) |
| A-02 | OneDrive-Pfade langsam | 🟡 mittel | Timeouts erhoehen (60s -> 120s) | N/A (OneDrive-Limitation) |
| A-03 | Python 3.14 bricht bei pydantic-core | 🔴 hoch | Python 3.13.12 via uv nutzen | Warten auf pydantic-core Wheels |
| A-04 | Vitest haengt sporadisch bei `--run` | 🟡 mittel | Timeout auf 120s oder einzeln laufen | jsdom + Cornerstone WASM |
| A-05 | Fly CLI (`flyctl`) fehlt lokal | 🟡 mittel | Deploy via GitHub Actions | Fly CLI installieren |
| A-06 | Hauptdomain-DNS zeigte auf Fly-CNAME mit 502 | ✅ FIXED | INWX: `carotis` von CNAME auf `A 204.168.230.127` gedreht | 2026-05-04 Run15 |
| A-07 | SSH-Zugriff auf Hetzner blockiert | ✅ FIXED | Key-ACL lokal repariert, SSH funktioniert | 2026-05-04 Run15 |
| A-08 | Frontend Build: Cornerstone3D WASM-Warnungen | 🟢 niedrig | Warnungen ignorieren, Build ist gruen | P3 (echtes C3D-Rendering) |
| A-09 | `rg` (ripgrep) Quotes in PowerShell | 🟢 niedrig | Einfache Quotes oder Escaping verwenden | N/A (Shell-Quirk) |
| A-10 | sklearn fehlt in venv (5 Tests failed) | ✅ FIXED | `pip install scikit-learn` + Import-Reihenfolge korrigiert | 2026-04-30 |
| A-11 | `decision_trees.case_id` UNIQUE constraint | 🟡 mittel | Unique case_ids pro Test | N/A (DB-Design) |
| A-12 | `vulnerability_markers` required 4 Keys | 🟡 mittel | Alle 4 Keys in Payload setzen | N/A (Schema-Design) |
| A-13 | FastAPI 0.115.5 + Starlette 1.0.0 incompatible | ✅ FIXED | FastAPI 0.115.5 → 0.136.1 | 2026-04-30 |
| A-14 | sklearn `_import_sklearn()` vertauschte Tupel | ✅ FIXED | `(LogisticRegression, IsotonicRegression)` statt `(Isotonic, Logistic)` | 2026-04-30 |
| A-15 | pytest.ini behandelt DeprecationWarning als Fehler | ✅ FIXED | `ignore::DeprecationWarning:fastapi` hinzugefuegt | 2026-04-30 |
| A-16 | `dependencies.py` dupliziert Auth-Code | ✅ FIXED | Re-export aus `security.py` | 2026-04-30 |
| A-17 | DicomViewer Memory Leak (createObjectURL) | ✅ FIXED | `objectUrlRef` + `URL.revokeObjectURL()` | 2026-04-30 |
| A-18 | Fragile `parents[4]` Pfad-Resolution | ✅ FIXED | `get_settings().project_root` | 2026-04-30 |
| A-19 | Claude Design Tweaks-Panel blockiert AI Panel | 🟢 niedrig | Toggle-Switch schliessen vor Screenshot | N/A (Design-Tool Verhalten) |
| A-20 | Cornerstone3D CJS-WASM Externalisierung | 🟢 niedrig | Vite-aliases + Lazy-Imports | P3 (echtes Rendering) |
| A-21 | AuthGate haengt ohne Backend in E2E | 🟡 mittel | `VITE_SKIP_AUTH=true` oder Backend starten | P1-Readiness |
| A-22 | Hetzner Web-Konsole Canvas-Terminal | 🟡 mittel | Befehle via browser_run_code_unsafe mit keyboard.type() | N/A |
| A-23 | INWX DNS-UI JavaScript-Modals | 🟡 mittel | Manuelle Eintraege oder INWX-API mit Token | N/A |

---

## 18. Session-Erkenntnisse — Harness The Whole Knowledge

### Deploy-Architektur P0f

- **Entscheidung alt**: Frontend Fly.io (`carotis.diggai.de`), Backend Hetzner (`api.carotis.diggai.de`).
- **Entscheidung aktuell**: Wegen Fly Trial/Billing 502 laeuft der P0f-Demo-Fallback komplett auf Hetzner. `api.carotis.diggai.de` und `carotis.diggai.de` sind online und zeigen auf denselben Server.
- **Konsequenz**: Caddy bedient beide Hostnames ueber `deploy/Caddyfile.backend`; Compose ist `deploy/hetzner-backend.compose.yml`; Serverpfad ist `/opt/carotis-ai/deploy`.
- **Status 2026-05-04**: Caddy laeuft healthy, `https://carotis.diggai.de/`, `https://api.carotis.diggai.de/` und `/health/` liefern 200. INWX-DNS ist finalisiert.

### 17-Step Optimization (S1-S17)

Alle 17 Schritte implementiert und getestet:

| Step | Was | Status | Datei |
|------|-----|--------|-------|
| S1 | CI-Pipeline | ✅ | `.github/workflows/ci.yml` |
| S2 | Deploy Health-Checks | ✅ | `.github/workflows/deploy-*.yml` |
| S3 | Typed API Errors | ✅ | `code/frontend/src/lib/apiError.ts` |
| S4 | Timeout+Retry | ✅ | `code/frontend/src/lib/apiClient.ts` |
| S5 | ErrorBoundary | ✅ | `code/frontend/src/components/ErrorBoundary.tsx` |
| S6 | Dynamic physicianRoleHash | ✅ | `code/backend/app/api/routes/demo.py` + Frontend Store |
| S7 | CORS List | ✅ | `code/backend/app/core/config.py` |
| S8 | Security Headers | ✅ | `code/backend/app/core/middleware.py` |
| S9 | Config Hardening | ✅ | `code/backend/app/core/config.py` |
| S10 | Metrics Auth | ✅ | `code/backend/app/main.py` |
| S11 | Graceful Shutdown | ✅ | `code/backend/app/services/inference_service.py` |
| S12 | Resource Limits | ✅ | `deploy/hetzner-backend.compose.yml` |
| S13 | Caddy Healthcheck | ✅ | `deploy/hetzner-backend.compose.yml` |
| S14 | Gzip Compression | ✅ | `code/backend/app/main.py` |
| S15 | E2E Stresstest | ✅ | `tests/test_rohde_walkthrough_e2e.py` (7/7 passing) |
| S16 | Bundle Analysis | ✅ | `code/frontend/package.json` + `npm run analyze` |
| S17 | Pre-Deploy Checklist | ✅ | `deploy/PRE_DEPLOY_CHECKLIST.md` |

### Secrets-Management

- **Regel**: Kein Secret jemals in Chat oder Datei. GitHub Secrets sind die einzige erlaubte Persistenz.
- **Lektion**: Ein GitHub-PAT war im Remote-URL eingebettet. Ein Fly-Token wurde im Chat gepostet. Beide mussten rotiert werden.
- **Praxis**: `rg` Secret-Scan vor jedem Push.

### Windows-PowerShell-Realitaet

- **Lektion**: `&&`/`||` funktionieren nicht. OneDrive ist langsam. Python 3.14 ist noch nicht produktionsreif.
- **Praxis**: Jeder Shell-Befehl muss PowerShell-kompatibel sein. Timeout immer mind. 60s, bei npm/docker 120s.

### Test-Verifikation als Gate

- **Lektion**: `DEBUG=true` ist fuer pytest Pflicht, sonst scheitern Config-Tests.
- **Ergebnis**: 105 passed, 11 skipped, 0 failed (Backend). 12 passed (Frontend). Diese Baselines duerfen nicht regredieren.
- **Neu**: pytest.ini muss `ignore::DeprecationWarning:fastapi` enthalten fuer FastAPI 0.136.1 + Starlette 1.0.0.

### MCP-Trio + Erweiterungen

- **Entscheidung**: 4 dedizierte MCP-Server (Obsidian, Graphify, Hermes, Browser) + 1 Combined-Server.
- **Begruendung**: Separation of Concerns, modulare Wartung, graceful degradation.
- **Status**: B1-B5 implementiert, 16/16 Tests PASS, in CI integriert.
- **Setup**: `pip install -r code/mcp_servers/requirements.txt`, `playwright install chromium`.

### Code-Penetrationstest-Lektionen

- **Unused Imports**: `ruff check backend/app --select F` findet F401 (unused imports).
- **Memory Leaks**: `URL.createObjectURL()` ohne `URL.revokeObjectURL()` = Leak. Immer ref + cleanup.
- **Fragile Pfade**: `Path(__file__).parents[N]` bricht bei Refactoring. `get_settings().project_root` ist robust.
- **Auth-Konsistenz**: `dependencies.py` sollte nicht Auth-Code duplizieren. Re-export aus `security.py`.
- **TypeScript**: `npm run typecheck` vor jedem Commit. 0 Errors ist das Ziel.

### FastAPI/Starlette Kompatibilitaet

- **Lektion**: FastAPI 0.115.5 ist nicht kompatibel mit Starlette 1.0.0.
- **Fix**: `pip install "fastapi>=0.115.8"` (wurde auf 0.136.1 aktualisiert).
- **Hinweis**: Starlette 1.0.0 entfernte `on_startup` aus `Router.__init__()`. FastAPI 0.115.5 uebergibt es noch.

### Claude Design Verifier-Agent

- **Lektion**: Claude Design hat einen internen Verifier-Agenten, der nach jeder Generation automatisch laeuft. Er faengt Runtime-Errors (React Hooks, Destructuring) und fixt sie ohne User-Prompt.
- **Beispiel**: `const { showAnnotations } = useTweaks()` wurde als falsch erkannt und auto-korrigiert.
- **Praxis**: Nicht sofort neu generieren bei kleinen Bugs — erst auf Verifier-Ausgabe warten.

### Frontend Blank-Screen Prevention

- **Lektion**: Cornerstone3D + vtk.js CJS-Default-Imports verursachen Runtime-Crash beim App-Start.
- **Fix**: Lazy-Imports fuer Cornerstone-Komponenten + Vite-Aliases fuer `globalthis`, `fast-deep-equal`, `seedrandom` + lokale Shims.
- **Ergebnis**: Kein Blank Screen mehr; Token-Gate und App-Inhalt rendern zuverlaessig.

### Playwright ESM-Kompatibilitaet

- **Lektion**: `require("fs")` funktioniert nicht in Playwrights ESM-Test-Kontext.
- **Fix**: Screenshots via `testInfo.attach()` (nativ) statt `fs.writeFileSync()`.

### AuthGate E2E Strategy

- **Lektion**: AuthGate validiert Token gegen Backend-API. Ohne Backend haengt der E2E-Test am Gate.
- **Workarounds**: (1) Backend im Hintergrund starten, (2) `VITE_SKIP_AUTH=true` fuer CI-E2E, (3) Mock-Service-Worker.

### Modell-Routing-Effizienz

- **Lektion**: Kimi K2.6 ist exzellent fuer Bulk-Prompts mit klaren Datei-Grenzen. Codex ist exzellent fuer Python-Implementierung. Opus 4.7 ist exzellent fuer Architektur-Entscheidungen. Copilot/Sonnet 4.6 ist exzellent fuer UI-Prototyping und Browser-Harness.
- **Praxis**: Niemals denselben Stack von zwei Modellen gleichzeitig bearbeiten lassen ohne disjunkte Ownership.

### Local-First als nicht-verhandelbare Constraint

- **Lektion**: Jede Architektur-Entscheidung wird zuerst durch das Local-First-Prisma gefiltert.
- **Konsequenz**: Kein Cloud-API fuer Patientendaten, keine externe Inference, SQLite-only.
- **Praxis**: Wenn ein Tool/Service Cloud-Anforderungen hat, wird er abgelehnt oder lokal gehostet (Ollama, Hermes).

---

*Version: 2026-05-01 v6 — Harness The Whole Knowledge + Design Bridge*
*Letztes Update: Claude Design Harness + Playwright E2E Patterns + Blank-Screen Prevention + Anomalien A-19..A-21*
*Gueltig bis: Naechste Major-Session*
