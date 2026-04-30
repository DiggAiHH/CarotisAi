"""XAI Service for generating explanation heatmaps.

Supports Grad-CAM and HiRes-CAM for MFSD-UNet segmentation model.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

import numpy as np
import structlog

if TYPE_CHECKING:
    import torch

log = structlog.get_logger()


@dataclass(frozen=True)
class XAIResult:
    """Result of XAI explanation generation."""

    heatmap: np.ndarray  # (H, W) float32 in [0, 1]
    method: str  # "gradcam" or "hirescam"
    layer_name: str
    resolution_pixels: int  # pixels above threshold
    sharpness_variance: float

    def to_dict(self) -> dict:
        return {
            "method": self.method,
            "layer_name": self.layer_name,
            "resolution_pixels": self.resolution_pixels,
            "sharpness_variance": round(self.sharpness_variance, 6),
            "shape": list(self.heatmap.shape),
        }


class XAIService:
    """Generate explanation heatmaps for segmentation predictions."""

    def __init__(
        self, model: "torch.nn.Module", target_layer: "torch.nn.Module"
    ) -> None:
        self.model = model
        self.target_layer = target_layer
        self._gradcam = None
        self._hirescam = None

    def _get_gradcam(self):
        if self._gradcam is None:
            from ml.xai.gradcam import SegGradCAM

            self._gradcam = SegGradCAM(self.model, self.target_layer)
        return self._gradcam

    def _get_hirescam(self):
        if self._hirescam is None:
            from ml.xai.gradcam import SegHiResCAM

            self._hirescam = SegHiResCAM(self.model, self.target_layer)
        return self._hirescam

    def explain(
        self,
        input_tensor: "torch.Tensor",
        method: str = "gradcam",
        threshold: float = 0.5,
    ) -> XAIResult:
        """Generate explanation heatmap.

        Args:
            input_tensor: Model input (1, C, H, W)
            method: "gradcam" or "hirescam"
            threshold: Threshold for counting resolution pixels

        Returns:
            XAIResult with heatmap and metadata
        """
        if method not in ("gradcam", "hirescam"):
            raise ValueError("method must be 'gradcam' or 'hirescam'")

        if method == "gradcam":
            cam = self._get_gradcam()
        else:
            cam = self._get_hirescam()

        heatmap = cam.generate(input_tensor)

        resolution_pixels = int((heatmap > threshold).sum())
        sharpness_variance = float(heatmap.var())

        log.info(
            "xai_heatmap_generated",
            method=method,
            shape=heatmap.shape,
            resolution_pixels=resolution_pixels,
            sharpness_variance=sharpness_variance,
        )

        return XAIResult(
            heatmap=heatmap,
            method=method,
            layer_name=str(self.target_layer),
            resolution_pixels=resolution_pixels,
            sharpness_variance=sharpness_variance,
        )

    def remove_hooks(self) -> None:
        """Clean up hooks to prevent memory leaks."""
        if self._gradcam is not None:
            self._gradcam.remove_hooks()
            self._gradcam = None
        if self._hirescam is not None:
            self._hirescam.remove_hooks()
            self._hirescam = None
