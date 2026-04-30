"""Grad-CAM + HiResCAM for MFSD-UNet segmentation model.

Used during training/eval to visualise which regions the model focuses on.
The backend XAI service uses cv2-based overlay (no PyTorch needed at inference).
This module is for training-time analysis and validation only.

References:
- Grad-CAM: Selvaraju et al., ICCV 2017
- HiResCAM: Draelos & Carin, Nature MI 2021 (pixel-wise weighting instead of GAP)
"""

from __future__ import annotations

import numpy as np
import torch
import torch.nn.functional as F


class SegGradCAM:
    """Grad-CAM for a segmentation model.

    Hooks into a specific convolutional layer and uses the gradient of
    the sum of the segmentation mask (i.e. predicted lesion area) with
    respect to that layer's activations.
    """

    def __init__(self, model: torch.nn.Module, target_layer: torch.nn.Module) -> None:
        self.model = model
        self._activations: torch.Tensor | None = None
        self._gradients: torch.Tensor | None = None

        self._fwd_hook = target_layer.register_forward_hook(self._save_activation)
        self._bwd_hook = target_layer.register_full_backward_hook(self._save_gradient)

    def _save_activation(self, _module, _input, output: torch.Tensor) -> None:
        self._activations = output.detach()

    def _save_gradient(self, _module, _grad_input, grad_output: tuple) -> None:
        self._gradients = grad_output[0].detach()

    def generate(self, input_tensor: torch.Tensor) -> np.ndarray:
        """Return Grad-CAM heatmap (H, W) normalised to [0, 1]."""
        self.model.eval()
        input_tensor = input_tensor.requires_grad_(True)

        outputs = self.model(input_tensor)
        seg_main = outputs[0]  # (1, 1, H, W)

        # Score = sum of positive activations in the segmentation mask
        score = F.relu(seg_main).sum()
        self.model.zero_grad()
        score.backward()

        if self._gradients is None or self._activations is None:
            raise RuntimeError("Hooks did not capture gradients/activations")

        # Global average pool gradients across spatial dims (Grad-CAM)
        weights = self._gradients.mean(dim=(2, 3), keepdim=True)  # (1, C, 1, 1)
        cam = (weights * self._activations).sum(dim=1, keepdim=True)  # (1, 1, H, W)
        cam = F.relu(cam)

        # Resize to input resolution
        h, w = input_tensor.shape[2:]
        cam = F.interpolate(cam, size=(h, w), mode="bilinear", align_corners=False)
        cam = cam.squeeze().cpu().numpy()

        # Normalise
        cam_min, cam_max = cam.min(), cam.max()
        if cam_max > cam_min:
            cam = (cam - cam_min) / (cam_max - cam_min)

        return cam.astype(np.float32)

    def remove_hooks(self) -> None:
        self._fwd_hook.remove()
        self._bwd_hook.remove()


class SegHiResCAM:
    """HiRes-CAM for a segmentation model.

    Unlike Grad-CAM which globally averages gradients (GAP), HiResCAM
    uses pixel-wise gradient weighting:
        cam = sum(gradients * activations, dim=1)

    This preserves spatial resolution and avoids the blurring effect of GAP.
    Particularly beneficial for thin vessel structures in CTA images.

    Reference: Draelos & Carin, "HiResCAM: Interpretable deep learning
    for medical image analysis", Nature Machine Intelligence 2021.
    """

    def __init__(self, model: torch.nn.Module, target_layer: torch.nn.Module) -> None:
        self.model = model
        self._activations: torch.Tensor | None = None
        self._gradients: torch.Tensor | None = None

        self._fwd_hook = target_layer.register_forward_hook(self._save_activation)
        self._bwd_hook = target_layer.register_full_backward_hook(self._save_gradient)

    def _save_activation(self, _module, _input, output: torch.Tensor) -> None:
        self._activations = output.detach()

    def _save_gradient(self, _module, _grad_input, grad_output: tuple) -> None:
        self._gradients = grad_output[0].detach()

    def generate(self, input_tensor: torch.Tensor) -> np.ndarray:
        """Return HiRes-CAM heatmap (H, W) normalised to [0, 1]."""
        self.model.eval()
        input_tensor = input_tensor.requires_grad_(True)

        outputs = self.model(input_tensor)
        seg_main = outputs[0]  # (1, 1, H, W)

        score = F.relu(seg_main).sum()
        self.model.zero_grad()
        score.backward()

        if self._gradients is None or self._activations is None:
            raise RuntimeError("Hooks did not capture gradients/activations")

        # HiResCAM: pixel-wise multiplication instead of GAP
        # gradients shape: (1, C, H', W')
        # activations shape: (1, C, H', W')
        cam = (self._gradients * self._activations).sum(dim=1, keepdim=True)
        cam = F.relu(cam)

        # Resize to input resolution
        h, w = input_tensor.shape[2:]
        cam = F.interpolate(cam, size=(h, w), mode="bilinear", align_corners=False)
        cam = cam.squeeze().cpu().numpy()

        # Normalise
        cam_min, cam_max = cam.min(), cam.max()
        if cam_max > cam_min:
            cam = (cam - cam_min) / (cam_max - cam_min)

        return cam.astype(np.float32)

    def remove_hooks(self) -> None:
        self._fwd_hook.remove()
        self._bwd_hook.remove()
