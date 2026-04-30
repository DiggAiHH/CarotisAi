# ADR-0007: Reasoning-Alignment-Loss fuer Decision-Tree-Harvesting

## Kontext

Das Decision-Tree-Harvesting erfasst die Begründung des Arztes (deciding_feature, ruled_out, etc.).
Die aktuelle Trainingspipeline optimiert Stenose-Regression und Klassifikation, lernt aber nicht explizit,
*warum* ein Arzt eine bestimmte Entscheidung getroffen hat. Dies führt zu einem Reasoning-Alignment-Loss:
das Modell kann korrekt klassifizieren, ohne die gleichen visuellen Merkmale wie der Arzt zu nutzen.

## Entscheidung

Wir führen einen **Multi-Task-Head** `deciding_feature` ein, der parallel zur Stenose-Regression trainiert wird:

- **Input**: Letzte UNet-Feature-Maps (vor dem finalen Conv)
- **Head**: GAP + FC(256) + Dropout(0.3) + FC(|F|) wobei |F| die Anzahl der dokumentierten deciding_features ist
- **Loss**: `L_total = L_stenosis + alpha * L_feature + beta * L_cam_mask`
  - `L_feature`: CrossEntropy zwischen vorhergesagtem und erfasstem deciding_feature
  - `L_cam_mask`: MSE zwischen HiResCAM/GradCAM-Maske und einer vom Arzt annotierten ROI (falls vorhanden)

## Konsequenzen

- **Positiv**: Modell lernt, auf die gleichen Regionen zu achten wie der Arzt → bessere Erklärbarkeit.
- **Positiv**: Reasoning-Head kann für XAI-Validierung genutzt werden ("Hat das Modell dieselbe Begründung?").
- **Negativ**: Erhöhte Modellkomplexität; |F| muss vorab festgelegt werden (aktuell 4 Klassen + "other").
- **Negativ**: Annotation von ROI-Masken ist aufwendig und nur in der P2-Phase verfügbar.

## Alternativen

| Alternative | Nachteil |
|-------------|----------|
| Post-hoc Attention-Alignment (KL-Divergenz zwischen Arzt-Heatmap und GradCAM) | Erfordert pixelgenaue Annotationen, nicht skalierbar |
| Contrastive Learning mit Agreement/Disagreement-Paaren | Datenhungrig, P0-Datensatz zu klein |
| Reinforcement Learning from Human Feedback (RLHF) | Overkill für Edge-Deployment, Rechenintensiv |
| Keine Änderung (Status Quo) | Reasoning-Alignment-Loss bleibt unadressiert |

## Risiken

1. **Overfitting auf deciding_feature**: Wenn |F| zu klein ist, dominiert eine Klasse.
   - *Mitigation*: Gewichteter Loss; Klasse "other" als Catch-All.
2. **Falsche Korrelation**: Modell lernt deciding_feature aus dem Hintergrund statt aus der Plaque.
   - *Mitigation*: HiResCAM-Masken regularisieren den Feature-Head auf die relevante Region.
3. **Regulatorische Akzeptanz**: Ein "zusätzlicher" Head könnte als design change unter MDR gelten.
   - *Mitigation*: Head ist optional und kann zur Laufzeit deaktiviert werden; ONNX-Export enthält nur aktivierte Heads.

## Umsetzung

- **P3**: Prototyp des Multi-Task-Heads in `ml/models/mfsd_unet.py`
- **P4**: Integration von `L_feature` in `ml/training/losses.py`
- **P5**: HiResCAM-Annotation-Tool für ROI-Masken (Frontend)
- **P6**: A/B-Test: Stenose-Genauigkeit mit/without Reasoning-Head

## Compliance

- **MDR Anhang I, 17.1**: Software muss korrekte Ergebnisse liefern; Reasoning-Alignment erhöht die Validierbarkeit.
- **DSGVO Art. 22**: Recht auf Erklärung automatisierter Entscheidungen; Reasoning-Head stützt die Begründung.
- **ISO 13485**: Design-Change → dieser ADR dokumentiert die Entscheidung.
