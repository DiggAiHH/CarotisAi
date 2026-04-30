# RUNBOOK_TODAY — Was Lou jetzt tut

> Diese Datei ist die **Schritt-für-Schritt-Anleitung für die nächsten 90 Minuten**. Wenn du den Workspace zum ersten Mal aufmachst und nicht weißt, wo anfangen: hier.

---

## Ziel von heute

Acht Office-Dokumente auf das Klinikum-Dortmund-Setting umgestellt + Aroob hat sie reviewed + die Mail an Prof. Rohde liegt versandbereit. Kein Code, keine Repos, keine ML-Modelle. Nur das Stakeholder-Paket.

**Wann fertig?** Wenn `tasks.jsonl` Tasks T-001 bis T-009 alle auf `done` stehen. Erwartung: 90–120 Min konzentrierte Arbeit + Aroob-Review-Zeit.

---

## Voraussetzungen

- [x] `Carotis AI/` Workspace ist offen (du liest gerade aus dem)
- [ ] Microsoft 365 Copilot / Office Agent / Stride ist verfügbar (du hast die Konten)
- [ ] Aroob ist erreichbar (Telefon / Slack / WhatsApp) für den Review-Schritt
- [ ] Du hast 60–90 Min am Stück Zeit, ungestört

---

## Die 10 Schritte

### Schritt 1 — Pre-Flight (5 Min)

```powershell
# In PowerShell, im Carotis AI Workspace:
cd "C:\Users\tubbeTEC\OneDrive\z\Documents\Claude\Projects\Carotis AI"
type CLAUDE.md
type MEMORY.md
Get-ChildItem memory\runs\ | Sort-Object LastWriteTime -Descending | Select-Object -First 3
```

oder bequemer:

```powershell
.\scripts\preflight.ps1
```

**Check:** Ist `memory/runs/2026-04-27_opus47_harness_v1.md` da? Ja → weiter. Nein → schreib mir das in einer Cowork-Session.

### Schritt 2 — Stride / Office Agent öffnen (2 Min)

Microsoft 365 → Copilot → Stride. Workspace „Carotis AI" anlegen oder den existierenden öffnen. Diese 7 Files dort hochladen:

1. `Anschreiben_Dr_Alrawashdeh_KI_Carotis_Diagnostik.docx`
2. `Ki_Carotis_Expose.docx`
3. `Ki_Carotis_Diagnostik.docx`
4. `Value_Proposition_Ki_Carotis.docx`
5. `Carotis_Ai.pptx`
6. `Ki_Tools_Marktanalyse.docx`
7. `Carotis_Ai_Konzept.docx`

Plus den Master-Plan + Decision-Tree-Spec als Kontext-Beilage:
- `04_MASTER_PLAN.md`
- `05_DECISION_TREE_HARVESTING.md`

### Schritt 3 — Globalen Kontext in Stride einfügen (1 Min)

Datei `07_OFFICE_AGENT_PROMPTS.md` öffnen. Sektion **„Globaler Kontext"** komplett kopieren und in Stride als erste Nachricht einfügen.

### Schritt 4 — Prompt G durchziehen (Floy-Recherche v2) — 10 Min

`07_OFFICE_AGENT_PROMPTS.md` → Sektion „PROMPT G". Komplett kopieren, in Stride einfügen, ausführen.

Output-Datei: `KI_Tools_Marktanalyse_v2.docx` — speichern im Workspace.

**Verify:** Datei existiert. Öffne sie kurz, scrolle zur neuen Gap-Analyse-Sektion, prüfe: Tabelle Floy vs Carotis-AI ist da, „Klinikum Dortmund" mind. 1× erwähnt, „Decision-Tree-Harvesting" mind. 1× erwähnt.

In `tasks.jsonl` → T-001 als `done` markieren (manuell mit Editor: `"status":"pending"` → `"status":"done"`).

Schreib einen Run-Log:
```bash
notepad memory\runs\2026-04-27_stride_prompt_g.md
```
Inhalt: Format aus `01_HARNESS.md` Sektion „Memory-Hierarchie" (Goal/Done/Surprised by/Avoided/Next/Memory updates).

### Schritt 5 — Prompt H, C, D, E, F, B in Sequenz (je 10–15 Min)

Pro Prompt:
1. Sektion in `07_OFFICE_AGENT_PROMPTS.md` öffnen
2. Komplett kopieren, in Stride einfügen
3. Output speichern als `<originalname>_v2.docx` bzw. `_v2.pptx`
4. Datei kurz öffnen, visuell prüfen (Layout intakt? neue Sektion da? Klinikum Dortmund?)
5. `tasks.jsonl` → entsprechenden Task auf `done`
6. Run-Log in `memory/runs/`

Sequenz:
- **Prompt H** → `Carotis_AI_Konzept_v2.docx` (T-002)
- **Prompt C** → `Expose_Carotis_AI_Rohde_v2.docx` (T-003)
- **Prompt D** → `Tech_Description_Klinikum_v2.docx` (T-004)
- **Prompt E** → `Value_Proposition_Klinikum_v2.docx` (T-005)
- **Prompt F** → `Carotis_Ai_Rohde_v2.pptx` (T-006) — **das ist der wichtigste, weil Demo-Material**
- **Prompt B** → `Anschreiben_Aroob_an_Rohde_v2.docx` (T-007) — Backup zum Mail-Text

### Schritt 6 — Prompt A: Mail-Text generieren (10 Min)

**Wichtig:** Du hast ZWEI Pfade für die Mail.

**Pfad A (Stride):** `07_OFFICE_AGENT_PROMPTS.md` → Sektion „PROMPT A". In Stride. Output: `Mail_Aroob_an_Rohde_v2.docx`. Vorteil: Umlaute, Word-Format, einheitlicher Style.

**Pfad B (Plaintext-Backup):** `Mail_Aroob_an_Rohde_DRAFT.txt` ist bereits fertig im Workspace (UTF-8 ohne Umlaute, damit sie in jedem Mail-Client sauber ankommt). Vorteil: kein Stride nötig, kein Halluzinations-Risiko.

**Empfehlung:** Pfad A für die finale Versendung. Pfad B als Vergleichs-Referenz, falls Stride was Komisches generiert.

T-008 auf `done` setzen.

### Schritt 7 — CV als PDF rendern (5 Min)

`CV_Laith_Alshdaifat.md` ist da. Du brauchst ein PDF für die Mail-Anlage.

Zwei Wege:
- **Schnell:** in VS Code öffnen, „Markdown PDF" Extension verwenden, Ctrl+Shift+P → „Markdown PDF: Export (pdf)" → speichern als `CV_Laith_Alshdaifat.pdf`
- **Stride:** Stride-Prompt: *„Wandle die folgende Markdown-Datei in ein professionelles PDF um. Format: A4, Schriftgrad 11pt, Helvetica, dezenter Header mit DiggAI-Branding."* + den CV-Inhalt einfügen.

### Schritt 8 — Aroob-Review koordinieren (variabel, 30–60 Min Aroob's Zeit)

Aroob anrufen oder Cowork-Session mit ihr aufmachen. Ihr alle 8 Files schicken (entweder OneDrive-Share oder per Mail). Sie:

1. Liest die Mail (`Mail_Aroob_an_Rohde_v2.docx`) — klingt das nach ihr? Würde sie das so schreiben?
2. Liest das Konzept (`Carotis_AI_Konzept_v2.docx`) — ist das medizinisch korrekt?
3. Liest das Exposé (`Expose_Carotis_AI_Rohde_v2.docx`) — ist die Methodik realistisch?
4. Sieht die PowerPoint kurz an (`Carotis_Ai_Rohde_v2.pptx`) — funktioniert die als Visual-Begleitung?

Bei jeder Anmerkung von Aroob:
- Mini-Anmerkungen → direkt in Word korrigieren
- Größere Änderungen → zurück zu Stride mit Korrektur-Prompt: *„In Datei X, Sektion Y, ändere Z von ‚alt' zu ‚neu', weil [Begründung]. Gib mir die korrigierte Version."*

T-009 auf `done` setzen.

### Schritt 9 — Mail rausschicken (5 Min)

Aroob öffnet ihr Klinikum-Mail-Konto. Erstellt neue Mail. Empfänger: Prof. Rohde (DIRECT, nicht Sekretariat — ihr habt seine direkte Adresse aus der bisherigen Korrespondenz). Betreff + Mail-Text aus `Mail_Aroob_an_Rohde_v2.docx`. Anhänge:

- Anlage 1: `KI_Tools_Marktanalyse_v2.docx`
- Anlage 2: `Carotis_AI_Konzept_v2.docx`
- Anlage 3: `CV_Laith_Alshdaifat.pdf`

(Optional, je nach Aroob's Komfort: das Exposé `Expose_Carotis_AI_Rohde_v2.docx` als Anlage 4 — mehr ist besser für Akademiker.)

Sendet ab. Zeitpunkt notieren in `memory/runs/2026-04-27_mail_an_rohde.md`.

T-010 auf `done` setzen.

### Schritt 10 — Folge-Erinnerung in deinem Kalender (2 Min)

Erinnerung in 7 Tagen (also für **2026-05-04**): *„Hat Rohde geantwortet? Falls nein: kein zweiter Push, aber Status-Mail in 14 Tagen vorbereiten."*

Dann: zurücklehnen. Du hast deinen Teil gemacht.

---

## Ab jetzt heißt es warten

Bis Rohde antwortet, ist P0 inhaltlich abgeschlossen. Was du in der Zwischenzeit produktiv machen kannst (alles **non-blocking** für P0):

- **dr-aroob-ki Repo durchgehen** — die alten Tasks T-018, T-028 (siehe Elbtronika-Harness) noch offen?
- **Decision-Tree-Capture als Mock-UI** in dr-aroob-ki vorbereiten — wenn Rohde ja sagt, hat Lou's Demo schon das fertige UI-Mock dabei
- **Anonymisierungs-Pipeline weiter** — `scripts/anonymize.py` ist bereits Skelett da, du könntest die Tests grün kriegen
- **Ethik-Antrag-Skelett lesen** — `ethics/ethikantrag_skelett.md` (kommt gleich) — vorab schon mal verstehen, was P1 verlangt
- **Risk-Register weiterführen** — `risk_register.md` dokumentiert Hazards systematisch nach ISO-14971-Stil

---

## Wenn Rohde antwortet

→ `06_ROHDE_MEETING_KIT.md` Sektion 6 + 8 lesen, dann Template 9 (Stakeholder) für die Reply nutzen.

---

## Wenn was schiefgeht

- **Stride hängt / produziert Müll:** Pfad B nutzen (Plaintext-Mail) + die docx-Files manuell mit Word editieren (langsamer, aber sicher)
- **Aroob hat größere Bedenken:** STOP. Cowork-Session öffnen, mit Opus 4.7 darüber reden. Lieber 1 Tag verschieben als eine schlechte Mail rausschicken
- **Du bist müde / frustriert:** STOP. Morgen früh fertig machen. Zwei Stunden Schlaf > 30 Minuten unfocused arbeit

---

**Letzte Aktualisierung:** 2026-04-27 · Opus 4.7
