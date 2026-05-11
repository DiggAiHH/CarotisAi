# Remotion Skill-Harness fuer Carotis-AI

## Zweck

Operativer Harness-Input fuer ein lokales Remotion-Video im Carotis-AI-Projekt. Ziel ist ein kurzes, reproduzierbares Rohde-Demo-Video, das die P0f-Demo erklaert, ohne Patientendaten, Cloud-Assets oder fragile Browser/CSS-Animationen zu verwenden.

Grundlage: frisch installierter Skill `remotion-best-practices`, gelesen am 2026-05-02. Diese Datei ist Planungsinput, kein Projekt-Scaffold und keine Installationsanweisung.

## 10 Remotion-Aufgaben fuer Carotis-AI

| Nr. | Aufgabe | Status | Ergebnis / Artefakt |
|---:|---|---|---|
| 1 | Rohde-Demo-Video als 3-Minuten-Komposition planen. | `executed-as-plan` | Artefakt: 180 Sekunden Narrative mit klinischem Einstieg, Local-First-Architektur, XAI-Demo, Decision-Tree-Harvesting und Call-to-Action. |
| 2 | 30fps als verbindliche Timing-Basis setzen. | `executed-as-plan` | Artefakt: 180s x 30fps = 5400 Frames; alle Szenen werden in Frames geplant, nicht in CSS-Zeitangaben. |
| 3 | Sequence-Plan fuer alle Szenen definieren. | `executed-as-plan` | Artefakt: Szenen-Tabelle mit `from` und `durationInFrames`; jede Szene ist als Remotion-`Sequence` denkbar. |
| 4 | CSS-Animations und Tailwind-Animation-Klassen ausschliessen. | `executed-as-plan` | Artefakt: Animationsregel: nur `useCurrentFrame()`, `interpolate()`, `Easing` oder Remotion-konforme Timing-Utilities. |
| 5 | Asset-Regel fuer Demo-Medien festlegen. | `executed-as-plan` | Artefakt: alle Logos, Screenshots, synthetischen DICOM-Frames, Audio und Untertitel liegen lokal unter `public/` und werden via `staticFile()` referenziert. |
| 6 | One-frame-render-check als Harness-Gate aufnehmen. | `executed-as-plan` | Artefakt: Pruefpunkt fuer Frame 30 bei 30fps als Ein-Sekunden-Sanity-Check fuer Layout, Farben, Textueberlauf und sichtbare Assets. |
| 7 | Captions lokal und JSON-basiert planen. | `executed-as-plan` | Artefakt: Untertitelmodell nutzt Remotion-`Caption`-Struktur mit `text`, `startMs`, `endMs`, `timestampMs`, `confidence`; keine Cloud-Transkription fuer Projektdaten. |
| 8 | Audio-Spur lokal planen. | `executed-as-plan` | Artefakt: Voiceover oder Musik liegt lokal in `public/audio/`; Einbindung konzeptionell ueber `<Audio>` aus `@remotion/media`, Lautstaerke/Fades framebasiert. |
| 9 | Local-only Datenschutz fuer Video-Produktion fixieren. | `executed-as-plan` | Artefakt: nur synthetische Demo-Daten, anonymisierte UI-Screenshots und lokale Assets; keine echten Patientendaten, keine Remote-URLs, keine externe TTS/API. |
| 10 | Rohde-spezifischen Review-Output definieren. | `executed-as-plan` | Artefakt: finales Video soll als Meeting-Asset dienen: klare klinische Frage, nachvollziehbare KI-Begruendung, lokale Deploybarkeit, naechster Schritt Rohde-Go. |

## Preflight-Integration

- Vor jeder Remotion-Arbeit `remotion-best-practices/SKILL.md` lesen; bei Captions zusaetzlich `rules/subtitles.md`, bei Audio `rules/audio.md`.
- Fuer Carotis-AI immer 30fps explizit planen; Sekundenangaben in Frames umrechnen und in der Szenen-Tabelle dokumentieren.
- Vor Render/Export pruefen: alle Medien lokal unter `public/`, alle Demo-Daten synthetisch oder anonymisiert, keine Remote-Asset-URLs.
- Einen One-frame-render-check als Minimalgate vorm langen Render vorsehen, bevorzugt Frame 30 und spaeter je ein Keyframe pro Hauptszene.
- Keine Projektdateien ausserhalb des aktuell freigegebenen Write-Sets anfassen; Remotion-Planung darf Harness-Input bleiben, bis ein eigener Implementierungsauftrag existiert.

## Anti-Patterns

- CSS `transition`, CSS `animation` oder Tailwind-`animate-*` fuer Timing verwenden.
- Assets aus Cloud-URLs, Screenshots mit Patientendaten oder externe TTS/API in die Rohde-Demo aufnehmen.
- Sequenzen nur narrativ in Sekunden beschreiben, ohne `from`/`durationInFrames`-Plan.
- Captions als lose SRT/Textdatei ohne JSON-`Caption`-Normalisierung behandeln.
- Ein 3-Minuten-Video direkt komplett rendern, ohne vorher Frame-Checks fuer Layout, Textueberlauf und Asset-Aufloesung zu machen.

## Kompositionsskizze: 3-Minuten-Rohde-Video

Rahmen:
- `fps`: 30
- `durationInFrames`: 5400
- Format: 16:9, Meeting-/Mail-tauglich
- Daten: ausschliesslich synthetische Demo-DICOMs, anonymisierte Screenshots, lokale Audio-/Caption-Dateien

| Zeit | Frames | Sequence-Inhalt | Zweck |
|---|---:|---|---|
| 00:00-00:12 | 0-359 | Titel: Carotis-AI, lokale CTA-Auswertung, Klinikum-Dortmund-Kontext. | Sofort klar machen, worum Rohde gebeten wird. |
| 00:12-00:30 | 360-899 | Klinisches Problem: Stenosegrad, Plaque-Vulnerability, Erklaerbarkeit, Datenschutz. | Bedarf verdichten, ohne Marketington. |
| 00:30-00:52 | 900-1559 | Local-First-Architektur: Edge-Backend, SQLite-Audit, ONNX Runtime lokal, keine Cloud-Inferenz. | Datenschutz- und Deploy-Vertrauen aufbauen. |
| 00:52-01:22 | 1560-2459 | Demo-UI: Patient-List, DICOM-Viewer, AI Panel, synthetischer Fall. | Zeigen, dass ein nutzbarer Workflow existiert. |
| 01:22-01:52 | 2460-3359 | Grad-CAM/SHAP-Erklaerung: Heatmap, Confidence, Trust Score, Unsicherheitswarnung. | XAI-Nutzen fuer klinische Bewertung darstellen. |
| 01:52-02:22 | 3360-4259 | Decision-Tree-Harvesting: Aerztliche Begruendung, Override, Disagreement-Audit. | Wissenschaftliche Differenzierung zeigen. |
| 02:22-02:44 | 4260-4919 | Forschungsplan: P1 Ethik/DSGVO, P2 retrospektive Daten, P3 Training, P5 Validierung. | Rohde sieht realistische Phasen statt Tool-Demo. |
| 02:44-03:00 | 4920-5399 | Schluss: konkrete Bitte um Go, Datenzugangsklaerung und Betreuungsgespraech. | Naechste Entscheidung klar formulieren. |

Render-Hinweise fuer spaetere Umsetzung:
- Animationen framebasiert planen: Fade/Slide/Reveal ueber `useCurrentFrame()` und `interpolate()`.
- Captions pro Szene in JSON halten und anhand `startMs`/`endMs` synchronisieren.
- Voiceover lokal aufnehmen oder lokal generieren; Lautstaerke und Fades framebasiert steuern.
- Vor Finalrender pruefen: Frame 30, 900, 1560, 2460, 3360, 4920.
