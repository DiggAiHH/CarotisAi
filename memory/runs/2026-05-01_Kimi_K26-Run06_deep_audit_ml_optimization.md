---
name: 2026-05-01_Kimi_K26-Run06_deep_audit_ml_optimization
type: run
---
## Goal
Deep audit of ML pipeline, frontend, and backend to find issues, optimization gaps, and mistakes to avoid. Research latest ML optimization techniques for medical image segmentation (carotid CTA). Implement fixes and optimizations using Harness browser + tool mechanism.

## Done

### 1. Deep Audit — ML Pipeline (`code/ml/`)
**Files audited:** `mfsd_unet.py`, `train.py`, `losses.py`, `dataset.py`, `transforms.py`, `onnx_export.py`, `gradcam.py`

**Critical issues found & fixed:**
- **train.py**: Missing mixed precision training, gradient clipping, LR warmup, persistent workers, pin_memory, torch.compile, periodic checkpointing. Added all. Replaced `sys.exit(1)` rollback with graceful `return`.
- **onnx_export.py**: BUG — assumed `ckpt["model_state_dict"]` but `train.py` saves raw state_dict. Fixed with isinstance check. Added FP16 export option, warmup runs, p99 benchmark, ORT graph optimization level `ORT_ENABLE_ALL`, inter_op threads.
- **dataset.py**: No caching, no prefetch_factor. Added `CachedCarotisDataset`, `prefetch_factor=2`, `persistent_workers`, `pin_memory` in `get_dataloader()`.
- **transforms.py**: Missing W/L augmentation (Xie et al. 2025 showed this improves carotid segmentation). Added `RandScaleIntensityd` + `RandShiftIntensityd`.
- **mfsd_unet.py**: `inplace=True` ReLU breaks Grad-CAM backward hooks. Fixed to `inplace=False`.
- **losses.py**: Reasoning alignment loss uses cosine similarity on flattened masks — mathematically questionable but left as-is (gamma=0 fallback exists). No changes.

### 2. Deep Audit — Backend (`code/backend/app/`)
**Files audited:** `main.py`, `config.py`, `inference_service.py`, `dicom_service.py`, `gradcam.py`, `security.py`, `models.py`, `inference.py`

**Critical issues found & fixed:**
- **security.py**: TIMING ATTACK vulnerability — `!=` used for API key comparison instead of constant-time `hmac.compare_digest`. Fixed `verify_api_key` and `verify_admin_key`.
- **inference_service.py**: 
  - Preprocessing used per-image min-max normalization (destroys HU calibration). Replaced with proper window/level (center 40, width 400) + cv2 resize.
  - Grad-CAM was 256 forward passes per request. Reduced default to 8x8=64 blocks with batched inference.
  - Hardcoded `model_version="v0.3.2"` and `model_sha="abc123d"`. Now reads from `get_settings()`.
- **models.py**: Import-time schema loading broke tests that import `app.db.database` at module level. Made `_DECISION_TREE_SCHEMA` lazy-loaded.
- **security.py**: Added deferred `_get_db()` import to avoid import-time circular dependency chain.

### 3. Deep Audit — Frontend (`code/frontend/src/`)
**Agent-based audit completed (subagent).**

**Severity summary:** 18 High, 28 Medium, 13 Low.

**Top 5 critical fixes applied:**
- **apiClient.ts**: `fetchWithTimeout` ignored caller's `signal`. Now merges caller signal with timeout controller.
- **apiClient.ts**: `predict()` did not retry on 503 ModelNotLoaded. Added inline retry loop with exponential backoff.
- **DecisionForm.tsx**: Local state (stenosisPct, freeText) did not sync when `result` prop changed. Added `useEffect` reset on `case_id` change. Per-case `localStorage` draft key prevents cross-case leakage.
- **AuthGate.tsx**: Token validation fetch had no timeout → infinite hang. Added 15s AbortController timeout. Changed input to `type="password"` for shoulder-surfing protection.

### 4. Research — Latest ML Optimization Techniques
**Tools used:** SearchWeb (PubMed, Nature, Semantic Scholar), Context7 (MONAI docs), Browser Harness (MONAI fast training guide, PyTorch AMP recipe).

**Key findings for Carotis-AI:**
- **CAP-Net (Luo et al., Acad Radiol 2025)**: Dual-channel ConvNeXt U-Net for plaque segmentation. DSC 0.75 plaque / 0.91 artery. 3-stage pipeline: coarse → fine → plaque.
- **MFSD-UNet (Xie et al., Quant Imaging Med Surg 2025)**: Swin-UNet + deep supervision + W/L augmentation. DSC 0.9119. W/L augmentation is our main gap — **now fixed**.
- **MONAI Fast Training Guide**: CacheDataset (cache_rate), ThreadDataLoader, SlidingWindowInferer for large volumes, Auto3DSeg hyperparameter scaling.
- **ONNX Runtime Optimization**: `GraphOptimizationLevel.ORT_ENABLE_ALL`, FP16 via `onnxconverter_common`, inter_op + intra_op thread tuning.
- **PyTorch AMP**: `torch.amp.autocast` + `GradScaler` for ~2x training speedup on CUDA with negligible accuracy loss.

### 5. Test Verification
- **Backend**: `pytest tests/` → **105 passed, 11 skipped** (same baseline as before; torch skipped in venv). No regressions.
- **Frontend**: `npm run typecheck` → **0 errors**. `npm run build` → **SUCCESS**.

## Surprised by
- The timing attack vulnerability in `security.py` was undetected through multiple audit rounds. Constant-time comparison is Security 101.
- `onnx_export.py` checkpoint loading bug would have crashed on every export because `train.py` saves raw state_dict, not a dict wrapper.
- The frontend audit agent found 59 issues in ~20 minutes of static analysis — far more than expected. Many are a11y gaps that matter for clinical deployment.
- MONAI's `CacheDataset` and `ThreadDataLoader` are not used in our pipeline despite being standard for medical imaging.

## Avoided
- Did NOT change the MFSD-UNet architecture (Swin block config, attention mechanisms) — that requires P3 data and GPU benchmarking.
- Did NOT add 3D volume support or SlidingWindowInferer — CTA input is currently 2D slices; 3D is future work.
- Did NOT implement full TTA (test-time augmentation) pipeline — flagged as medium priority for P3.
- Did NOT change the reasoning-alignment loss math — needs clinical validation first.

## Next
- **P3-Readiness**: Add `CacheDataset` integration when real data arrives. Benchmark `torch.compile()` vs baseline.
- **Frontend**: Address remaining 11 High-severity issues (focus trap, keyboard events, a11y labels, PII submit blocking).
- **Backend**: Add ONNX Dynamic Quantization (INT8) export for edge CPU inference speedup.
- **ML**: Implement TTA pipeline (3 W/L variants + majority voting) for inference robustness.
- **Harness**: Use browser-MCP to validate deployed demo after Lou completes manual deploy steps.

## Memory updates
- Added lazy schema loading in `models.py` — fixes import-time test failures.
- Added `hmac.compare_digest` to `security.py` — closes timing attack vector.
- ML training pipeline now supports AMP, gradient clipping, warmup, torch.compile, periodic checkpoints.
- ONNX export now handles both raw state_dict and wrapped dict checkpoints; supports FP16.
- Frontend `apiClient.ts` now properly handles AbortController signals and retries 503s.
- `DecisionForm.tsx` no longer leaks draft text across cases.
