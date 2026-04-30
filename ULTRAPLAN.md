# ULTRAPLAN - Carotis-AI Agent Pre-Flight Protocol

Version: 2026-04-30  
Scope: verbindliches Co-Working-Protokoll fuer Codex, Copilot, Kimi, Claude/Opus/Sonnet/Haiku und lokale Agenten im Carotis-AI Workspace.

Dieses Dokument ist der Startpunkt fuer neue Agents. Es fasst zusammen, was in dieser Session praktisch funktioniert hat, was auf diesem Rechner kaputt ist, welche Tools wann genutzt werden und wo Agents stoppen muessen.

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
- Aktive Deploy-Architektur: Frontend Fly.io, Backend Hetzner.
- Netlify/Render sind fuer P0f nicht mehr Ziel.

## 2. Hard Pre-Flight

Vor jeder Arbeit:

1. `CLAUDE.md` lesen.
2. `AGENTS.md` lesen.
3. `MEMORY.md` lesen.
4. Letzte 3 Run-Logs lesen:

```powershell
Get-ChildItem memory\runs -File | Sort-Object LastWriteTime -Descending | Select-Object -First 3 Name
```

5. Bei Code-Arbeit bekannte Anomalien lesen:

```powershell
Get-ChildItem memory\anomalies -File
```

6. Git pruefen:

```powershell
git status --short --branch
git remote -v
```

7. Secrets scannen, bevor gepusht wird:

```powershell
rg -n "FlyV1|fm2_|github_pat_|BEGIN OPENSSH PRIVATE KEY|BEGIN RSA PRIVATE KEY|API_TOKEN=.*[A-Za-z0-9_-]{20,}" -g '!data/**' -g '!**/.git/**' -g '!**/node_modules/**' .
```

## 3. Memory-Disziplin

Kein Prompt endet ohne 5-Zeilen-Run-Log.

Pfad-Konvention:

```text
memory/runs/YYYY-MM-DD_<Agentname>_<Model>-RunNN_<thema>.md
```

Beispiele:

```text
memory/runs/2026-04-30_Codex_GPT55-Run03_clean_repo_handoff.md
memory/runs/2026-04-30_Kimi_K26-Run01_frontend_fly.md
memory/runs/2026-04-30_Copilot_Sonnet46-Run02_p0f_fix.md
```

Minimalformat:

```markdown
---
name: YYYY-MM-DD_Agent_Model-RunNN_topic
type: run
---
## Goal
## Done
## Surprised by
## Avoided
## Next
```

Wenn die Session ein neues dauerhaftes Artefakt erzeugt, danach Pointer in `MEMORY.md` setzen.

## 4. Tool-Matrix Fuer Codex In Diesem Workspace

### Shell

Nutzen fuer:

- `git`, `gh`, `docker`, `npm`, `pytest`, `ssh`
- Datei-Listing und schnelle Reads
- Secret-Setzen via `gh secret set`

Regeln:

- PowerShell ist die Default-Shell.
- Keine Bash-Operatoren `&&` / `||` verwenden.
- Keine destruktiven Befehle ohne Pfadpruefung.
- Bei OneDrive-Pfaden Timeouts hoeher setzen.
- Fuer parallele Shell-Reads `multi_tool_use.parallel` verwenden.

### apply_patch

Nutzen fuer:

- Manuelle Datei-Edits.
- Neue Markdown-/YAML-/Python-/TS-Dateien.
- Kleine gezielte Aenderungen.

Nicht nutzen fuer:

- Formatierung ganzer Codebaeume.
- Generated build output.
- Secrets.

### GitHub CLI `gh`

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

### Docker

Installiert:

```text
C:\Program Files\Docker\Docker\resources\bin\docker.exe
```

Nutzen fuer:

- Demo-Compose-Validierung.
- Lokalen Smoke-Test, wenn Docker Desktop laeuft.

### SSH

Installiert:

```text
C:\Windows\System32\OpenSSH\ssh.exe
```

Status 2026-04-30:

- Deploy-Key wurde lokal erzeugt:

```text
deploy/hetzner_deploy_key
deploy/hetzner_deploy_key.pub
```

- `HETZNER_SSH_PRIVATE_KEY` wurde in GitHub Secrets gesetzt.
- Direkter SSH-Zugriff von diesem Rechner auf `root@204.168.230.127` schlug fehl:

```text
Permission denied (publickey,password)
```

Stop-Regel:

- Agent darf nicht raten.
- Lou muss den Public Key auf dem Server in `~/.ssh/authorized_keys` eintragen oder SSH-Zugang bereitstellen.

### Fly.io

Status 2026-04-30:

- `flyctl` / `fly` ist auf diesem Rechner nicht installiert.
- Der im Chat gepostete Fly-Token gilt als kompromittiert.

Stop-Regel:

- Alten Fly-Token in Fly.io loeschen.
- Neuen Token erzeugen.
- Token direkt in GitHub Secret `FLY_API_TOKEN` setzen.
- Token nie wieder in Chat oder Dateien posten.

### Web / Browser / Provider-Konsolen

Agents duerfen oeffentliche Doku recherchieren. Provider-Aktionen wie Fly Token, INWX DNS oder Hetzner Console brauchen authentifizierte Session und duerfen nur ausgefuehrt werden, wenn der User klar `go` sagt und das Tool verfuegbar ist.

## 5. Aktuelle Secrets

Gesetzt in GitHub Repo `DiggAiHH/CarotisAi`:

```text
ACME_EMAIL
ADMIN_API_KEY
API_KEY
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

## 6. Deploy-Architektur P0f

Frontend:

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
carotis         CNAME  carotis-ai-frontend.fly.dev
```

Falls Fly andere Records fordert, nach erstem Fly-App-Setup:

```powershell
fly certs show carotis.diggai.de --config deploy/fly.frontend.toml
```

## 7. Python Auf Diesem Rechner

Verfuegbar:

```text
Python 3.14 system default
Python 3.13.12 via uv path:
C:\Users\tubbeTEC\AppData\Roaming\uv\python\cpython-3.13.12-windows-x86_64-none\python.exe
```

Wichtig:

- Backend `.venv` war Python 3.14 und brach bei `pydantic-core==2.27.1`.
- Fuer Backend-Tests funktioniert Python 3.13.12.
- Temp-venv `.venv313` wurde erfolgreich genutzt und danach entfernt.
- Wenn neu gebraucht:

```powershell
cd "c:\Users\tubbeTEC\OneDrive\z\Documents\Claude\Projects\Carotis AI\code"
& "C:\Users\tubbeTEC\AppData\Roaming\uv\python\cpython-3.13.12-windows-x86_64-none\python.exe" -m venv .venv313
& .\.venv313\Scripts\python.exe -m pip install -r backend\requirements.txt
```

Test mit sauberem `DEBUG`:

```powershell
$env:DEBUG="true"
& .\.venv313\Scripts\python.exe -m pytest tests -p no:warnings
```

Bekanntes Ergebnis:

```text
107 passed, 2 skipped
```

Ohne `DEBUG=true` koennen Config-Tests scheitern, wenn die Shell `DEBUG=release` geerbt hat.

## 8. Frontend Verifikation

Pfad:

```powershell
cd "code\frontend"
```

Kommandos:

```powershell
npm run typecheck
npm test -- --run
npm run lint
npm run build
```

Bekannte Ergebnisse:

- Typecheck: gruen.
- Vitest: 12 passed.
- Lint: gruen.
- Build: gruen, aber Vite/Cornerstone WASM-Warnungen und grosse Chunks sind bekannt.

Warnungen nicht reflexiv fixen, wenn sie aus Cornerstone/WASM kommen und Build erfolgreich ist.

## 9. Backend Verifikation

Pfad:

```powershell
cd "code"
```

Kommandos:

```powershell
$env:DEBUG="true"
& .\.venv313\Scripts\python.exe -m pytest tests -p no:warnings
& .\.venv313\Scripts\python.exe -m ruff check backend\app tests
& .\.venv313\Scripts\python.exe -m black --check backend\app tests
```

Wenn `pytest` ohne Einschränkung auch `ml/` sammelt, koennen fehlende ML-Extras blockieren:

```text
monai
timm
mlflow
```

Dann fuer Backend-Arbeit gezielt `pytest tests` nutzen.

## 10. Modellrouting

| Aufgabe | Modell / Agent |
|---|---|
| Architektur, ADR, regulatorische Texte | Opus 4.7 |
| Code-Implementierung, Debugging | Codex GPT-5.5 / Sonnet 4.6 |
| Atomare Edits, Run-Logs, i18n | Haiku 4.5 |
| Bulk-Prompts mit klaren Dateien | Kimi K2.6 |
| PR-Review und Regression-Risiko | Codex / Sonnet |

Subagenten:

- Nur wenn der User explizit parallele Agenten/Subagenten will.
- Disjunkte Datei-Ownership definieren.
- Nicht denselben Stack doppelt bearbeiten lassen.
- Danach Integrationsrunde lokal.

## 11. Skills Und Connectors

Verfuegbare Skills in dieser Umgebung:

- `vercel-react-best-practices`: React/Next Performance und Pattern.
- `vercel-composition-patterns`: Komponentenarchitektur.
- `web-design-guidelines`: UI/UX/A11y Review.
- `openai-docs`: nur fuer OpenAI API/Produktfragen.
- `skill-creator`, `skill-installer`, `plugin-creator`: nur bei Skill/Plugin-Aufgaben.
- `microsoft-foundry/*`: nur Azure Foundry Aufgaben.
- `imagegen`: nur fuer Bildassets, nicht fuer Code.

Nutzung:

- Skill nur einsetzen, wenn Aufgabe klar passt oder User ihn nennt.
- `SKILL.md` lesen, nicht blind aus Beschreibung handeln.
- Keine Connector-/Provider-Aktion mit Patientendaten.

## 12. Verbote

Niemals:

- Patientendaten in Cloud, Chat, Browser, GitHub, Fly, Hetzner-Logs oder externe APIs.
- Secrets in Dateien, Chat oder Remote-URLs.
- Direkt nach `master` pushen, wenn Branch-Schutz/PR gefordert ist.
- Office-Dokumente direkt editieren, wenn Stride-Prompt gefordert ist.
- `git reset --hard` oder `git checkout --` auf fremde Aenderungen ohne expliziten Wunsch.
- Docker/SSH/Fly Provider-Aktionen vortaeuschen, wenn Tool/Auth fehlt.

## 13. Stop-Regeln

Sofort stoppen und User konkret sagen, was er tun muss, wenn:

- SSH-Zugang fehlt.
- Fly Token fehlt oder kompromittiert ist.
- DNS nur in Provider-UI setzbar ist.
- Secret benoetigt wird.
- Testumgebung Python 3.14 statt 3.13 nutzt und Dependencies nicht bauen.
- Remote auf falsches Repo zeigt.

Aktueller Stop-Stand 2026-04-30:

```text
BLOCKER 1: root@204.168.230.127 erlaubt aktuellen SSH-Zugang nicht.
ACTION: Public Key aus deploy/hetzner_deploy_key.pub in /root/.ssh/authorized_keys eintragen.

BLOCKER 2: FLY_API_TOKEN fehlt und alter Token ist kompromittiert.
ACTION: Alten Fly Token loeschen, neuen erzeugen, als GitHub Secret FLY_API_TOKEN setzen.

BLOCKER 3: flyctl fehlt lokal.
ACTION: Fly App/Cert entweder ueber GitHub Actions mit FLY_API_TOKEN oder nach Installation von flyctl ausfuehren.
```

