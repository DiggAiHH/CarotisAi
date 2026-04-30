---
name: kimi_adaptation
description: 09b_KIMI_PROMPT_SEQUENCE.md erstellt — Kimi-K2.6-Variante mit Bundling und Session-Setup-First-Pattern. Lessons Learned aus P-01 Copilot eingebaut.
type: run
last_updated: 2026-04-28
---

# Session 2026-04-28 (afternoon) · Opus 4.7 (Cowork) · Kimi K2.6 Adaptation

## Goal

Lou hat P-01 mit Copilot abgeschlossen (`code/.github/copilot-instructions.md`, 76 Zeilen, UTF-8 OK). Hat 61 % seiner Wochen-Quota verbraucht. Wechselt für die nächsten Stages auf Kimi K2.6 (Moonshot AI) — riesiger Kontext (256k), günstiger.

Aufgabe: 09_COPILOT_PROMPT_SEQUENCE.md auf Kimi adaptieren. Constraints:
- Kein `@workspace`, keine Auto-Load-Files
- Kein File-System-Zugriff (Kimi outputs Text, Lou pastet)
- Keine Verify-Commands automatisch
- Aber: 256k Kontext-Window → Bundling möglich

Plus: Lessons Learned aus P-01 einbauen (Line-Count-DoDs sind Müll, PowerShell-Codepage-Encoding-Trap, Verify zu Windows-zentriert).

## Done

- `09b_KIMI_PROMPT_SEQUENCE.md` neu erstellt:
  - **Schritt 0 (Session-Setup):** ~700-Wörter-Block den Lou einmal pastet, primt Kimi mit Carotis-AI-Kontext (Stack, Hard Rules, Verzeichnisstruktur, Hermes/Ollama, Jake van Clief, Decision-Tree-Harvesting)
  - **K-01 bis K-16:** 16 Prompts statt 29 bei Copilot. Bundling-Strategie:
    - K-01 = P-01 (Refresh, optional wenn schon OK)
    - K-02 = Stage B bundled (4 Memory-Files in 1 Prompt)
    - K-03 = Stage C bundled (4 Infra-Files in 1 Prompt)
    - K-04 bis K-08 = Backend (5 separate, weil je eigene Tests)
    - K-09 = Stage E bundled (5 Frontend-Files in 1 Prompt)
    - K-10 bis K-14 = ML Pipeline (5 separate, weil große Files)
    - K-15 = Stage G bundled (8 Test+CI-Files in 1 Prompt)
    - K-16 = Stage H bundled (5 Hermes-Integration-Files in 1 Prompt)
- **Lessons-Learned-Fix:**
  - Line-Count-DoDs ersetzt durch funktionale Checks ("Sektionen vorhanden", "Pfade auflösbar", "Tests grün")
  - PowerShell-Codepage-Trap explizit im Setup-Block erklärt: VS Code reads UTF-8 nativ
  - Verify-Steps stehen für Lou (manuell), nicht für Kimi
- MEMORY.md Index aktualisiert (Pointer auf 09b)
- Token-Saver-Tipps für Kimi am Ende des Files

## Surprised by

- Kimi's 256k-Kontext ist 4-8× größer als Copilot Chat. Damit ist Bundling kein Risiko — Kontext-Verlust passiert nicht.
- Lou's Copilot-Quota ist nach 1 echtem Prompt + ein paar Terminal-Commands schon bei 61 %. Das ist mehr als erwartet — vermutlich rechnet GitHub die `@workspace`-Context-Loads heftig mit. Bei Kimi wird das nicht passieren, weil der Kontext einmal vorne dran hängt und nicht jedem Call neu beigeladen wird.
- Eigentlich hätte ich von Anfang an mit Kimi-Bundling planen sollen. Lehre für die Zukunft: bei Hochkontextfähigen Modellen Bundling als Default, nicht Per-File-Prompts.

## Avoided

- Nicht versucht, das Original-09 zu rewriten — der ist für Lou's späteres Copilot-Recovery (wenn Quota zurück ist) noch nützlich. Stattdessen 09b als Sibling.
- Nicht jeden einzelnen Copilot-Prompt 1:1 übernommen — wo Bundling sinnvoll war, gebündelt. Wo nicht (große ML-Files mit eigenen Tests), separat gelassen.
- Keine Promises gemacht über Kimi-Output-Qualität bei deutscher Sprache — Setup-Block sagt "deutsche Kommentare in Skripten OK, Code-Symbole englisch", aber Lou muss visuell prüfen.

## Next

**Lou's nächster konkreter Schritt:**
1. Kimi öffnen (`https://kimi.moonshot.cn/` oder `https://www.kimi.com/`)
2. Setup-Block aus `09b_KIMI_PROMPT_SEQUENCE.md` Schritt 0 pasten
3. Warten auf "Verstanden, ich kenne Carotis-AI..." Antwort
4. K-02 als ersten echten Prompt pasten (K-01 ist optional, weil P-01 schon Copilot-Output OK ist)
5. Weiter K-03, K-04, ... in der Sequence
6. Pro Prompt: 5-Zeilen-Run-Log in `memory/runs/2026-04-28_kimi_K-NN.md`

**Wenn Kimi für einen Prompt nicht reicht (z.B. Halluzination, falscher Stack):**
- Korrektur-Prompt: "Korrektur in FILE X: <was war falsch>"
- NICHT den ganzen Prompt nochmal — kostet Tokens

**Wenn Kimi-Quota / Account-Limit auch trifft:**
- Fallback auf direkten Anthropic API mit Sonnet 4.6 für die letzten Prompts
- Oder: warten bis Copilot-Quota am 4. Mai resettet

**Nach K-16:** End-to-End-Verifikation laufen lassen (curl health, pytest), dann zurück zu RUNBOOK_TODAY.md (Mail an Rohde).

## Memory updates

- `MEMORY.md` → Pointer auf 09b ergänzt
- `memory/runs/2026-04-28_opus47_kimi_adaptation.md` neu (diese Datei)

## Hinweise an die nächste Session

1. **Wenn Lou sagt "Kimi-Output zerlegt FILE X":** Schau im 09b nach Token-Saver-Tipp 3 ("Korrektur in FILE X: <bug>"). Niemals den ganzen Prompt nochmal pasten lassen.
2. **Wenn Lou sagt "Kimi versteht den Setup-Block nicht":** Setup-Block kürzen oder in 2 Teile splitten (erst Stack + Rules, dann Verzeichnis + Conventions). Aber zuerst prüfen ob Kimi tatsächlich nicht antwortet — manchmal antwortet er knapp und das ist OK.
3. **Wenn 09 (Copilot) und 09b (Kimi) divergent werden:** wir haben jetzt 2 parallele Prompt-Sets. Das ist in Ordnung — sie addressieren verschiedene Modelle. Nicht versuchen zu konsolidieren.
4. **Replicabilität:** Wenn ein anderes Projekt nach Carotis-AI kommt, ist die Vorlage:
   - Setup-Block mit Stack + Hard Rules + Verzeichnisstruktur
   - K-01 = onboarding doc
   - K-02 = bundled memory
   - K-03 = bundled infra
   - K-04..N = backend modules
   - K-N+1 = bundled frontend
   - K-N+2..M = ML or domain-specific modules
   - K-M+1 = bundled tests
   - K-M+2 = bundled deployment

   Nur die Hard Rules und Domain-Module ändern sich. Das ist der wiederverwendbare Engineering-Harness-Pattern.
