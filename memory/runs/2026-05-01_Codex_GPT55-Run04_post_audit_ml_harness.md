---
name: 2026-05-01_Codex_GPT55-Run04_post_audit_ml_harness
type: run
---
## Goal
Deep-Audit-Nachlauf fuer ML/Backend/Harness: offene Optimierungen aus Run06 gegen aktuelle Quellen pruefen, risikoarme Fixes umsetzen, Wiederholfehler im Harness dokumentieren.

## Done
- Pre-Flight nach AGENTS/ULTRAPLAN ausgefuehrt; letzte Run-Logs und Anomalien gelesen.
- Web-Recherche abgeglichen: MFSD-UNet 2025 bestaetigt W/L-Augmentation + Deep Supervision; ONNX Runtime empfiehlt Quantization, aber nur nach Genauigkeitsvalidierung.
- `InferenceService`: fehlenden `get_settings`-Import gefixt; `enable_inference_tta` als default-off Config-Hook ergaenzt; W/L-TTA batcht drei Fenster und mittelt Outputs, bleibt aber klinisch deaktiviert bis Validierung.
- `onnx_export.py`: unsichere statische INT8-Quantisierung mit random calibration entfernt; Dynamic INT8 opt-in via `_quantize_dynamic_onnx()` ergaenzt; ASCII-only Console-Output im beruehrten Exporter.
- `code/ml/requirements.txt`: `sympy` fuer `onnxruntime.quantization` ergaenzt.
- Tests ergaenzt: TTA-Batch-Shape und Dynamic-Quantization-Smoke.
- `deploy/MCP_SETUP.md`: Post-Audit Harness Lessons dokumentiert.

## Surprised by
- `onnxruntime.quantization` importiert ohne `sympy` nicht; die Dependency war nicht deklariert.
- Der INT8-Zweig aus Run06 referenzierte `sess`, bevor die Session erzeugt wurde, und nutzte synthetische Zufallsdaten fuer statische Quantisierung. Das waere fuer medizinische Segmentierung methodisch falsch.

## Avoided
- Keine Cloud-Inferenz, keine Patientendaten, keine externen Daten-Uploads.
- Keine Architektur-Aenderung an MFSD-UNet und keine klinisch aktive TTA/INT8-Nutzung ohne Validierungsdatensatz.
- Keine fremden lokalen Aenderungen reverted; der Workspace war bereits durch den Kimi-Deep-Audit dirty.

## Next
- INT8/FP16/TTA erst mit anonymisiertem Hold-out-Set benchmarken: Dice, Stenosis-MAE, Vulnerability-AUC, p50/p95/p99 CPU-Latenz.
- P3: echte 3D/Sliding-Window-Inferenz separat designen; nicht in P0-Demo mischen.
- Deploy bleibt extern blockiert durch Lou-Steps: Fly Token, Hetzner SSH, DNS/Fly App.

## Memory updates
- `MEMORY.md` Pointer ergaenzt.
- `tasks.jsonl` K-47 hinzugefuegt und auf done gesetzt.
