# P0f — Production-Demo-Pivot Prompts (Kimi K2.6 + Codex GPT-5.5 + Sonnet 4.6)

> **Stand:** 2026-04-30 · **Plan-Run:** `memory/runs/2026-04-30_opus47_p0f_pivot_plan.md`
>
> **Ziel von P0f:** Mail an Prof. Rohde geht raus mit **Live-Link + Repo + Webseite**, nicht mit Konzept-PDF. Rohde kann selbst klicken bevor er antwortet. Strategie-Shift: "Wir haben gebaut" statt "Wir wollen bauen".
>
> **Kontext:** Code-Stack ist done (P0e: 101/101 pytest, 12/12 Vitest, 0 Anomalien). Stride V2 Office-Docs liegen in `Stride V2/`. App + Backend lauffaehig via `make demo`. Es fehlen: oeffentliche Webseite, Cloud-Deploy mit Auth-Gate, Walkthrough-Mode, Rohde-Kit, Mail v3.
>
> **Wellen-Logik (parallel auf disjunkten Datei-Ownerschaften):**
> - **Welle A (Tag 1-3):** W-01 (Kimi) + W-02 (Codex) parallel.
> - **Welle B (Tag 1-3, parallel zu A):** W-03 + W-04 + W-05 (alle Kimi, disjunkte Frontend-Pfade).
> - **Welle C (Tag 3-4):** W-06 (Codex) + W-07 + W-08 (Sonnet).
> - **Welle D (Tag 5):** W-09 + W-10 (Opus 4.7 generiert Stride V3 Prompts, Lou fuehrt sie aus).
> - **Welle E (Tag 6-7):** W-11 (Codex) + W-12 (Lou).
>
> **Pre-Flight fuer JEDE Welle:** Lies CLAUDE.md, AGENTS.md, MEMORY.md, letzte 3 Run-Logs unter `memory/runs/`. Pruefe `memory/anomalies/`. Setze Task in `tasks.jsonl` auf `in_progress`. Schreib am Ende `memory/runs/<datum>_<welle>.md`.
>
> **Hard Rules:** Keine Patientendaten in Cloud. Keine Office-Doc-Edits durch Modell — nur Stride-Prompts. Keine Cloud-Inferenz fuer echte DICOM. Local-First bleibt religioes.

---

## WELLE A — Public Webseite + Cloud-Deploy

### W-01 — Public Landing `carotis.diggai.de` (Kimi K2.6)

**Routing:** Kimi K2.6 (Boilerplate + Tailwind, Output-Token-schonend via caveman).

**Prompt:**

```text
Du bist Kimi K2.6. Pre-Flight: lies CLAUDE.md, AGENTS.md, MEMORY.md, runs/2026-04-30_opus47_p0f_pivot_plan.md.

Aufgabe W-01: Erstelle eine statische Public-Landing-Page fuer carotis.diggai.de.

Ownership (disjunkt):
- Neue Datei `code/website/index.html`
- Neue Datei `code/website/style.css` (oder Tailwind via CDN inline)
- Neue Datei `code/website/assets/` mit Logo-SVG + 3 App-Screenshot-Placeholdern
- Neue Datei `code/website/README.md` mit Build- und Deploy-Anleitung
- Neue Datei `code/website/netlify.toml` fuer Netlify-Deploy

Berührt NICHT: backend, frontend, ml, scripts, tests, regulatory, ethics, memory.

Inhalt (DEUTSCH, sachlicher Ton, keine "revolutionaer"-Sprache):

1. **Hero-Section** — H1: "Carotis-AI — Lokale, erklaerbare Carotis-Diagnostik"
   Tagline: "Promotionsprojekt am Klinikum Dortmund. Local-First. DSGVO by Design. Decision-Tree-Harvesting."
   Primary CTA: "Demo testen" → linkt auf `https://app.carotis.diggai.de` (Token-Gated)
   Secondary CTA: "Konzept lesen" → linkt auf PDF des Carotis-AI-Konzepts (Anlage 2)

2. **Problem-Section** — 3 Bullets:
   - Marktloesungen sind cloud-basiert → DSGVO-Risiko in deutschen Kliniken
   - Generische Tools sind nicht Carotis-spezifisch
   - Black-Box-Modelle ohne Erklaerbarkeit kollidieren mit EU AI Act Art. 13

3. **Loesungs-Section** — Architektur-Diagramm (SVG inline) mit 4 Layern:
   - Pixel-Layer (MFSD-UNet, Dice 0.91 nach Xie 2024)
   - XAI-Layer (HiResCAM Heatmap, Grad-CAM Fallback, ADR-005)
   - Decision-Tree-Harvesting-Layer (anonymisierte Begruendungs-Strukturen)
   - Daily-Learning-Loop (taegliche inkrementelle Updates)

4. **Trust-and-Security-Section** — 5 Bullets mit Icons:
   - Local-First: Patientendaten verlassen das Klinikum nie
   - DSGVO Art. 35 DPIA done (Skelett in `ethics/dpia_skelett.md`)
   - DICOM PS 3.15 Anonymisierung (33 PII-Tags)
   - ISO 14971 Risk Register (11 Hazards inkl. Freitext-PII)
   - DIN EN 62304 Plan-File in Vorbereitung (Margaritoff-Review)

5. **Team-Section** — 3 Cards:
   - Dr. med. Aroob Alrawashdeh — Aerztin in Weiterbildung Radiologie, Klinikum Dortmund
   - Laith Alshdaifat (Lou) — Medizintechniker HAW Hamburg, Engineering-Lead
   - Dr. Islam Shdaifat — JoVision, AI-Architect, 4 Patente Computer Vision
   Mit Hinweis: "Wissenschaftliche Beratung: Prof. Margaritoff (DIN EN 62304), Prof. Tolg (SIMLab), Prof. van Stevendaal (Vorsitz Medizintechnik HH)."

6. **FAQ-Section** — 6 Akkordeon-Items, basierend auf 06_ROHDE_MEETING_KIT.md F1-F10. Kurzantworten, je 2-3 Saetze.

7. **Contact-Section** — mailto-Link zu `aroob.alrawashdeh@klinikumdo.de` (oder Lou, falls Aroob nicht oeffentlich) + LinkedIn-Lous + GitHub-Link (privat oder Public-Repo Link).

8. **Footer** — Impressum-Link (Pflicht in DE), Datenschutz-Link, Verweis "Demo-Webseite — kein Medizinprodukt im Sinne der MDR".

Tech:
- Tailwind CSS via CDN (kein Build-Step zwingend) ODER Vite+Tailwind als optional Build-Pfad — entscheide pragmatisch.
- Mobile-first responsive.
- Dark-Theme mit `slate-950 / slate-100`, semantische Farben wie im Frontend.
- Lighthouse-Score Performance >= 90, Accessibility >= 95.

Deployment:
- `netlify.toml` mit `publish = "."`, `command = ""`. Keine Build-Step noetig wenn pure HTML+CDN.
- Custom-Domain Setup-Anleitung in `code/website/README.md`: DNS CNAME `carotis.diggai.de` → Netlify-Subdomain.

DoD:
- 5 Sektionen rendern korrekt
- mailto-Link funktioniert
- Keine externen JS-Tracker (DSGVO!)
- Lighthouse Run lokal >= 90/95
- README.md erklaert Deploy in 10 Zeilen

Run-Log: `memory/runs/2026-04-30_kimi_W-01.md` mit Goal/Done/Surprised-by/Avoided/Next.
```

---

### W-02 — Demo-Deploy + Auth-Gate `app.carotis.diggai.de` (Codex GPT-5.5)

**Routing:** Codex GPT-5.5 (Infra-Code, Docker, Reverse-Proxy, Auth-Logik).

**Prompt:**

```text
Du bist Codex GPT-5.5. Pre-Flight: lies CLAUDE.md, AGENTS.md, MEMORY.md, runs/2026-04-30_opus47_p0f_pivot_plan.md, regulatory/hardware_spec.md.

Aufgabe W-02: Erstelle eine Cloud-Deploy-Pipeline fuer den Demo-Stack mit Token-Gated Auth.

Ownership (disjunkt):
- Neue Datei `deploy/Dockerfile.demo` (Multi-Stage, kombiniert Backend+Frontend in einem Image fuer den Demo-Use-Case)
- Neue Datei `deploy/Caddyfile` (Reverse-Proxy mit automatischem HTTPS via Let's Encrypt)
- Neue Datei `deploy/docker-compose.demo.yml`
- Neue Datei `deploy/fly.toml` (Fly.io Region fra, Hetzner als Alternative dokumentiert)
- Neue Datei `deploy/README.md` mit Step-by-Step Deploy-Anleitung
- Edit `code/backend/app/core/security.py`: Erweitere um `verify_demo_token()` Function (separater Header `X-Demo-Token` mit Pruefung gegen Whitelist in DB)
- Edit `code/backend/app/db/models.py`: Neue Tabelle `DemoToken(token_hash, label, expires_at, requests_used, max_requests)` 
- Neue Datei `code/backend/app/api/routes/demo.py`: GET /api/v1/demo/whoami (returns Token-Label + Quota), POST /api/v1/demo/log-walkthrough-step

Berührt NICHT: frontend (W-03/04 zustaendig), website (W-01 zustaendig), ml, scripts, tests/test_audit_trail.py, tests/test_inference_full.py, regulatory, ethics, memory.

Architektur:
- Single-Container Demo-Image: `python:3.13-slim` Base, Python-Backend + nginx fuer Static-Frontend-Build
- Caddy als externer Reverse-Proxy mit automatischem TLS und Rate-Limiting
- SQLite persistiert in Volume `/data` (Fly Volume oder Hetzner-Volume)
- Demo-Tokens werden vorab via `scripts/generate_rohde_token.py` (W-06) erstellt
- Token-Whitelist in Tabelle `DemoToken`. Header `X-Demo-Token` ueberschreibt `X-API-Key` fuer Demo-Endpoints
- Audit-Tag `audit_event.metadata = {"demo_token_label": "rohde-2026-04-30"}` damit Lou nachvollziehen kann was Rohde geklickt hat

Sicherheit:
- Demo-Tokens sind 32-Byte SHA-256-Hashes (in DB nur Hash, nie Klartext)
- Rate-Limit per Token: 100 Inferenzen / Tag, 500 Decision-Tree-Captures / Tag
- Auto-Expiry nach 30 Tagen
- Robots.txt: Disallow:/ fuer den App-Subdomain (Rohde soll keine Indexierung)

Tests (DoD):
- Neuer Test `code/tests/test_demo_token.py` mit 6 Tests: Token-Hashing, Whitelist-Lookup, Expired-Token-Reject, Rate-Limit-Enforce, Audit-Tag-Persist, Whoami-Endpoint
- Bestehende Tests gruen halten: `pytest -p no:warnings` 101 + 6 = 107 passed
- ruff 0, black formatted, npm typecheck 0 (Frontend nicht beruehrt aber lint nicht brechen)

Run-Log: `memory/runs/2026-04-30_codex_W-02.md`.

WICHTIG: Branch-Schutz beachten. Erstelle PR mit Titel `feat(demo): production-grade demo deploy with token-gated auth (W-02)`. Nicht direkt nach main pushen.
```

---

## WELLE B — Frontend Hardening (parallel zu Welle A, Kimi K2.6)

### W-03 — Walkthrough-Mode (5-Step-Tour) (Kimi K2.6)

**Prompt:**

```text
Du bist Kimi K2.6. Pre-Flight wie ueblich.

Aufgabe W-03: Walkthrough-Mode fuer das Frontend bauen. Zielgruppe: Prof. Rohde, klickt zum ersten Mal in die App.

Ownership (disjunkt):
- Neuer Ordner `code/frontend/src/components/Walkthrough/`
  - `Walkthrough.tsx` — Container mit Progress, Next/Back/Skip
  - `WalkthroughStep.tsx` — Single-Step-Renderer (Title, Text, Highlight-Target via data-tour-id)
  - `useWalkthrough.ts` — Hook mit State-Machine (5 Steps)
  - `Walkthrough.test.tsx` — Vitest mit 4 Tests (Mount, Next, Skip, Done-Callback)
- Edit `code/frontend/src/App.tsx`: Mount `<Walkthrough />` wenn URL-Param `?tour=1` gesetzt ODER Token-Label = "rohde-*" (via `whoami`-Response)
- Edit `code/frontend/src/components/AiPanel/AiPanel.tsx`: data-tour-id-Attribute auf 3 wichtigen Elementen
- Edit `code/frontend/src/components/DicomViewer/DicomViewer.tsx`: data-tour-id auf Viewer
- Edit `code/frontend/src/components/DecisionForm/DecisionForm.tsx`: data-tour-id auf Form

Berührt NICHT: backend (W-02 zustaendig), website, ml, scripts, regulatory, ethics, memory.

5-Step-Walkthrough (DEUTSCHE Texte):

Step 1 — Welcome (Modal-Card zentriert)
- Titel: "Willkommen bei Carotis-AI"
- Text: "Diese Tour zeigt Ihnen in 3 Minuten, wie das System einen CTA-Datensatz analysiert. Sie koennen jederzeit ueberspringen."
- Highlight: keiner

Step 2 — DICOM laden (Tooltip an DicomViewer)
- Titel: "Schritt 1 — Synthetischer Fall geladen"
- Text: "Hier sehen Sie einen synthetischen CTA-Datensatz. Die App laeuft mit anonymisierten Demo-Faellen — keine echten Patientendaten."
- Highlight: DicomViewer

Step 3 — AI-Analyse (Tooltip an AiPanel)
- Titel: "Schritt 2 — KI-Vorschlag mit Vertrauenswert"
- Text: "Das Modell schaetzt Stenosegrad nach NASCET, Plaque-Vulnerability und liefert einen Trust-Score. Die HiResCAM-Heatmap zeigt, worauf das Modell sich stuetzt."
- Highlight: AiPanel

Step 4 — Decision-Tree (Tooltip an DecisionForm)
- Titel: "Schritt 3 — Ihre Entscheidung in 30 Sekunden"
- Text: "Bestaetigen oder korrigieren Sie den Vorschlag. Ihre Begruendung wird anonymisiert gespeichert und am naechsten Tag fliesst sie ins Modell-Update."
- Highlight: DecisionForm

Step 5 — Done (Modal-Card zentriert)
- Titel: "Tour abgeschlossen"
- Text: "Sie haben gerade einen kompletten Befundungsvorgang gesehen. Der reale Workflow im Klinikum waere identisch — nur mit echten DICOM-Daten via PVS. Fragen? Kontakt: aroob.alrawashdeh@klinikumdo.de"
- CTA: "Eigenen Demo-Fall ausprobieren" → setzt `?tour=0` und laedt eine zufaellige Demo-Case.

UI:
- Tooltip-Stil: Tailwind dark mit `bg-slate-900 border-emerald-400`. Pfeil zum Highlight.
- Modal-Stil: zentriert, `max-w-md`, mit Backdrop-Blur.
- Progress-Indicator: 5 Dots oben rechts.
- localStorage-Key `carotis_tour_done` damit Tour nicht 2x ungewollt startet.

DoD:
- `npm test -- --run` 12 + 4 = 16 Tests gruen
- `npm run typecheck` 0 Fehler
- `npm run lint` 0 Fehler
- `npm run build` SUCCESS
- Manuelle Pruefung: `?tour=1` startet Tour, Skip schliesst, Next/Back funktionieren

Run-Log: `memory/runs/2026-04-30_kimi_W-03.md`.
```

---

### W-04 — i18n-Dict + UI-String-Audit DE (Kimi K2.6)

**Prompt:**

```text
Du bist Kimi K2.6. Pre-Flight wie ueblich.

Aufgabe W-04: Alle Frontend-UI-Strings in eine zentrale i18n-Datei extrahieren. Sicherstellen dass nichts mehr Englisch im UI ist (Code bleibt Englisch, UI ist Deutsch — siehe CLAUDE.md Sprachregelung).

Ownership (disjunkt):
- Neue Datei `code/frontend/src/lib/i18n.ts` mit `t()`-Funktion und Default-Locale `de`
- Neue Datei `code/frontend/src/lib/i18n.test.ts` mit 3 Tests
- Edit `code/frontend/src/components/AiPanel/AiPanel.tsx`: ersetze Roh-Strings durch `t("ai_panel.foo")`
- Edit `code/frontend/src/components/ConfidenceBadge.tsx`: ersetze Roh-Strings
- Edit `code/frontend/src/components/DecisionForm/DecisionForm.tsx`: ersetze Roh-Strings
- Edit `code/frontend/src/components/FreeTextField.tsx`: ersetze Roh-Strings
- Edit `code/frontend/src/components/DicomViewer/DicomViewer.tsx`: ersetze Roh-Strings
- Edit `code/frontend/src/App.tsx`: ersetze Roh-Strings

Berührt NICHT: backend, website, ml, scripts, regulatory, ethics, memory, Walkthrough-Komponenten (W-03 hat eigene Strings inline).

Implementation:
- `i18n.ts` exportiert `t(key: string, vars?: Record<string,string>): string`
- Locale-File `de` als Object Literal (kein JSON-Loader noetig)
- Vars-Substitution mit `{{name}}` Pattern
- Fallback-Verhalten: wenn key nicht existiert, returne key + `console.warn("missing-i18n-key")`

Audit-Regel:
- Vor dem Commit: `grep -rE "(['\"])(Confidence|Loading|Error|Submit|Cancel|Save|Delete)" code/frontend/src/components/` MUSS leer sein
- Alle UI-Strings mit Grossbuchstabe-Anfang im JSX MUESSEN durch `t()` ersetzt sein

DoD:
- 12 Vitest + 4 (W-03) + 3 (W-04) = 19 Tests gruen
- npm typecheck/lint/build alle 0
- Manuell: deutsche UI-Strings sind komplett. Englisch nur in Code/Kommentaren.

Run-Log: `memory/runs/2026-04-30_kimi_W-04.md`.
```

---

### W-05 — 30 Synthetic-Cases + 5 Decision-Tree-Beispiele (Kimi K2.6)

**Prompt:**

```text
Du bist Kimi K2.6. Pre-Flight wie ueblich.

Aufgabe W-05: Demo-Daten erweitern. Aktuell 10 synthetische DICOMs. Ziel: 30 Faelle, die alle relevanten klinischen Szenarien abdecken, plus 5 vorgespielte Decision-Tree-Eintraege fuer "Walkthrough-Default-Fall".

Ownership (disjunkt):
- Edit `code/scripts/generate_demo_data.py`: erweitere von 10 auf 30 Faelle
- Edit `code/scripts/generate_demo_data.py`: optionaler Flag `--with-decision-trees` der 5 vorgespielte JSON-Decision-Trees in die DB schreibt
- Neue Datei `code/scripts/test_generate_demo_data.py` (oder Erweiterung der bestehenden) mit 4 zusaetzlichen Tests (Stenosegrad-Coverage, Plaque-Type-Coverage, Decision-Tree-Validity, Idempotenz)
- Neue Datei `code/data/demo/case_catalog.json` als Manifest aller 30 Faelle (case_id, side, stenosis_grade, plaque_type, intent_tag)

Berührt NICHT: backend/app, frontend, website, ml, regulatory, ethics, memory.

Coverage-Matrix (30 Faelle, je 6 pro Stenosegrad-Klasse, je 7-8 pro Plaque-Typ):

Stenosegrade (NASCET):
- 0-29% (mild): 6 Faelle
- 30-49% (moderat): 6 Faelle
- 50-69% (moderat-schwer): 6 Faelle
- 70-99% (schwer): 6 Faelle
- Okklusion 100%: 6 Faelle

Plaque-Typen (multi-label, je Fall 1-2 Marker):
- IPH (intraplaque haemorrhage): 8 Faelle
- ThinCap (thin fibrous cap): 7 Faelle
- LRNC (lipid-rich necrotic core): 8 Faelle
- Calcified: 7 Faelle

Seiten:
- Links: 15 Faelle
- Rechts: 15 Faelle

Edge-Cases (manuell setzen):
- 1 Fall mit grenzwertiger Bildqualitaet (Motion-Artefakt simuliert)
- 1 Fall mit starker Verkalkung (Beam-Hardening simuliert)
- 1 Fall mit beidseitig hochgradiger Stenose
- 1 Fall mit Vortritt-Befundung "Karotis-Web" als seltene Variante
- 1 Fall mit unklarer Plaque-Morphologie (sollte vom Modell mit niedrigem Trust-Score kommen)

5 vorgespielte Decision-Trees (fuer Walkthrough-Default und Trust-Calibration-Demo):
- Fall 01: Modell sagt 65% Stenose / IPH, Arzt bestaetigt → high agreement, high trust
- Fall 02: Modell sagt 30% Stenose, Arzt korrigiert auf 45% → disagreement, mid trust
- Fall 03: Modell sagt 80% Stenose, Arzt bestaetigt → high agreement, mid trust
- Fall 04: Modell sagt LRNC, Arzt sagt ThinCap → plaque-type-disagreement, low trust on plaque
- Fall 05: Edge-Fall — Modell unsicher (trust 0.4), Arzt setzt Override mit Freitext "Karotis-Web Verdacht"

case_catalog.json Format:
[
  {"case_id":"case_01","side":"left","stenosis":65,"plaque":["IPH"],"tour_default":true,"description":"Walkthrough-Default-Fall"},
  ...
]

DoD:
- 30 .dcm Files in `code/data/demo/dicom/`
- 5 Decision-Tree-Records nach `--with-decision-trees`-Flag in DB
- pytest 101 + 4 (W-05) = 105 passed (W-02-Tests koennen parallel hinzukommen)
- Manuell: `python scripts/generate_demo_data.py --with-decision-trees && curl http://localhost:8000/api/v1/decision-tree/recent` zeigt 5 Eintraege

Run-Log: `memory/runs/2026-04-30_kimi_W-05.md`.
```

---

## WELLE C — Rohde-Kit (Tag 3-4)

### W-06 — Rohde-Token-Generator (Codex GPT-5.5)

**Prompt:**

```text
Du bist Codex GPT-5.5. Pre-Flight wie ueblich. W-02 muss durch sein (deine Tabelle DemoToken existiert).

Aufgabe W-06: CLI-Skript zum Erzeugen von Demo-Tokens mit Audit-Tagging.

Ownership (disjunkt):
- Neue Datei `code/scripts/generate_rohde_token.py`
- Edit `code/scripts/test_generate_rohde_token.py` (neu) mit 5 Tests
- Edit `code/Makefile`: Target `make rohde-token`

Berührt NICHT: backend/app/core (ausser via Modell-Import), frontend, website, regulatory, ethics, memory.

Funktion:
```
python scripts/generate_rohde_token.py \
  --label "rohde-2026-04-30" \
  --max-requests 500 \
  --expires-days 30 \
  --output rohde_token.txt
```

Verhalten:
- Generiert 32-Byte URL-safe Token via `secrets.token_urlsafe(32)`
- Hash-Speichert in DemoToken-Tabelle (BLAKE2b mit per-deploy Salt aus env)
- Schreibt KLARTEXT-Token in --output File mit Permissions 0600
- Print Confirmation auf stdout MIT bewusst Klartext-Token (Lou kopiert ins Mail)
- Audit-Event "demo_token_generated" mit label, expires_at

DoD:
- 101 + 6 (W-02) + 5 (W-06) = 112 pytest passed
- Manuell: Skript laeuft, Token funktioniert via `curl -H "X-Demo-Token: <token>" http://localhost:8000/api/v1/demo/whoami`
- Ausgabedatei hat permissions 0600 unter Linux/macOS

Run-Log: `memory/runs/2026-04-30_codex_W-06.md`.
```

---

### W-07 — Rohde-Anleitung 2-Seiten-PDF (Sonnet 4.6 mit docx skill)

**Prompt:**

```text
Du bist Sonnet 4.6. Pre-Flight wie ueblich. Lies zusaetzlich 06_ROHDE_MEETING_KIT.md.

Aufgabe W-07: 2-Seiten-Anleitung fuer Prof. Rohde, damit er die Demo selbststaendig nutzen kann. Output: .docx ueber den anthropic-skills:docx Skill, dann nach Stride V3 zum PDF-Export.

Ownership (disjunkt):
- Neue Datei `outputs/Rohde_Anleitung_v1.docx` (von dir generiert)
- Neue Datei `Stride V3/Rohde_Anleitung_PROMPT.md` (Stride-Prompt fuer Lou zum Polishen + PDF-Export)

Berührt NICHT: backend, frontend, website, scripts, ml, tests, regulatory (ausser als Quelle), ethics, memory ausser eigenes Run-Log.

Inhalt (DEUTSCH, formell, Sie-Form, max 2 Seiten):

Seite 1 — Was ist Carotis-AI?
- 3 Saetze Projekt-Kontext (Klinikum Dortmund, Promotion Aroob, Local-First)
- Was die Demo zeigt: synthetische DICOM-Faelle, AI-Vorschlag mit Trust-Score, Decision-Tree-Capture
- Was die Demo NICHT zeigt: keine echten Patientendaten, keine PVS-Integration, keine taegliche Modell-Aktualisierung (das passiert erst nach Ihrem Go)
- Sicherheits-Hinweis: Token ist personalisiert, gilt 30 Tage, 500 Requests Limit

Seite 2 — Wie nutze ich die Demo?

Schritt 1 — Webseite besuchen
URL: `https://carotis.diggai.de`
Was Sie sehen: Konzept-Uebersicht und CTA "Demo testen"

Schritt 2 — Demo-App oeffnen mit persoenlichem Token
URL: `https://app.carotis.diggai.de?tour=1`
Token (in Zwischenablage kopieren beim Login):
[Lou setzt hier den realen Token ein vor dem Versand]

Schritt 3 — Walkthrough abschliessen (3 Minuten)
Die Tour fuehrt durch DICOM-Viewer, AI-Panel, Decision-Form. Nach Abschluss koennen Sie eigene Faelle aus dem 30-Fall-Katalog auswaehlen.

Schritt 4 — Decision-Tree-Capture testen
Nach AI-Vorschlag: Stenose-Slider, Plaque-Type-Checkboxen, Trust-Score-Stern, optionaler Freitext. 30 Sekunden pro Fall.

Schritt 5 — Feedback geben
Antworten Sie bitte auf die Mail von Aroob mit Ihrer Einschaetzung: passt die UX zum Klinikum-Workflow? Welche Felder fehlen?

FAQ (3 kurze QA):
- "Was passiert mit meinen Klicks?" → Nur Audit-Tag mit Token-Label, keine PII, lokal.
- "Funktioniert das im Klinikum-Netz?" → Ja, falls keine SSL-Inspektion. Sonst lokal an Aroobs Laptop testen.
- "Wie sicher ist der Token?" → 32-Byte-Random, Hash in DB, Auto-Expiry. Kein Schaden falls verloren — Lou kann widerrufen.

Footer Seite 2:
- Kontakt fuer Rueckfragen: Lou (laith.alshdaifat@haw-hamburg.de) und Aroob
- Hinweis: "Demo-App ist kein Medizinprodukt im Sinne der MDR."

Format:
- Schriftart: Calibri 11pt, Zeilenabstand 1.15
- Header: "Carotis-AI · Demo-Anleitung fuer Prof. Dr. med. Stefan Rohde"
- Footer: "Stand: 30.04.2026 · Vertraulich · Token-personalisiert"

Stride V3 Prompt (Lou-Anweisung):
- Datei `Stride V3/Rohde_Anleitung_PROMPT.md` enthaelt: "Oeffne `outputs/Rohde_Anleitung_v1.docx`, ersetze Token-Platzhalter mit dem realen Token aus W-06 Output, exportiere als PDF nach `Stride V3/Rohde_Anleitung_v1.pdf`."

DoD:
- Datei `outputs/Rohde_Anleitung_v1.docx` existiert, oeffnet sauber in Word
- Stride-Prompt fertig zum Copy-Paste in Stride-UI
- 2 Seiten exakt (kein Overflow)

Run-Log: `memory/runs/2026-04-30_sonnet_W-07.md`.
```

---

### W-08 — Walkthrough-Video-Skript 3 Min (Sonnet 4.6)

**Prompt:**

```text
Du bist Sonnet 4.6. Pre-Flight wie ueblich.

Aufgabe W-08: Skript fuer ein 3-Minuten-Walkthrough-Video, das Lou aufnimmt und in der Mail an Rohde verlinkt (YouTube unlisted oder Loom).

Ownership (disjunkt):
- Neue Datei `outputs/Rohde_Video_Script_v1.md` (Markdown mit Zeit-Stempeln, Sprecher-Notizen, B-Roll-Hinweisen)

Berührt NICHT: irgendetwas anderes.

Inhalt (DEUTSCH, sachlich-warm, Lou als Sprecher):

[00:00 - 00:15] Hook
- B-Roll: Public-Webseite Hero-Section
- Sprecher: "Sehr geehrter Herr Prof. Rohde, mein Name ist Laith Alshdaifat — der Schwager von Aroob. Ich nehme Sie in den naechsten drei Minuten mit durch das, was wir auf Basis Ihrer Floy-Hausaufgabe gebaut haben."

[00:15 - 00:45] Architektur in 30 Sekunden
- B-Roll: Architektur-Diagramm aus 04_MASTER_PLAN.md, langsame Zoom-Bewegung
- Sprecher: "Carotis-AI ist Local-First. Patientendaten verlassen Ihr Klinikum nie. Das Modell laeuft auf einem Edge-Server. Erklaerbarkeit kommt aus HiResCAM-Heatmaps. Und das wirklich Neue: wir lernen nicht nur das Bild, sondern auch die anonymisierte Begruendungs-Struktur der Befundung — Decision-Tree-Harvesting nennen wir das."

[00:45 - 01:30] Live-Demo Stenose-Befund
- B-Roll: Bildschirmaufnahme der Demo-App, DICOM laedt
- Sprecher: "Hier laden wir einen synthetischen Fall. Das Modell liefert in unter drei Sekunden einen Stenosegrad nach NASCET, eine Plaque-Klassifikation und eine HiResCAM-Heatmap. Sie sehen rechts den Trust-Score — fuenf Segmente, von wenig bis viel Vertrauen."

[01:30 - 02:00] Decision-Tree-Capture
- B-Roll: Decision-Form rechts, Stenose-Slider, Checkboxen, Trust-Stern
- Sprecher: "Der Befunder bestaetigt oder korrigiert. 30 Sekunden. Das System speichert anonym die Begruendung. Heute Nacht fliesst diese Begruendung ins naechste Modell-Update."

[02:00 - 02:30] Was das Klinikum bekommt
- B-Roll: Stride V2-Schluessel-Slide aus dem Expose
- Sprecher: "Fuer das Klinikum: null Euro, null Cloud, null PII-Export. Fuer Aroobs Promotion: ein klinisches Validierungs-Paper und ein Methodik-Paper, beide mit Ihrem Namen als Senior-Author. Fuer Sie: ein Promotionsprojekt, das schon laeuft, statt noch geplant wird."

[02:30 - 03:00] Ask
- B-Roll: zurueck zur Webseite mit Contact-Section
- Sprecher: "Wir bitten Sie nicht um eine Entscheidung im Voraus. Wir bitten Sie nur, die Demo zu testen — Aroob hat Ihnen einen persoenlichen Token geschickt — und uns dann zu sagen, was Sie ergaenzen wuerden, bevor wir den Ethikantrag schreiben. Vielen Dank fuer Ihre Zeit."

Aufnahme-Hinweise:
- Tool: Loom oder OBS, 1080p, 30fps, Mikrofon mit Pop-Schutz
- Hintergrund: neutraler Schreibtisch oder Blur, Bookcase okay aber keine privaten Fotos
- Kleidung: Hemd, kein Logo
- Tempo: 130-140 Woerter pro Minute, ausreichende Pausen
- Outro: 1 Sekunde Standbild Carotis-AI-Logo

Distribution:
- YouTube unlisted oder Loom mit Workspace-Sharing-Link
- Link in Mail v3 (W-09) als "Optional: 3-Minuten-Walkthrough"

DoD:
- Skript laeuft beim Sprechen genau 3:00 Minuten +/- 10 Sekunden
- B-Roll-Hinweise eindeutig (Lou kann ohne Rueckfrage aufnehmen)
- Outro-Folie als SVG/PNG-Hinweis: "Use code/website/assets/logo.svg, fade-in 0.3s"

Run-Log: `memory/runs/2026-04-30_sonnet_W-08.md`.
```

---

## WELLE D — Stride V3 + Mail v3 (Tag 5, Opus 4.7)

### W-09 — Mail v3 Anschreiben Stride-Prompt (Opus 4.7)

**Prompt:**

```text
Du bist Opus 4.7. Pre-Flight: lies CLAUDE.md, AGENTS.md, MEMORY.md, 06_ROHDE_MEETING_KIT.md (Master-Entwurf der alten Mail), Stride V2/Anschreiben_Aroob_an_Rohde_v2.docx, runs/2026-04-30_t012_rohde_reply_kit.md, runs/2026-04-30_opus47_p0f_pivot_plan.md.

Aufgabe W-09: Generiere Stride V3 Prompt fuer das aktualisierte Anschreiben an Prof. Rohde. Strategie-Shift: Mail referenziert Live-Demo + Webseite + Repo, NICHT mehr nur ein Konzept.

Ownership (disjunkt):
- Neue Datei `Stride V3/Anschreiben_Aroob_an_Rohde_v3_PROMPT.md`

Berührt NICHT: irgendwelche .docx-Dateien direkt (HARD RULE: Modell editiert keine Office-Docs).

Inhalt des Stride-Prompts:

```
Stride V3 Prompt — Anschreiben Aroob an Prof. Rohde v3

Quelle: `Stride V2/Anschreiben_Aroob_an_Rohde_v2.docx`
Output: `Stride V3/Anschreiben_Aroob_an_Rohde_v3.docx`

Aufgabe (Stride):
1. Oeffne v2-Dokument.
2. Ersetze die alten Kern-Absaetze (Floy-Recherche-Zusammenfassung, Konzept-Anlagen-Verweis) durch den unten stehenden v3-Text.
3. Aktualisiere Anlagen-Liste: 1) Floy-Marktanalyse v2 (existiert), 2) Demo-Zugang (Webseite + App + Token), 3) Carotis-AI-Konzeptpapier v2 (existiert), 4) CV Lou (existiert).
4. Speichere als v3.docx im Stride V3 Ordner.

Ton-Regeln (unveraenderbar):
- Sie-Form, formell, Aroob als Aerztin in Weiterbildung
- Kein "weltweit erste", "revolutionaer", "bahnbrechend"
- Konkrete Zahlen statt Adjektive
- Max 25 Zeilen Mailtext
- Zwei Anhaltspunkte zur konkreten Aktion (Demo testen + Termin vorschlagen)

v3-Text (zwischen den Markern einfuegen, alten Kerntext ersetzen):

>>> START v3-Kerntext

Sehr geehrter Herr Prof. Rohde,

vielen Dank fuer Ihre Aufgabenstellung. Die Recherche zu KI-Tools in der Radiologie und der Floy-Software ist abgeschlossen (Anlage 1). Die zentrale Erkenntnis: keine der etablierten Loesungen erfuellt gleichzeitig DSGVO-Anforderungen, Carotis-Spezifitaet und Erklaerbarkeit fuer den deutschen Klinikum-Workflow.

Aus dieser Luecke heraus haben mein Schwager Laith Alshdaifat und ich in den vergangenen Wochen einen lauffaehigen Prototyp gebaut, statt nur ein Konzept zu schreiben:

- Lokales Backend mit MFSD-UNet-Inferenz, ONNX-Runtime, HiResCAM-Heatmap und Decision-Tree-Capture (101 automatisierte Tests gruen).
- React-Frontend mit DICOM-Viewer, AI-Panel und 30-Sekunden-Befundungs-Form (12 Frontend-Tests gruen).
- Audit-Trail nach DICOM PS 3.15 und Risk-Register nach ISO 14971.

Sie koennen das System ohne Klinikum-Zugang oder Patientendaten ueber einen persoenlichen Token testen:

  Webseite: https://carotis.diggai.de
  Demo-App: https://app.carotis.diggai.de?tour=1
  Token: <REPLACE_BY_LOU_FROM_W-06_OUTPUT>
  Anleitung: Anlage 2 (Rohde_Anleitung_v1.pdf, 2 Seiten)
  Optional: 3-Minuten-Walkthrough-Video <YOUTUBE_LINK_VON_LOU>

Mein Wunsch: dass Sie die Demo zehn Minuten lang ausprobieren und uns danach Ihre Einschaetzung zukommen lassen — was fehlt aus Klinikum-Sicht, was wuerden Sie zuerst aendern. Ein Termin-Wunsch fuer ein 30-Min-Gespraech meinerseits: <THREE_DATE_OPTIONS_BY_LOU>.

Mit freundlichen Gruessen
Aroob Alrawashdeh
Aerztin in Weiterbildung fuer Radiologie
Klinikum Dortmund

>>> END v3-Kerntext

Anlagen v3:
1. KI_Tools_Marktanalyse_v2.pdf (aus Stride V2)
2. Rohde_Anleitung_v1.pdf (aus W-07 Stride-Schritt)
3. Carotis_AI_Konzept_v2.pdf (aus Stride V2 → PDF-Export, Stride V3 Prompt H)
4. CV_Laith_Alshdaifat.pdf (aus CV_Laith_Alshdaifat.md → docx skill → PDF)

Pre-Send-Checks (Lou):
- Token aus W-06 wirklich eingesetzt
- 3 Termin-Optionen mit Datum + Uhrzeit eingesetzt
- Video-Link gesetzt oder Zeile geloescht falls kein Video aufgenommen
- Keine Tippfehler in der Anrede
- Anlagen alle dabei
- Mail kommt von Aroobs Klinikum-Adresse, nicht private

Trigger nach Versand: T-009 in tasks.jsonl auf done. Run-Log `memory/runs/<datum>_lou_T-009_mail_sent.md`.
```

DoD:
- Stride-Prompt-Datei existiert in `Stride V3/`
- Lou kann den Inhalt 1:1 in Stride-UI als Prompt eingeben

Run-Log: `memory/runs/2026-04-30_opus_W-09.md`.
```

---

### W-10 — Stride V3 Office-Doc-Updates (Opus 4.7 generiert alle 7 Prompts)

**Prompt:**

```text
Du bist Opus 4.7. Pre-Flight wie ueblich. Lies alle Stride V2 .docx Dateien (via mcp file-read oder docx-skill).

Aufgabe W-10: Generiere fuer alle 7 Stride V2 Dokumente jeweils einen Stride V3 Prompt, der das Dokument auf den P0f-Stand hebt (Live-Demo-Verweise, gebauter Stack, Zahlen aus 101/101 Tests, etc.).

Ownership (disjunkt):
- Neue Datei `Stride V3/Anschreiben_Aroob_an_Rohde_v3_PROMPT.md` (siehe W-09 — falls schon erledigt, ueberspringen)
- Neue Datei `Stride V3/KI_Tools_Marktanalyse_v3_PROMPT.md` (Floy-Update — pruefen ob neue Tools seit April 2026 dazukamen)
- Neue Datei `Stride V3/Carotis_AI_Konzept_v3_PROMPT.md` (Konzept aktualisieren, Live-Demo-Verweise einsetzen)
- Neue Datei `Stride V3/Expose_Carotis_AI_Rohde_v3_PROMPT.md` (Expose mit Phase-Status P0e DONE)
- Neue Datei `Stride V3/Tech_Description_Klinikum_v3_PROMPT.md` (technische Beschreibung mit echtem Stack-Snapshot)
- Neue Datei `Stride V3/Value_Proposition_Klinikum_v3_PROMPT.md` (Value Prop mit Live-Demo-Verweis)
- Neue Datei `Stride V3/Carotis_Ai_Rohde_v3_PROMPT.md` (Pitch-Deck v3 — neue Folien: Live-Demo-Screenshot, Phase-Status, Test-Coverage)

Berührt NICHT: keine .docx-Datei direkt.

Pro Stride-Prompt-File einheitliche Struktur:
- Quelle (alter Pfad)
- Output-Pfad (Stride V3)
- Aufgabe (3-7 Schritte)
- Tonregeln-Verweis auf CLAUDE.md
- Konkrete Such-und-Ersetz-Anweisungen mit Vorher/Nachher-Snippets
- Vor-Versand-Checks

DoD:
- 7 Stride-V3-Prompt-Files in `Stride V3/`
- Lou kann jeweils per Copy-Paste den Inhalt in Stride starten
- Keine .docx-Datei wurde direkt veraendert (HARD RULE)

Run-Log: `memory/runs/2026-04-30_opus_W-10.md`.
```

---

## WELLE E — Pre-Send-Hardening (Tag 6-7)

### W-11 — Demo-Stresstest + Pre-Send-Smoke (Codex GPT-5.5)

**Prompt:**

```text
Du bist Codex GPT-5.5. Pre-Flight wie ueblich.

Aufgabe W-11: End-to-End-Smoke-Test der Demo-Pipeline genau so, wie Rohde sie laufen wuerde.

Ownership (disjunkt):
- Neue Datei `code/tests/test_rohde_walkthrough_e2e.py` (pytest, bestehende Suite gruen halten)
- Neue Datei `code/scripts/k6_rohde_load.js` (k6-Load-Test fuer 1 Stunde mit 5 simulierten Rohde-Sessions)
- Neue Datei `deploy/runbook_pre_send.md` (Lou-Checkliste vor Mail-Versand)

Berührt NICHT: irgendwelche Production-Code-Pfade ausser via tests.

E2E-Test-Coverage (test_rohde_walkthrough_e2e.py, 6 Tests):
1. Token-Whoami liefert Label + Quota
2. DICOM-Upload (Demo-Fall 01) liefert Prediction in unter 5 Sekunden
3. AI-Panel-Endpoints liefern HiResCAM-Heatmap + Trust-Score
4. Decision-Tree-Capture-POST liefert 201 mit Audit-ID
5. Audit-Trail-GET (mit Admin-Key, der NICHT Rohdes Token ist) zeigt Demo-Token-Label
6. Token nach 500 Requests blockiert

k6-Load-Test:
- 5 Virtual Users
- 1 Stunde Dauer
- Jeder VU: Walkthrough-Sequence + 5 Inferences + 5 Decision-Trees
- Pruefe: P95-Latenz < 5s, 0 Errors, Memory < 1GB

Pre-Send-Runbook (deploy/runbook_pre_send.md):
1. `make demo` lokal lauffaehig
2. `pytest -p no:warnings` 101 + 6 (W-02) + 5 (W-06) + 6 (W-11) = 118 passed
3. `npm test -- --run` 12 + 4 (W-03) + 3 (W-04) = 19 passed
4. `npm run build` SUCCESS
5. Webseite (W-01) deployed und Lighthouse >= 90/95
6. Demo-App (W-02) deployed, Health-Check 200 unter `https://app.carotis.diggai.de/health/`
7. Token via W-06 generiert, in Mail v3 + Anleitung v1 eingesetzt
8. Walkthrough-Video aufgenommen oder Zeile aus Mail entfernt
9. 3 Termin-Optionen in Mail eingetragen
10. Stride V3 alle Office-Docs gerendert + PDFs exportiert
11. Rohde-Anleitung v1 PDF Anlage
12. Aroob CC nicht vergessen
13. Lou und Aroob 5-Minuten-Review der Mail
14. Send

DoD:
- Alle 118 pytest gruen, alle 19 Vitest gruen, Build SUCCESS
- k6-Run mit 0 Errors
- Runbook checkbar (Markdown-Checkboxen)

Run-Log: `memory/runs/2026-04-30_codex_W-11.md`.
```

---

### W-12 — Mail rausschicken (Lou — human task)

```text
Lou-Aufgabe (kein Modell):

1. Runbook (W-11 Output) durchgehen, alle 14 Punkte gruen.
2. Mail v3 in Stride finalisiert (W-09).
3. Stride V3 Office-Docs gerendert (W-10), als PDFs in Anlage.
4. Rohde-Anleitung v1 PDF mit eingesetztem Token (W-06 + W-07 Stride-Schritt).
5. Optional Walkthrough-Video aufgenommen (W-08).
6. Mail von Aroobs Klinikum-Adresse versenden, Aroob als Hauptabsender, Lou im CC.
7. tasks.jsonl: T-001..T-009 auf done.
8. Run-Log `memory/runs/<datum>_lou_T-009_mail_sent.md` mit:
   - Versand-Datum
   - Mail-Inhalt-Snapshot
   - Rohde-Antwort-Erwartungs-Datum (+14 Tage)
   - 14-Tage-Reminder im Kalender
9. Wenn Antwort kommt: Reply-Kit aus runs/2026-04-30_t012_rohde_reply_kit.md aktivieren (T-012).
```

---

## Routing & Tooling Cheat Sheet

| Welle | Modell | Begruendung |
|-------|--------|-------------|
| W-01, W-03, W-04, W-05 | Kimi K2.6 | Boilerplate + UI-Code, Output-Token-schonend, parallel ausfuehrbar |
| W-02, W-06, W-11 | Codex GPT-5.5 | Infra/Backend/Auth/Tests, deeperes System-Verstaendnis noetig |
| W-07, W-08 | Sonnet 4.6 | Stakeholder-Texte mit nuanciertem Ton |
| W-09, W-10 | Opus 4.7 | Stride-V3-Generierung mit politisch sensibler Tonality |
| W-12 | Lou | Human-Final-Step |

## Pre-Flight (jede Welle, nicht verhandelbar)

```bash
cat CLAUDE.md
cat MEMORY.md
ls -t memory/runs/ | head -3
grep -rE "<welle-keyword>" memory/runs/ || true
ls memory/anomalies/
```

Bei Code-Aenderungen: lies AGENTS.md komplett. Bei Office-Docs: nur Stride-Prompts.

## DoD-Format pro Welle (immer dasselbe)

- Files in disjunkter Ownership erstellt/editiert
- Tests gruen (pytest + Vitest)
- Lint/Typecheck/Build 0
- Run-Log geschrieben unter `memory/runs/<datum>_<modell>_<welle>.md`
- MEMORY.md Pointer aktualisiert
- tasks.jsonl Status aktualisiert wo zutreffend

## Anti-Pattern (immer vermeiden)

- Office-Doc direkt editieren
- Patientendaten in Cloud (Demo-Webseite und Demo-App = synthetische Daten only)
- Modell-Inferenz mit echtem PVS verbinden bevor Rohde Go gibt
- Zwei Wellen mit ueberlappenden File-Ownerschaften gleichzeitig fahren
- Test-Coverage senken
- "revolutionaer / bahnbrechend / weltweit erste" in jeglichem Text

---

## Nach P0f

**Wenn Rohde positiv antwortet:** Aktiviere `06_ROHDE_MEETING_KIT.md` Sektion 4-8. Live-Termin in 30 Min mit Demo. P1 (Ethik + Datenvertrag + DSGVO) startet sofort.

**Wenn Rohde Bedenken hat:** Reply-Kit Szenario B oder C aus `runs/2026-04-30_t012_rohde_reply_kit.md`.

**Wenn Rohde Nein sagt:** Reply-Kit Szenario D + Plan B (Tolg / van Stevendaal / Margaritoff).

**Wenn Rohde 14 Tage nicht antwortet:** Status-Update-Mail (Reply-Kit Szenario C-Anpassung), kein Druck.

---

*Erstellt: 2026-04-30 · Modell: Opus 4.7 · Plan-Run: `memory/runs/2026-04-30_opus47_p0f_pivot_plan.md` · Status: ready-to-execute*
