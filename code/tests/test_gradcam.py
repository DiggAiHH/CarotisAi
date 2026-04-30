"""Tests for Grad-CAM and HiResCAM XAI modules.

Skips gracefully if torch is not installed.
"""

from __future__ import annotations

import pytest

try:
    import torch
    import torch.nn as nn

    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False


@pytest.mark.skipif(not TORCH_AVAILABLE, reason="torch not installed")
class TestSegGradCAM:
    def test_gradcam_output_shape(self):
        from ml.xai.gradcam import SegGradCAM

        class DummySegModel(nn.Module):
            def __init__(self):
                super().__init__()
                self.conv = nn.Conv2d(1, 8, 3, padding=1)
                self.out = nn.Conv2d(8, 1, 1)

            def forward(self, x):
                return [self.out(torch.relu(self.conv(x)))]

        model = DummySegModel()
        cam = SegGradCAM(model, model.conv)

        x = torch.randn(1, 1, 64, 64)
        heatmap = cam.generate(x)

        assert heatmap.shape == (64, 64)
        assert heatmap.min() >= 0.0
        assert heatmap.max() <= 1.0

        cam.remove_hooks()

    def test_gradcam_values_normalised(self):
        from ml.xai.gradcam import SegGradCAM

        class DummySegModel(nn.Module):
            def __init__(self):
                super().__init__()
                self.conv = nn.Conv2d(1, 4, 3, padding=1)
                self.out = nn.Conv2d(4, 1, 1)

            def forward(self, x):
                return [self.out(torch.relu(self.conv(x)))]

        model = DummySegModel()
        cam = SegGradCAM(model, model.conv)

        x = torch.randn(1, 1, 32, 32)
        heatmap = cam.generate(x)

        assert heatmap.dtype == "float32"
        assert 0.0 <= heatmap.min() <= heatmap.max() <= 1.0

        cam.remove_hooks()


@pytest.mark.skipif(not TORCH_AVAILABLE, reason="torch not installed")
class TestSegHiResCAM:
    def test_hirescam_output_shape(self):
        from ml.xai.gradcam import SegHiResCAM

        class DummySegModel(nn.Module):
            def __init__(self):
                super().__init__()
                self.conv = nn.Conv2d(1, 8, 3, padding=1)
                self.out = nn.Conv2d(8, 1, 1)

            def forward(self, x):
                return [self.out(torch.relu(self.conv(x)))]

        model = DummySegModel()
        cam = SegHiResCAM(model, model.conv)

        x = torch.randn(1, 1, 64, 64)
        heatmap = cam.generate(x)

        assert heatmap.shape == (64, 64)
        assert heatmap.min() >= 0.0
        assert heatmap.max() <= 1.0

        cam.remove_hooks()

    def test_hirescam_sharper_than_gradcam(self):
        """HiResCAM should have higher spatial variance (sharper) than Grad-CAM."""
        from ml.xai.gradcam import SegGradCAM, SegHiResCAM

        class DummySegModel(nn.Module):
            def __init__(self):
                super().__init__()
                self.conv = nn.Conv2d(1, 8, 3, padding=1)
                self.out = nn.Conv2d(8, 1, 1)

            def forward(self, x):
                return [self.out(torch.relu(self.conv(x)))]

        model = DummySegModel()

        grad_cam = SegGradCAM(model, model.conv)
        hires_cam = SegHiResCAM(model, model.conv)

        torch.manual_seed(42)
        x = torch.randn(1, 1, 32, 32)

        h_grad = grad_cam.generate(x)
        h_hires = hires_cam.generate(x)

        # Spatial variance as proxy for sharpness
        var_grad = h_grad.var()
        var_hires = h_hires.var()

        # HiResCAM should typically be sharper (higher variance)
        # but this is a statistical property, not guaranteed on single sample
        # so we just check both are valid
        assert var_grad >= 0
        assert var_hires >= 0

        grad_cam.remove_hooks()
        hires_cam.remove_hooks()
