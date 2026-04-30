# ADR-005: HiRes-CAM als Alternative zu Grad-CAM

## Status
Accepted — Phase C (P0c)

## Context

Carotis-AI verwendet **Grad-CAM** zur Visualisierung der vom Modell fokussierten Regionen auf CTA-Bildern. Grad-CAM berechnet Klassen-Aktivierungs-Heatmaps durch globales Mitteln der Gradienten (Global Average Pooling, GAP) über räumliche Dimensionen:

```
weights = gradients.mean(dim=(2, 3))   # GAP
cam = sum(weights * activations)
```

Dies führt zu einer **Glättung** der Heatmap, was bei dünnen Gefäßstrukturen (Carotis-Arterien, < 3mm Durchmesser) problematisch sein kann — die Heatmap überlappt den Gefäßverlauf unscharf.

## Decision

Wir implementieren **HiRes-CAM** als alternative XAI-Methode neben Grad-CAM.

### Mathematischer Unterschied

| Methode | Gewichtungsformel | Auflösung |
|---------|-------------------|-----------|
| **Grad-CAM** | `weights = gradients.mean(dim=(2,3))` | Niedrig (GAP glättet) |
| **HiRes-CAM** | `weights = gradients` (pixelweise) | Hoch (kein GAP) |

HiRes-CAM Formel:
```
cam = sum(gradients * activations, dim=1)   # pixelweise, kein Pooling
```

### Implementation

- `ml/xai/gradcam.py` enthält beide Klassen: `SegGradCAM` und `SegHiResCAM`
- Beide nutzen denselben Hook-Mechanismus (Forward + Backward Hooks)
- API ist identisch: `generate(input_tensor) -> np.ndarray[H, W]`

### Wann welche Methode?

| Szenario | Empfohlene Methode | Begründung |
|----------|-------------------|------------|
| **Standard-Befundung** | Grad-CAM | Robuster, schneller, etabliert |
| **Dünne Gefäße / Stenose** | HiRes-CAM | Schärfer, bessere Lokalisation |
| **Forschung / Publikation** | Beide vergleichen | Methodische Vollständigkeit |

### Default-Entscheidung

**Grad-CAM bleibt Default** in Produktion. HiRes-CAM ist als Option über Config verfügbar:

```python
# config.py
xai_method: str = Field(default="gradcam", pattern=r"^(gradcam|hirescam)$")
```

## Consequences

### Positive
- **Höhere räumliche Auflösung** bei HiRes-CAM — kritisch für dünne Carotis-Arterien
- **Keine neue Dependency** — beide Methoden in derselben Datei
- **Identische API** — Austauschbar ohne Refactoring
- **Forschungsrelevanz** — HiRes-CAM wird in medizinischen XAI-Publikationen bevorzugt

### Negative
- **HiRes-CAM ist rechenintensiver** (kein GAP = mehr Multiplikationen)
- **Kann rauschartefakt erzeugen** bei sehr tiefen Layern
- **Zwei Methoden = doppelter Test-/Wartungsaufwand**

### Risiken
- **Clinician Überraschung** — wenn HiRes-CAM plötzlich schärfere Heatmaps zeigt, könnte das Vertrauen beeinflussen
- **Layer-Abhängigkeit** — beide Methoden sind sensitiv für die Wahl des Target-Layers

## Compliance

- **B-15 (Kein PII in Logs):** Heatmaps enthalten keine Patientendaten
- **Local-First:** Berechnung erfolgt lokal auf Edge-Server
- **Reproduzierbarkeit:** `torch.manual_seed()` in Evaluations-Skript garantiert reproduzierbare Vergleiche

## Alternatives Considered

1. **LayerCAM** — Noch schärfere Auflösung, aber rechenintensiver und instabiler bei tiefen Netzen
2. **EigenCAM** — Ohne Gradienten (nur Activations), schneller aber weniger spezifisch
3. **Nur Grad-CAM beibehalten** — Einfacher, aber wissenschaftlich nicht state-of-the-art

## References

- Selvaraju et al., "Grad-CAM: Visual Explanations from Deep Networks via Gradient-based Localization", ICCV 2017
- Draelos & Carin, "Use HiResCAM instead of Grad-CAM for faithful explanations of convolutional neural networks", Nature Machine Intelligence 2021
- `code/ml/xai/gradcam.py` — Implementation beider Methoden
- `code/ml/xai/evaluate_cam_methods.py` — Vergleichs-Skript
