# Browser-Harness Input fuer Carotis-AI

## Zweck

Operative Eingabedatei fuer den frisch installierten `browser-harness` Skill im Carotis-AI Workspace. Ziel ist reproduzierbare Browser-Verifikation fuer Demo, Claude Design, Deploy-UIs und Screenshot-Artefakte ohne Patientendaten, ohne Secrets und ohne echte Provider-Aenderungen.

## Konkrete Aufgaben

| Nr. | Aufgabe | Status | Ergebnis / Artefakt |
| --- | --- | --- | --- |
| 1 | Demo-Smoke lokal gegen `http://localhost:3000` mit neuem Tab, Load-Wait und Screenshot. | executed-as-plan | Sichtbarer App- oder AuthGate-Zustand als `artifacts/browser/demo_smoke_desktop.png`; keine echten Patientendaten. |
| 2 | Auth-Gate pruefen: Token-Feld, Submit-Button, Fehlerzustand bei fehlendem Backend, kein Tokenwert loggen. | executed-as-plan | AuthGate-Screenshot plus Kurznotiz: `Server nicht erreichbar` ist erwartetes Ergebnis ohne Backend. |
| 3 | Responsive Viewports fuer Desktop `1280x720` und Mobile `375x667` aufnehmen. | executed-as-plan | Zwei Screenshots mit Layout-Vergleich; mobile Ansicht darf keine ueberlappenden Panels zeigen. |
| 4 | Claude Design Prototype oeffnen und Generation-Complete-Signale pruefen. | executed-as-plan | Screenshot nach File-Tab/Verifier-Signal; Tweaks-Panel vor AI-Panel-Screenshot schliessen. |
| 5 | Claude Design iframe-Interaktion verifizieren: Patients, Viewer und AI Tabs sichtbar durchklicken. | executed-as-plan | Drei Zustands-Screenshots; Ergebnis in Run-Log als UI-Smoke referenzierbar. |
| 6 | Fly.io UI read-only pruefen: App-/Release-/Domain-Seiten nur anzeigen, keine Token erstellen, keine Deploy-Aktion. | executed-as-plan | Screenshot der sichtbaren App-/Domain-Konfiguration; Stop bei Login-Wall oder Token-Dialog. |
| 7 | Hetzner Console read-only pruefen: Server-Uebersicht oder Konsole nur sichtbar machen, keine Befehle tippen. | executed-as-plan | Screenshot der Server-Uebersicht; Canvas-Terminal nur mit explizitem Human-Go bedienen. |
| 8 | INWX DNS read-only pruefen: Domainliste und Nameserver/DNS-Tab anzeigen, keine Records speichern. | executed-as-plan | Screenshot der vorhandenen DNS-Ansicht; fehlende `carotis`/`api.carotis` Records als manuelle Aktion notieren. |
| 9 | Screenshot-Harvest fuer Rohde-Demo: Startzustand, Viewer, Grad-CAM, AI Panel, Decision Capture. | executed-as-plan | Kuratiertes Screenshot-Set fuer Briefing/Runbook; alle Daten synthetisch oder Demo-only. |
| 10 | Domain-Skill-Capture: wiederverwendbare URL-Muster, Waits, UI-Traps und stabile Selektoren dokumentieren. | executed-as-plan | Durable Notes fuer `memory/domain/` oder spaeter `agent-workspace/domain-skills/`; keine Cookies, Secrets oder user-spezifischen States. |

## Preflight-Integration

- `browser-harness` nutzen, wenn ein sichtbarer Browserzustand, Screenshot, iframe, Provider-UI oder Claude-Design-Prototyp geprueft werden muss.
- Vor jeder Nutzung erst lokale Memorys und aktuelle Run-Logs lesen, dann mit `new_tab(url)` starten; nicht die aktive User-Registerkarte mit `goto_url()` ueberschreiben.
- Nach jeder bedeutenden UI-Aktion einen Screenshot oder `page_info()` zur Verifikation erzeugen; sichtbare Fehlerzustaende faktisch notieren.
- Stoppen, sobald Login-Daten, 2FA, Secrets, Tokenwerte, Patientendaten, echte DNS-/Deploy-/Billing-Aktionen oder unklare Provider-Modals auftauchen.
- Erkenntnisse nur als langlebige Muster dokumentieren: URL-Pattern, Wait-Grund, UI-Trap, stabile Labels; keine Run-Narration und keine privaten Session-Daten.

## Anti-Patterns

- Provider-UIs automatisiert veraendern, wenn die Aufgabe nur Read-only-Verifikation erlaubt.
- Credentials aus Screenshots abtippen, Token auslesen oder Login-Walls umgehen.
- Patientendaten, echte DICOMs oder nicht anonymisierte medizinische Inhalte in externe Seiten laden.
- Blind auf Selektoren vertrauen, obwohl Screenshot/iframe/Shadow-DOM den echten Zustand schneller und robuster zeigt.
- Pixelkoordinaten als Domain-Wissen speichern; stattdessen Ziel ueber sichtbaren Text, Rolle, Label oder URL-Muster beschreiben.

## Sichere Beispielcommands

```bash
browser-harness -c '
new_tab("http://localhost:3000")
wait_for_load()
print(page_info())
capture_screenshot("artifacts/browser/demo_smoke_desktop.png")
'

browser-harness -c '
new_tab("http://localhost:3000")
set_viewport_size(375, 667)
wait_for_load()
capture_screenshot("artifacts/browser/demo_smoke_mobile.png")
'

browser-harness -c '
new_tab("https://claude.ai/design/p/019de4bf-5dbc-7c47-b1fe-8a0466e64c9c?file=Carotis+AI.html")
wait_for_load()
print(page_info())
# Stop if redirected to login. Do not type credentials.
'

browser-harness -c '
new_tab("https://example.com")
wait_for_load()
capture_screenshot("artifacts/browser/read_only_check.png")
# Use provider URLs only for read-only checks; never save forms or create tokens.
'
```
