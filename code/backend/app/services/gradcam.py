from __future__ import annotations

import cv2
import numpy as np


def generate_gradcam_heatmap(
    model_session,
    input_array: np.ndarray,
    target_class: int = 0,
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

    Returns:
        512x512 RGB heatmap as ``np.uint8``.
    """
    input_name = model_session.get_inputs()[0].name
    base_output = model_session.run(None, {input_name: input_array})[0]
    base_score = float(base_output[0, target_class])

    _, _, h, w = input_array.shape
    blocks = 16
    block_h = h // blocks
    block_w = w // blocks
    sensitivity = np.zeros((blocks, blocks), dtype=np.float32)

    eps = 0.01
    for i in range(blocks):
        for j in range(blocks):
            perturbed = input_array.copy()
            y0, y1 = i * block_h, (i + 1) * block_h
            x0, x1 = j * block_w, (j + 1) * block_w
            perturbed[0, :, y0:y1, x0:x1] += eps
            pert_output = model_session.run(None, {input_name: perturbed})[0]
            sensitivity[i, j] = abs(float(pert_output[0, target_class]) - base_score)

    # Resize to 512x512
    heatmap = cv2.resize(sensitivity, (512, 512), interpolation=cv2.INTER_LINEAR)

    # Normalize
    heatmap = (heatmap - heatmap.min()) / (heatmap.max() - heatmap.min() + 1e-8)

    # Apply JET colormap
    heatmap = np.uint8(255 * heatmap)
    heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
    heatmap = cv2.cvtColor(heatmap, cv2.COLOR_BGR2RGB)

    return heatmap
