---
name: skill_harness_obsidian_2026-05-02
description: Operative Harness-Inputs fuer den frisch installierten obsidian-Skill im Carotis-AI Workspace.
type: skill_harness
skill: obsidian
last_updated: 2026-05-02
phase: P0f
---

# Obsidian Skill Harness Input - Carotis-AI

## Zweck

Operative Eingabe fuer den `obsidian`-Skill im Carotis-AI Workspace. Ziel: lokale Markdown-Notizen, Run-Logs, P0f-Status und Backlinks diszipliniert lesbar halten, ohne Patientendaten, Secrets oder externe Cloud-Sync-Pfade zu beruehren. Der Skill darf fuer Lesen, Suchen, Wikilinks und vorbereitete Notiz-Artefakte genutzt werden; echte Vault-Schreibaktionen nur nach expliziter Freigabe.

## Aufgaben

| # | Aufgabe | Status | Ergebnis / Artefakt |
|---|---|---|---|
| 1 | Vault-Pfad vor Nutzung feststellen und quoted behandeln. | `executed-as-plan` | Artefakt: `OBSIDIAN_VAULT_PATH` oder Default-Pfad dokumentiert, keine Aktion gegen ungepruefte Pfade. |
| 2 | Vault-Sync fuer Carotis-Notizen planen, nicht blind ausfuehren. | `executed-as-plan` | Artefakt: Sync-Plan `source -> target -> backlinks -> no-patient-data-check`. |
| 3 | Neue Run-Logs mit Projektstatus verlinken. | `executed-as-plan` | Artefakt: Run-Log enthaelt Wikilinks zu `[[project_status_p0]]`, `[[ULTRAPLAN]]`, relevanter Task-ID. |
| 4 | P0f-Notizen konsolidieren. | `executed-as-plan` | Artefakt: kurze P0f-Indexnotiz mit Deploy-Blockern, Rohde-Paket, Mail-Status und naechster Human-Action. |
| 5 | Rohde-Kontext per Backlinks auffindbar machen. | `executed-as-plan` | Artefakt: Backlinks von Rohde-Notizen zu `[[06_ROHDE_MEETING_KIT]]`, `[[deploy/runbook_pre_send]]`, `[[project_status_p0]]`. |
| 6 | Deploy-Kontext per Backlinks auffindbar machen. | `executed-as-plan` | Artefakt: Deploy-Notiz verlinkt `[[deploy/PRE_DEPLOY_CHECKLIST]]`, `[[deploy/runbook_pre_send]]`, `[[ULTRAPLAN]]`. |
| 7 | Anomalien- und Regression-Kontext verlinken. | `executed-as-plan` | Artefakt: Bug-/Triage-Notiz verlinkt `[[memory/anomalies/README]]` und konkrete Anomalie-Dateien. |
| 8 | Search-Disziplin erzwingen, bevor Notizen neu erstellt werden. | `executed-as-plan` | Artefakt: Suchprotokoll mit `rg` im Repo plus Obsidian-Search im Vault, Treffer kurz bewertet. |
| 9 | Wikilinks gegen Dateinamen und Note-Titel pruefen. | `executed-as-plan` | Artefakt: keine orphan links fuer zentrale Knoten wie Rohde, Deploy, P0f, Anomalien, Run-Logs. |
| 10 | Sicherheitscheck vor jeder Vault-Notiz anwenden. | `executed-as-plan` | Artefakt: Notiz enthaelt nur synthetische Demo-Fakten, Projektstatus und Links; keine DICOM-Rohdaten, keine IDs, keine Token. |

## Preflight-Integration

- Vor Obsidian-Nutzung zuerst `ULTRAPLAN.md`, `CLAUDE.md`, `MEMORY.md`, letzte 3 Run-Logs und `memory/anomalies/` lesen.
- Zuerst im Projekt mit `rg` suchen; Obsidian-Search erst danach nutzen, damit bestehende Workspace-Artefakte Vorrang haben.
- Jeden neuen Note-Entwurf mit mindestens einem Backlink zu Status, Run-Log oder Task versehen.
- Vault-Pfade immer quoten und externe Vault-Schreibaktionen nur nach ausdruecklicher User-Freigabe ausfuehren.
- Vor Sync oder Write explizit pruefen: keine Patientendaten, keine Secrets, keine Roh-DICOM-Inhalte, keine privaten Tokenwerte.

## Anti-Patterns

- Nicht in einen externen Obsidian-Vault schreiben, wenn der Auftrag nur eine Projektdatei erlaubt.
- Keine Notizen ohne Backlinks erzeugen; orphan notes verlieren den Harness-Wert.
- Keine Patientendaten, private Fall-IDs, Roh-DICOM-Auszuge, Token oder Secret-Namen mit Werten in den Vault uebernehmen.
- Keine neue P0f-Notiz anlegen, bevor `rg` und Vault-Search nach Rohde, Deploy, P0f, Anomalien und Task-ID gelaufen sind.
- Keine breiten Syncs ueber `node_modules`, `.git`, `data/`, Screenshots oder generierte Reports.

## Beispiel-Wikilinks

```markdown
## Rohde P0f Handoff

Status: [[project_status_p0]]
Meeting-Kontext: [[06_ROHDE_MEETING_KIT]]
Pre-Send Runbook: [[deploy/runbook_pre_send]]
Deploy-Checkliste: [[deploy/PRE_DEPLOY_CHECKLIST]]
Anomalien-Index: [[memory/anomalies/README]]
Letzter Skill-Install-Run: [[memory/runs/2026-05-02_Codex_GPT55-Run08_skill_sources]]

Notiz:
- P0f bleibt aktiv, bis Demo-Link und Rohde-Mail durch Lou/Aroob freigegeben sind.
- Nur synthetische Demo-Daten referenzieren.
- Keine Secrets oder Patientendaten in diese Notiz kopieren.
```
