---
name: nightly-retrain
trigger_phrases: ["trainiere mit neuen Decision-Trees", "nightly retrain", "incremental train"]
schedule: "0 22 * * *"  # 22:00 Klinikum-Schliesszeit
required_tools: [bash, filesystem]
---
# Nightly-Retrain Skill

Action: Liest memory/decisions/ since last_run, wenn >= 10 neue Trees
verfuegbar, ruft ml/training/train.py --incremental, vergleicht
Performance, deploy oder rollback.

Steps:
1. ls ../memory/decisions/ | filter > last_run_timestamp
2. Wenn count < 10: log "skipped, nicht genug Trees", exit
3. Run: python ../ml/training/train.py --incremental --max-epochs 3
   --config configs/incremental.yaml
4. Bei return-code 1: log "rollback_triggered", senden Alert an Lou
   (Mail oder Slack via Hermes-Webhook)
5. Bei return-code 0:
   a. python -m ../ml.inference.onnx_export --checkpoint <new_ckpt>
      --output ../data/models/mfsd_unet_new.onnx
   b. python ../scripts/sign_model.py (kommt in T-016 aus tasks.jsonl)
   c. atomic mv mfsd_unet_new.onnx -> mfsd_unet.onnx
   d. POST /admin/reload-model an Backend (causes lazy reload)
6. Eintrag in ../memory/runs/<datum>_nightly_retrain.md mit
   Performance-Diff
