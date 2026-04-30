# Hermes + Browser Harness — Knowledge Harnessing Workflow

## Übersicht

Der Knowledge Harnessing Prozess verbindet die lokale KI-Inferenz (Carotis-AI) mit der Wissensakquise aus vertrauenswürdigen medizinischen Quellen. Ärzte erhalten nicht nur eine KI-Vorhersage, sondern können diese mit aktueller Literatur und Leitlinien hinterlegen — alles innerhalb des Local-First-Edge-Systems.

```
┌─────────────┐    ┌─────────────┐    ┌─────────────────┐    ┌──────────────┐
│ DICOM Upload│ →  │ AI Inference│ →  │ Doctor Review   │ →  │ Knowledge    │
│ (anonymized)│    │ (MFSD-UNet) │    │ + Grad-CAM      │    │ Capture      │
└─────────────┘    └─────────────┘    └─────────────────┘    └──────────────┘
                                                                    │
                                                                    ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────────┐    ┌──────────────┐
│ Pattern     │ ←  │ Weekly      │ ←  │ Decision Trees  │ ←  │ Browser      │
│ Mining      │    │ Report      │    │ (JSON Schema)   │    │ Research     │
└─────────────┘    └─────────────┘    └─────────────────┘    └──────────────┘
```

---

## Schritt-für-Schritt für Ärzte

### Schritt 1: DICOM-Upload & Anonymisierung
1. Arzt lädt CTA-DICOM-Serie in die Carotis-AI Web-Oberfläche
2. System prüft Anonymisierung (PS 3.15 Basic Application Level Confidentiality Profile)
3. Bei fehlender Anonymisierung: `anonymize-batch` Skill wird automatisch vorgeschlagen
4. DICOM wird im temporären Verzeichnis (`data/dicom_temp/`) gehalten, niemals persistiert

### Schritt 2: KI-Review
1. System führt ONNX-Inferenz durch (lokal, keine Cloud)
2. Ergebnisse werden angezeigt:
   - Stenose-Grad (%) mit Konfidenzintervall
   - Plaque-Vulnerability-Score
   - Grad-CAM Heatmap über dem Originalbild
   - Trust-Score (1–5, basierend auf Trainingsdaten-Ähnlichkeit)
3. Arzt prüft visuell und bewertet Plausibilität

### Schritt 3: Knowledge Capture
1. Arzt klickt **„Capture Decision"**
2. `doctor-knowledge-capture` Skill wird aktiviert
3. Arzt beantwortet strukturierte Fragen:
   - Stimmen Sie der KI-Einschätzung zu? (Ja/Nein/Teilweise)
   - Welche Begründung haben Sie? (Freitext)
   - Vertrauen Sie der Vorhersage? (1–5 Skala)
   - Welche zusätzlichen Informationen wären hilfreich gewesen?

#### Browser-Enhancement (optional)
Wenn der Arzt sagt: **„Recherchiere das"** oder **„PubMed"**
1. `browser-harness` Skill wird aktiviert
2. Playwright MCP öffnet Browser im Hintergrund
3. Abfrage erfolgt gegen erlaubte Quellen:
   - **PubMed:** `carotid stenosis plaque vulnerability`
   - **Radiopaedia:** `carotid artery stenosis`
   - **ESC Knowledge:** `carotid atherosclerosis guidelines`
4. Top-3 Ergebnisse werden extrahiert und als JSON gespeichert
5. Arzt kann relevante Ergebnisse mit einem Klick in den Decision Tree übernehmen

### Schritt 4: Decision Tree Speicherung
1. Alle Eingaben des Arztes werden im Decision Tree JSON Schema (`schemas/decision_tree.schema.json`) validiert
2. Gespeichert in SQLite (`DecisionTreeLog` Tabelle)
3. SHA-256-Hash der DICOM-Datei wird referenziert (nicht die Datei selbst)
4. Audit-Trail wird geschrieben (append-only, immutable)

---

## Browser-Recherche in Decision Trees

Die Rechercheergebnisse fließen als `references`-Array in den Decision Tree ein:

```json
{
  "decision_id": "dt-2026-04-29-001",
  "dicom_hash": "sha256:abc123...",
  "ai_prediction": {
    "stenosis_percent": 72.5,
    "vulnerability_score": 0.84,
    "confidence": 0.91
  },
  "doctor_feedback": {
    "agreement": "partial",
    "trust_score": 4,
    "reasoning": "Stenosegrad scheint etwas überschätzt, Plaque-Morphologie stimmt"
  },
  "references": [
    {
      "source": "pubmed",
      "title": "Plaque vulnerability predicts stroke risk in carotid stenosis",
      "authors": "Smith et al.",
      "year": 2024,
      "snippet": "High-risk plaque features were associated with...",
      "relevance": 0.93,
      "url": "https://pubmed.ncbi.nlm.nih.gov/..."
    }
  ],
  "captured_at": "2026-04-29T14:30:00Z"
}
```

### Regeln für Referenzen
- Maximal 3 Referenzen pro Decision Tree (um Überladung zu vermeiden)
- Nur Abstracts/Snippets, keine Volltext-Downloads
- URLs werden auf erlaubte Domains beschränkt
- Patientendaten dürfen niemals in die Suchanfrage eingegeben werden

---

## Wöchentliche Pattern-Mining Reports

Jeden Sonntag um 23:00 Uhr:

1. `decision-pattern-miner` Skill wird automatisch gestartet
2. Analysiert alle Decision Trees der letzten 7 Tage
3. Generiert Report:
   - Häufige Abweichungen zwischen KI und Arzt
   - Durchschnittliche Trust-Scores pro Stenose-Intervall
   - Meist-zitierte Quellen aus Browser-Recherchen
   - Vorschläge für Schema-Erweiterungen
4. Report wird gespeichert in `memory/domain/research/weekly_patterns_YYYY-WXX.md`
5. Optional: E-Mail-Benachrichtigung an Admin (nur Metadaten, keine Patientendaten)

### Beispiel-Report-Ausschnitt
```markdown
## Wöchentlicher Pattern Report (KW 17/2026)

### Statistiken
- Entscheidungen erfasst: 34
- Durchschnittlicher Trust-Score: 3.8/5
- Browser-Recherchen ausgelöst: 12 (35 %)

### Top-Abweichungen
- Stenose >70 %: Ärzte tendieren zur Unterschätzung um 5–8 %
- Plaque-Vulnerability: Bei calcifizierten Plaques höhere Übereinstimmung

### Meist-zitierte Quellen
1. PubMed — "ESC Guidelines for carotid artery disease" (2024)
2. Radiopaedia — "Carotid artery stenosis grading" (Case #2847)

### Schema-Vorschläge
- Neues Feld: `plaque_composition` (enum: calcified, lipid-rich, mixed)
- Neues Feld: `symptomatic_status` (boolean)
```

---

## Trust-Score Monitoring

Der Trust-Score (1–5) ist ein zentraler Indikator für die Akzeptanz des Systems.

### Berechnung
- **1–2:** Starke Ablehnung — KI und Arzt widersprechen sich deutlich
- **3:** Neutral — Teilweise Übereinstimmung oder Unsicherheit
- **4–5:** Starke Zustimmung — KI-Vorhersage wird bestätigt

### Monitoring über Zeit
- `trust-calibration-monitor` Skill trackt Trends
- Bei durchschnittlichem Trust-Score < 3 über 2 Wochen: Alert an Entwickler
- Dashboard-Widget zeigt Trust-Score-Verteilung in Echtzeit

### Maßnahmen bei niedrigem Trust-Score
1. Prüfung der Trainingsdaten-Qualität
2. Review der meist-abgelehnten Vorhersagen
3. Ergänzung neuer Fälle ins Training-Set
4. Optional: `nightly-retrain` Skill anstoßen (bei ausreichend neuen Daten)

---

## Compliance & Sicherheit

| Aspekt | Maßnahme |
|--------|----------|
| Datenverbleib | Alle Prozesse lokal (Edge AI + lokaler Browser) |
| Patientendaten | Keine Eingabe in Browser-Suchanfragen |
| DICOM | In-memory Anonymisierung vor Verarbeitung |
| Audit | Append-only SQLite, SHA-256-Hashes, keine PII |
| Browser-Cache | 24h TTL, dann automatische Löschung |
| Volltext-Downloads | Verboten — nur Abstracts/Snippets erlaubt |

---

## Dateien & Konfiguration

| Datei | Zweck |
|-------|-------|
| `code/hermes/skills/browser-harness.md` | Skill-Definition für Browser-Recherche |
| `code/hermes/settings/knowledge_harness.json` | Konfiguration des gesamten Harness |
| `code/hermes/skills/doctor-knowledge-capture.md` | Skill für ärztliche Entscheidungserfassung |
| `code/hermes/skills/decision-pattern-miner.md` | Wöchentliche Pattern-Analyse |
| `code/hermes/skills/trust-calibration-monitor.md` | Trust-Score Tracking |
| `schemas/decision_tree.schema.json` | JSON-Schema für validierte Decision Trees |
| `memory/domain/research/` | Speicherort für Recherche-Ergebnisse |

---

*Letztes Update: 2026-04-29 · Erstellt für P0 (Rohde-Meeting-Vorbereitung)*
