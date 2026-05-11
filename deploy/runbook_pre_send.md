# Pre-Send Smoke Runbook - Rohde Demo

> Zweck: letzte technische Pruefung, bevor Aroob die Rohde-Mail mit Live-Demo-Link versendet. Keine echten Patientendaten verwenden.

## 1. Repo- und Secret-Hygiene

- [ ] `git status --short --branch` geprueft; keine unerwarteten fremden Aenderungen.
- [ ] `git remote -v` zeigt `https://github.com/DiggAiHH/CarotisAi.git` ohne Token.
- [ ] Secret-Scan ausgefuehrt:

```powershell
Select-String -Path * -Pattern "FlyV1|fm2_|github_pat_|BEGIN OPENSSH PRIVATE KEY|BEGIN RSA PRIVATE KEY|API_TOKEN=.*[A-Za-z0-9_-]{20,}" -CaseSensitive -SimpleMatch:$false
```

- [ ] Autopilot-Preflight lokal ausgefuehrt:

```powershell
powershell -ExecutionPolicy Bypass -File deploy/autopilot_preflight.ps1 -AllowDirtyWorktree -SkipSecrets
```

## 2. Lokale Backend-Pruefung

- [ ] Backend-Testumgebung gesetzt:

```powershell
cd code
$env:PYTHONPATH="backend"
$env:DEBUG="true"
$env:API_KEY="aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
$env:ADMIN_API_KEY="bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"
$env:ANONYMIZATION_SALT="ssssssssssssssss"
```

- [ ] Rohde-E2E-Test gruen:

```powershell
$PY = if (Test-Path ".\.venv\Scripts\python.exe") { ".\.venv\Scripts\python.exe" } else { ".\.venv313\Scripts\python.exe" }
& $PY -m pytest tests\test_rohde_walkthrough_e2e.py -v --tb=short -p no:warnings
```

- [ ] Smoke-Test gruen:

```powershell
$PY = if (Test-Path ".\.venv\Scripts\python.exe") { ".\.venv\Scripts\python.exe" } else { ".\.venv313\Scripts\python.exe" }
& $PY -m pytest tests\test_smoke.py -v --tb=short -p no:warnings
```

## 3. Frontend-Pruefung

- [ ] Typecheck gruen:

```powershell
cd code\frontend
npm run typecheck
```

- [ ] Lint gruen:

```powershell
npm run lint
```

- [ ] Build gruen; bekannte Cornerstone/WASM-Warnungen sind akzeptiert:

```powershell
npm run build
```

## 4. Demo-Artefakte

- [ ] `Stride V2/KI_Tools_Marktanalyse_v2.pdf` vorhanden.
- [ ] `Stride V2/Carotis_AI_Konzept_v2.docx` vorhanden.
- [ ] `Stride V2/Expose_Carotis_AI_Rohde_v2.docx` vorhanden.
- [ ] `Stride V2/Tech_Description_Klinikum_v2.docx` vorhanden.
- [ ] `Stride V2/Value_Proposition_Klinikum_v2.docx` vorhanden.
- [ ] `Stride V2/Anschreiben_Aroob_an_Rohde_v2.docx` vorhanden.
- [ ] `Stride V3/Anschreiben_Aroob_an_Rohde_v3_PROMPT.md` vorhanden.
- [ ] `outputs/Rohde_Video_Script_v1.md` vorhanden.
- [ ] `outputs/Aroob_Status_Briefing_v1.md` vorhanden.

## 5. Deploy-Blocker

- [ ] `FLY_API_TOKEN` als GitHub Secret gesetzt.
- [ ] Hetzner Public Key aus `deploy/hetzner_deploy_key.pub` in `/root/.ssh/authorized_keys` eingetragen.
- [ ] INWX DNS gesetzt:
  - `api.carotis` A `204.168.230.127`
  - `carotis` CNAME zur Fly-App
- [ ] Fly-App `carotis-ai-frontend` existiert und Custom Domain ist aktiv.

## 6. Live-Smoke Nach Deploy

- [ ] `curl.exe -k -I "https://api.carotis.diggai.de/health/"` zeigt **nicht** `Server: Netlify`.
- [ ] `curl.exe -k -I "https://api.carotis.diggai.de/health/"` liefert `200` oder erwartetes Backend-JSON.
- [ ] `curl.exe -k -I "https://carotis.diggai.de/"` liefert `200` und nicht `404`.
- [ ] Demo-Token funktioniert im Auth-Gate.
- [ ] Walkthrough startet mit `?tour=1`.
- [ ] Synthetischer DICOM-Upload liefert AI-Resultat oder eine klar erklaerte Demo-Fallback-Meldung.
- [ ] Decision-Tree-Capture speichert ohne PII.
- [ ] Audit-Trail zeigt Inferenz + Decision-Tree-Event.

### Aktueller Befund (2026-05-01)

- `api.carotis.diggai.de` zeigt derzeit auf `75.2.60.5` statt `204.168.230.127`.
- `carotis.diggai.de` und `www.carotis.diggai.de` liefern aktuell `404` mit `Server: Netlify`.
- Kritischer Pfad bleibt: DNS korrekt setzen + Fly/Hetzner Zielrouting validieren.

## 7. Mail-Freigabe

- [ ] Aroob hat v2/v3 Text gelesen.
- [ ] Keine echten Patientendaten in Anlagen.
- [ ] Token nicht in Run-Logs, Chat oder Git gespeichert.
- [ ] Kalender-Reminder fuer Follow-up in 14 Tagen gesetzt.
