# Rohde-Demo Testdaten

Stand: 2026-05-02

## Zweck

Diese Dateien sind synthetische CTA/DICOM-Demodaten fuer den Online-Test vor dem Versand an Prof. Rohde. Sie enthalten keine echten Patientendaten und wurden lokal ueber `code/scripts/generate_demo_data.py` erzeugt.

## Online-Testdaten

| Fall | Demo-Name | Online-Datei | Erwarteter Demo-Befund |
|---|---|---|---|
| 1 | A. Schmidt | `https://api.carotis.diggai.de/demo/dicoms/case_001.dcm` | moderate Stenose, weiche Plaque |
| 2 | M. Mueller | `https://api.carotis.diggai.de/demo/dicoms/case_002.dcm` | hochgradige rechtsseitige ICA-Stenose, Heatmap-Fokus |
| 3 | K. Weber | `https://api.carotis.diggai.de/demo/dicoms/case_003.dcm` | Grenzfall nahe OP-Schwelle |
| 4 | J. Fischer | `https://api.carotis.diggai.de/demo/dicoms/case_004.dcm` | niedriggradiger Fall mit Artefakt-/Motion-Hinweis |

## Lokaler Pfad

```text
code/frontend/public/demo/dicoms/
```

## Testablauf vor Versand

1. `https://api.carotis.diggai.de/` oeffnen.
2. Demo-Token eingeben.
3. Pruefen, ob sofort die Claude-Design-nahe 3-Spalten-Demo sichtbar ist: Patients, Viewer, AI.
4. Links einen synthetischen Fall auswaehlen.
5. Im Viewer Heatmap toggeln.
6. Rechts AI-Gauge, Confidence, Vulnerability Marker, SHAP und Trust Score pruefen.
7. `Download selected DICOM` klicken und die Datei erneut ueber `Datei auswaehlen` hochladen.
8. Nach Upload muss der echte Backend-Inferenzpfad laufen und das AI-Panel aktualisieren.

## Sicherheit

- Keine echten Patientendaten.
- Keine Rohdaten aus Klinik/Praxis.
- Nur synthetische Pixelwerte und leere DICOM-PII-Felder.
- Demo ist nicht fuer klinische Entscheidungen bestimmt.
