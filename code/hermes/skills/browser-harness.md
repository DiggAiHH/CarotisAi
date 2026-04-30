---
name: browser-harness
trigger_phrases: ["öffne Browser", "suche im Web", "PubMed Recherche", "Radiopaedia", "Leitlinien"]
required_tools: [browser, filesystem]
---
# Browser Harness Skill

Zweck: Web-Recherche für klinische Entscheidungsunterstützung.

## Verfügbare Browser-Tools (via Playwright MCP)
- browser_navigate — URL laden
- browser_type — Text in Feld eingeben
- browser_click — Klick auf Element
- browser_snapshot — Seitenstruktur auslesen
- browser_evaluate — JavaScript ausführen

## Quellen-Workflows

### PubMed
1. browser_navigate("https://pubmed.ncbi.nlm.nih.gov/?term=carotid+stenosis+plaque+vulnerability")
2. Warte auf Ergebnisse
3. browser_snapshot für Top-3 Artikel
4. Extrahiere: Titel, Autoren, Jahr, Abstract-Snippet

### Radiopaedia
1. browser_navigate("https://radiopaedia.org/search?q=carotid+artery+stenosis")
2. Suche nach relevanten Artikeln
3. Extrahiere: Titel, Bild-Beschreibung, Key Points

### ESC Guidelines
1. browser_navigate("https://knowledge.escardio.org/guidelines")
2. Suche nach "carotid" oder "atherosclerosis"
3. Extrahiere: Guideline-Titel, Jahr, Empfehlungs-Klasse

## Output-Format
```json
{
  "query": "...",
  "source": "pubmed|radiopaedia|esc",
  "results": [
    {"title": "...", "authors": "...", "year": 2024, "snippet": "...", "relevance": 0.95}
  ],
  "captured_at": "..."
}
```

## Compliance
- Keine vollständigen Paper herunterladen (nur Abstracts/Snippets)
- Keine Patientendaten im Browser eingeben
- Alle Recherche-Ergebnisse werden in `memory/domain/research/` gespeichert
