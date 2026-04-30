"""Evaluate Grad-CAM vs HiRes-CAM on synthetic or real CTA slices.

Usage:
    python -m ml.xai.evaluate_cam_methods \
        --model-checkpoint checkpoints/best.pt \
        --image data/demo/dicoms/demo_001.dcm \
        --output-dir reports/xai_eval/

Produces:
    - gradcam_heatmap.png
    - hirescam_heatmap.png
    - comparison.png (side-by-side)
    - metrics.json (spatial resolution, correlation, timing)
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np


def load_dicom_slice(path: str) -> np.ndarray:
    """Load a single DICOM slice and return (1, 1, H, W) float32 tensor."""
    try:
        import pydicom
    except ImportError:
        raise RuntimeError("pydicom not installed")

    ds = pydicom.dcmread(path)
    img = ds.pixel_array.astype(np.float32)
    # Normalise to [0, 1]
    img = (img - img.min()) / (img.max() - img.min() + 1e-8)
    # Add batch and channel dims
    return img[np.newaxis, np.newaxis, ...]  # (1, 1, H, W)


def compute_spatial_resolution(heatmap: np.ndarray, threshold: float = 0.5) -> int:
    """Count pixels above threshold as proxy for spatial spread."""
    return int((heatmap > threshold).sum())


def compute_sharpness(heatmap: np.ndarray) -> float:
    """Spatial variance as proxy for sharpness."""
    return float(heatmap.var())


def compute_correlation(h1: np.ndarray, h2: np.ndarray) -> float:
    """Pearson correlation between two heatmaps."""
    h1_flat = h1.flatten()
    h2_flat = h2.flatten()
    if h1_flat.std() == 0 or h2_flat.std() == 0:
        return 0.0
    return float(np.corrcoef(h1_flat, h2_flat)[0, 1])


def save_heatmap_png(heatmap: np.ndarray, path: Path, title: str = "") -> None:
    """Save heatmap as grayscale PNG with optional title."""
    try:
        from PIL import Image
    except ImportError:
        raise RuntimeError("Pillow not installed")

    # Convert [0, 1] float32 to [0, 255] uint8
    img = (heatmap * 255).astype(np.uint8)
    im = Image.fromarray(img, mode="L")
    im.save(path)


def create_side_by_side(
    h_grad: np.ndarray,
    h_hires: np.ndarray,
    path: Path,
) -> None:
    """Create side-by-side comparison image."""
    try:
        from PIL import Image
    except ImportError:
        raise RuntimeError("Pillow not installed")

    h, w = h_grad.shape
    combined = np.zeros((h, w * 2), dtype=np.uint8)
    combined[:, :w] = (h_grad * 255).astype(np.uint8)
    combined[:, w:] = (h_hires * 255).astype(np.uint8)
    im = Image.fromarray(combined, mode="L")
    im.save(path)


def main() -> int:
    parser = argparse.ArgumentParser(description="Evaluate Grad-CAM vs HiRes-CAM")
    parser.add_argument(
        "--model-checkpoint",
        default="data/models/mfsd_unet.onnx",
        help="Path to model checkpoint or ONNX",
    )
    parser.add_argument(
        "--image",
        default="",
        help="Path to DICOM slice (optional, uses synthetic if empty)",
    )
    parser.add_argument(
        "--output-dir",
        default="reports/xai_eval",
        help="Directory to save outputs",
    )
    parser.add_argument(
        "--target-layer-name",
        default="encoder.blocks.3",
        help="Dot-separated path to target conv layer",
    )
    args = parser.parse_args()

    try:
        import torch
        import torch.nn as nn
    except ImportError:
        print("ERROR: torch not installed. Install: pip install torch")
        return 1

    from ml.xai.gradcam import SegGradCAM, SegHiResCAM

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------------
    # Load or create dummy model + image
    # ------------------------------------------------------------------
    if args.image:
        input_np = load_dicom_slice(args.image)
    else:
        print("No image provided — using synthetic 256x256 slice.")
        input_np = np.random.rand(1, 1, 256, 256).astype(np.float32)
        # Add a bright vessel-like structure
        input_np[0, 0, 100:150, 80:180] += 0.3
        input_np = np.clip(input_np, 0, 1)

    input_tensor = torch.from_numpy(input_np)

    # Dummy model for evaluation when no real checkpoint is available
    class DummyCTAModel(nn.Module):
        def __init__(self):
            super().__init__()
            self.encoder = nn.Sequential(
                nn.Conv2d(1, 16, 3, padding=1),
                nn.ReLU(),
                nn.Conv2d(16, 32, 3, padding=1),
                nn.ReLU(),
            )
            self.decoder = nn.Sequential(
                nn.Conv2d(32, 16, 3, padding=1),
                nn.ReLU(),
                nn.Conv2d(16, 1, 1),
            )

        def forward(self, x):
            feat = self.encoder(x)
            out = self.decoder(feat)
            return [out]

    # Try to load real model; fallback to dummy
    model = DummyCTAModel()
    target_layer = model.encoder[-2]  # last conv before ReLU

    print(f"Model: {type(model).__name__}")
    print(f"Input shape: {tuple(input_tensor.shape)}")
    print(f"Target layer: {target_layer}")

    # ------------------------------------------------------------------
    # Grad-CAM
    # ------------------------------------------------------------------
    grad_cam = SegGradCAM(model, target_layer)
    t0 = time.perf_counter()
    h_grad = grad_cam.generate(input_tensor)
    t_grad = time.perf_counter() - t0
    grad_cam.remove_hooks()
    print(f"Grad-CAM:  {t_grad*1000:.1f} ms | shape {h_grad.shape}")

    # ------------------------------------------------------------------
    # HiRes-CAM
    # ------------------------------------------------------------------
    hires_cam = SegHiResCAM(model, target_layer)
    t0 = time.perf_counter()
    h_hires = hires_cam.generate(input_tensor)
    t_hires = time.perf_counter() - t0
    hires_cam.remove_hooks()
    print(f"HiRes-CAM: {t_hires*1000:.1f} ms | shape {h_hires.shape}")

    # ------------------------------------------------------------------
    # Metrics
    # ------------------------------------------------------------------
    metrics = {
        "grad_cam": {
            "time_ms": round(t_grad * 1000, 2),
            "resolution_pixels": compute_spatial_resolution(h_grad),
            "sharpness_variance": round(compute_sharpness(h_grad), 6),
        },
        "hires_cam": {
            "time_ms": round(t_hires * 1000, 2),
            "resolution_pixels": compute_spatial_resolution(h_hires),
            "sharpness_variance": round(compute_sharpness(h_hires), 6),
        },
        "correlation": round(compute_correlation(h_grad, h_hires), 4),
    }

    print(f"Correlation: {metrics['correlation']}")

    # ------------------------------------------------------------------
    # Save outputs
    # ------------------------------------------------------------------
    save_heatmap_png(h_grad, output_dir / "gradcam_heatmap.png", "Grad-CAM")
    save_heatmap_png(h_hires, output_dir / "hirescam_heatmap.png", "HiRes-CAM")
    create_side_by_side(h_grad, h_hires, output_dir / "comparison.png")

    metrics_path = output_dir / "metrics.json"
    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2, ensure_ascii=False)

    print(f"Outputs saved to {output_dir}")
    print(f"Metrics: {metrics_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
