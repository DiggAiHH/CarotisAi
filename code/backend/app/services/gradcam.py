from __future__ import annotations

import cv2
import numpy as np


def _extract_scalar_score(
    outputs: list[np.ndarray],
    batch_index: int,
    target_class: int,
) -> float:
    """Return a stable scalar from common demo-model ONNX output shapes."""
    score_output = outputs[1] if len(outputs) > 1 else outputs[0]
    arr = np.asarray(score_output, dtype=np.float32)
    if arr.ndim == 0:
        return float(arr)

    sample = arr[batch_index] if arr.shape[0] > batch_index else arr
    flat = np.asarray(sample, dtype=np.float32).reshape(-1)
    if flat.size == 0:
        return 0.0
    return float(flat[min(target_class, flat.size - 1)])


def generate_gradcam_heatmap(
    model_session,
    input_array: np.ndarray,
    target_class: int = 0,
    blocks: int = 16,
) -> np.ndarray:
    """
    Generate a class activation heatmap for an ONNX model session.

    Uses a finite-difference (block-perturbation) approach since ONNX
    Runtime does not expose native gradients. For production use,
    export the model with an explicit feature-map output or switch
    to the PyTorch model for full Grad-CAM support.

    Args:
        model_session: An ``onnxruntime.InferenceSession``.
        input_array: Pre-processed array of shape (N, C, H, W).
        target_class: Output index to explain.
        blocks: Grid size for perturbation (default 16, use 8 for faster inference).

    Returns:
        512x512 RGB heatmap as ``np.uint8``.
    """
    input_name = model_session.get_inputs()[0].name
    base_outputs = model_session.run(None, {input_name: input_array})
    base_score = _extract_scalar_score(base_outputs, 0, target_class)

    _, _, h, w = input_array.shape
    block_h = h // blocks
    block_w = w // blocks
    sensitivity = np.zeros((blocks, blocks), dtype=np.float32)

    eps = 0.01
    # Batch perturbations row-wise to reduce ONNX session overhead
    batch_inputs = []
    coords = []
    for i in range(blocks):
        for j in range(blocks):
            perturbed = input_array.copy()
            y0, y1 = i * block_h, (i + 1) * block_h
            x0, x1 = j * block_w, (j + 1) * block_w
            perturbed[0, :, y0:y1, x0:x1] += eps
            batch_inputs.append(perturbed)
            coords.append((i, j))

    # Keep perturbation inference sequential: some exported demo models have a
    # fixed batch dimension of 1 and reject concatenated perturbation batches.
    for idx, perturbed in enumerate(batch_inputs):
        outputs = model_session.run(None, {input_name: perturbed})
        i, j = coords[idx]
        score = _extract_scalar_score(outputs, 0, target_class)
        sensitivity[i, j] = abs(score - base_score)

    # Resize to 512x512
    heatmap = cv2.resize(sensitivity, (512, 512), interpolation=cv2.INTER_LINEAR)

    # Normalize
    heatmap = (heatmap - heatmap.min()) / (heatmap.max() - heatmap.min() + 1e-8)

    # Apply JET colormap
    heatmap = np.uint8(255 * heatmap)
    heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
    heatmap = cv2.cvtColor(heatmap, cv2.COLOR_BGR2RGB)

    return heatmap
