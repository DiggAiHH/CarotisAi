# ADR-006: Confidence Calibration & Trust Scoring

## Status
Accepted

## Context

Neuronale Netze für die Stenose-Quantifizierung liefern typischerweise über-konfidente Wahrscheinlichkeiten — das Modell gibt 0.95 aus, obwohl die tatsächliche Accuracy bei 0.70 liegt. Im klinischen Kontext führt dies zu **Overtrust**: Ärzte akzeptieren falsche Vorhersagen, weil die Confidence hoch erscheint. Eine Studie (PMC 2025, MIMIC-III, n=6689) zeigt, dass Calibration die Override-Rate von 87.6% auf 33.3% senkt. Für Carotis-AI ist daher eine explizite Confidence-Calibration und ein daraus abgeleiteter Trust-Score essenziell.

## Decision

Wir implementieren einen zweistufigen Ansatz:

1. **ConfidenceCalibrationService** (`backend/app/services/calibration_service.py`)
   - **Platt Scaling**: Logistische Regression auf den Logits (`sklearn.linear_model.LogisticRegression`), geeignet für unimodale Fehler.
   - **Isotonic Regression**: Nicht-parametrisch, monoton steigend (`sklearn.isotonic.IsotonicRegression`), geeignet für komplexere Verteilungen.
   - Auswahl per Config: `calibration_method: str = Field(default="platt", pattern=r"^(platt|isotonic)$")`
   - Kalibrierung wird auf einem Hold-out-Set (20% der Trainingsdaten) gefittet und als `.pkl` persistiert.

2. **TrustScoreService** (`backend/app/services/trust_score_service.py`)
   - Composite-Score aus drei Komponenten:

   | Komponente | Gewicht | Quelle |
   |------------|---------|--------|
   | Calibrated Confidence | 0.50 | `ConfidenceCalibrationService` |
   | Calibration Error (ECE) | 0.30 | Expected Calibration Error, invertiert: `1 - normalized_ece` |
   | Transparency (XAI) | 0.20 | Grad-CAM/HiRes-CAM Coverage-Ratio über der Stenose-ROI |

   - Ausgabe: Integer 1–5, gerundet, wobei 5 = höchstes Vertrauen.
   - Frontend-Display: Ampel-Farbcodierung via Tailwind (`red-500` = 1–2, `amber-400` = 3, `emerald-500` = 4–5).

## Consequences

Positive:
- **Reduzierte Overtrust-Rate** — Ärzte sehen kalibrierte Wahrscheinlichkeiten statt über-optimistischer Raw-Outputs.
- **Transparente Entscheidungsgrundlage** — Der composite Trust-Score kommuniziert Unsicherheit multi-dimensional (nicht nur Confidence).
- **Reversible Architektur** — Beide Services sind injectable Dependencies; Fallback auf Raw-Confidence ist trivial.
- **Regulatorische Relevanz** — Erfüllt DECIDE-AI / TMEA Simplicity Principles für erklärbare Unsicherheitskommunikation.

Negative:
- **Hold-out-Daten erforderlich** — Für Kalibrierung muss ein separater Validierungssatz existieren; reduziert effektives Trainingsvolumen.
- **Drift-Sensitivität** — Platt/Isotonic-Parameter sind statisch; bei Domain-Shift (anderer Scanner, Kontrastmittel-Protokoll) entkoppelt die Calibration. Re-Kalibrierung nötig.
- **Zusätzliche Latenz** — ca. 5–10ms pro Inferenz (sklearn Prediction auf CPU); vernachlässigbar gegenüber ONNX-Runtime.

## Alternatives Considered

1. **Temperature Scaling** — Einfacher als Platt (ein einzelner Skalarparameter), aber nur für Softmax-Outputs geeignet. Unser MFSD-UNet liefert Multi-Task-Outputs (Segmentierung + Regression + Klassifikation), wodurch Temperature Scaling nicht direkt anwendbar ist.
2. **Label Smoothing** — Wird während des Trainings angewendet (ε = 0.1), nicht als Post-Hoc-Calibration. Wir verwenden es bereits im Training, aber es ersetzt keine explizite Kalibrierung.
3. **No Calibration** — Default-Status vor dieser ADR. Abgelehnt, da die Override-Rate in Pilot-Tests zu hoch war (>80%) und die klinische Akzeptanz gefährdet.

## References

- Guo et al., "On calibration of modern neural networks", ICML 2017
- Platt, "Probabilistic outputs for support vector machines", 1999
- PMC 2025 Study: override rate 87.6% → 33.3% with calibration (MIMIC-III, n=6689)
- DECIDE-AI / TMEA Simplicity Principles
