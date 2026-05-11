"""Tests for ONNX Runtime session optimization settings."""

from __future__ import annotations

import os
from unittest.mock import MagicMock, patch

import numpy as np

os.environ["API_KEY"] = "a" * 32
os.environ["ADMIN_API_KEY"] = "b" * 32
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"
os.environ["ANONYMIZATION_SALT"] = "s" * 16

from app.services.inference_service import InferenceService


class TestInferenceServiceSessionOptions:
    @patch("app.services.inference_service.ort.InferenceSession")
    def test_session_uses_graph_optimization(self, mock_session):
        InferenceService(model_path="/fake/model.onnx", fallback_demo=False)
        call_kwargs = mock_session.call_args.kwargs
        sess_options = call_kwargs.get("sess_options")
        assert sess_options is not None
        # ORT_ENABLE_ALL = 99 (enum value)
        import onnxruntime as ort

        assert (
            sess_options.graph_optimization_level
            == ort.GraphOptimizationLevel.ORT_ENABLE_ALL
        )

    @patch("app.services.inference_service.ort.InferenceSession")
    def test_session_uses_cpu_provider(self, mock_session):
        InferenceService(model_path="/fake/model.onnx", fallback_demo=False)
        call_kwargs = mock_session.call_args.kwargs
        providers = call_kwargs.get("providers")
        assert providers == ["CPUExecutionProvider"]

    @patch("app.services.inference_service.ort.InferenceSession")
    def test_session_sets_thread_counts(self, mock_session):
        InferenceService(model_path="/fake/model.onnx", fallback_demo=False)
        call_kwargs = mock_session.call_args.kwargs
        sess_options = call_kwargs.get("sess_options")
        assert sess_options.intra_op_num_threads == 4
        assert sess_options.inter_op_num_threads == 2


class TestGradCamOptimization:
    @patch("app.services.gradcam.cv2.resize")
    @patch("app.services.gradcam.cv2.applyColorMap")
    @patch("app.services.gradcam.cv2.cvtColor")
    def test_batched_perturbation(self, mock_cvt, mock_color, mock_resize):
        from app.services.gradcam import generate_gradcam_heatmap

        mock_session = MagicMock()

        def _mock_run(*args, **kwargs):
            feed = args[1] if len(args) > 1 else {}
            inp = next(iter(feed.values()))
            batch = inp.shape[0]
            return [np.ones((batch, 1), dtype=np.float32) * 0.5]

        mock_session.run.side_effect = _mock_run
        mock_session.get_inputs.return_value = [MagicMock(name="input")]

        generate_gradcam_heatmap(
            mock_session, np.zeros((1, 1, 512, 512), dtype=np.float32), blocks=8
        )

        # Should be called with batched input (8 items concatenated)
        assert mock_session.run.call_count > 1  # base + batched calls
        mock_resize.assert_called_once()


class TestInferenceTTA:
    def test_model_input_batch_without_tta_has_single_window(self):
        hu = np.zeros((32, 32), dtype=np.float32)

        batch = InferenceService._build_model_input_batch(hu, enable_tta=False)

        assert batch.shape == (1, 1, 512, 512)
        assert batch.dtype == np.float32

    def test_model_input_batch_with_tta_has_three_windows(self):
        hu = np.linspace(-200, 400, num=32 * 32, dtype=np.float32).reshape(32, 32)

        batch = InferenceService._build_model_input_batch(hu, enable_tta=True)

        assert batch.shape == (3, 1, 512, 512)
        assert batch.dtype == np.float32
        assert not np.allclose(batch[0], batch[1])
