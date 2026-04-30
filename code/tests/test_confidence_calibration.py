"""Tests for ConfidenceCalibrationService."""

from __future__ import annotations

import numpy as np
import pytest

from app.services.confidence_calibration_service import (
    CalibrationMetrics,
    ConfidenceCalibrationService,
    compute_brier,
    compute_ece,
    compute_mce,
)


class TestMetrics:
    def test_ece_perfect_calibration(self):
        """Perfectly calibrated: confidence == accuracy in every bin."""
        confidences = np.array([0.1, 0.3, 0.5, 0.7, 0.9])
        accuracies = np.array([0.0, 0.0, 1.0, 1.0, 1.0])
        # Not perfectly calibrated across bins, but test basic computation
        ece = compute_ece(confidences, accuracies, n_bins=5)
        assert 0.0 <= ece <= 1.0

    def test_ece_zero_for_perfect(self):
        """If confidence exactly matches accuracy everywhere, ECE = 0."""
        confidences = np.array([0.5, 0.5, 0.5, 0.5])
        accuracies = np.array([1.0, 0.0, 1.0, 0.0])
        ece = compute_ece(confidences, accuracies, n_bins=2)
        assert ece == pytest.approx(0.0, abs=1e-6)

    def test_mce_range(self):
        confidences = np.array([0.5, 0.5])
        accuracies = np.array([1.0, 0.0])
        mce = compute_mce(confidences, accuracies, n_bins=2)
        assert 0.0 <= mce <= 1.0

    def test_brier_range(self):
        confidences = np.array([0.8, 0.2])
        accuracies = np.array([1.0, 0.0])
        brier = compute_brier(confidences, accuracies)
        assert 0.0 <= brier <= 1.0


class TestConfidenceCalibrationService:
    def test_platt_scaling_basic(self):
        """Platt scaling on simple synthetic data."""
        np.random.seed(42)
        # Generate logits where positive class has higher values
        logits = np.concatenate(
            [
                np.random.normal(2.0, 1.0, 50),
                np.random.normal(-2.0, 1.0, 50),
            ]
        )
        labels = np.concatenate([np.ones(50), np.zeros(50)])

        cal = ConfidenceCalibrationService(method="platt")
        metrics = cal.fit(logits, labels)

        assert metrics.ece < 0.3  # Should improve over raw
        assert metrics.n_samples == 100
        assert cal.is_fitted

    def test_isotonic_scaling_basic(self):
        np.random.seed(42)
        logits = np.concatenate(
            [
                np.random.normal(2.0, 1.0, 50),
                np.random.normal(-2.0, 1.0, 50),
            ]
        )
        labels = np.concatenate([np.ones(50), np.zeros(50)])

        cal = ConfidenceCalibrationService(method="isotonic")
        metrics = cal.fit(logits, labels)

        assert metrics.ece < 0.3
        assert cal.is_fitted

    def test_predict_proba_output_range(self):
        np.random.seed(42)
        logits = np.random.randn(100)
        labels = (logits > 0).astype(float)

        cal = ConfidenceCalibrationService(method="platt")
        cal.fit(logits, labels)

        test_logits = np.random.randn(20)
        probs = cal.predict_proba(test_logits)

        assert len(probs) == 20
        assert np.all(probs >= 0.0)
        assert np.all(probs <= 1.0)

    def test_predict_without_fit_raises(self):
        cal = ConfidenceCalibrationService()
        with pytest.raises(RuntimeError, match="not fitted"):
            cal.predict_proba(np.array([1.0, 2.0]))

    def test_invalid_method_raises(self):
        with pytest.raises(ValueError, match="'platt' or 'isotonic'"):
            ConfidenceCalibrationService(method="invalid")

    def test_confidence_buckets(self):
        cal = ConfidenceCalibrationService()
        assert cal.get_confidence_bucket(0.5) == "low"
        assert cal.get_confidence_bucket(0.75) == "medium"
        assert cal.get_confidence_bucket(0.95) == "high"
        assert cal.get_confidence_bucket(0.7) == "medium"
        assert cal.get_confidence_bucket(0.9) == "high"

    def test_save_and_load(self, tmp_path):
        np.random.seed(42)
        logits = np.random.randn(50)
        labels = (logits > 0).astype(float)

        cal = ConfidenceCalibrationService(method="platt")
        cal.fit(logits, labels)

        path = tmp_path / "calibration.pkl"
        cal.save(path)
        assert path.exists()

        cal2 = ConfidenceCalibrationService()
        cal2.load(path)
        assert cal2.is_fitted
        assert cal2.method == "platt"

        # Predictions should match
        test_logits = np.random.randn(10)
        probs1 = cal.predict_proba(test_logits)
        probs2 = cal2.predict_proba(test_logits)
        np.testing.assert_array_almost_equal(probs1, probs2)

    def test_metrics_to_dict(self):
        m = CalibrationMetrics(ece=0.05, mce=0.1, brier=0.08, n_samples=100)
        d = m.to_dict()
        assert d["ece"] == 0.05
        assert d["n_samples"] == 100


class TestOnnxCalibrationExport:
    def test_platt_onnx_export_roundtrip(self, tmp_path):
        """Fit Platt scaler, export to ONNX, verify ort output matches predict_proba."""
        pytest.importorskip("onnx")
        pytest.importorskip("onnxruntime")

        from ml.inference.onnx_export import _export_platt_onnx

        np.random.seed(42)
        logits = np.concatenate(
            [
                np.random.normal(2.0, 1.0, 50),
                np.random.normal(-2.0, 1.0, 50),
            ]
        )
        labels = np.concatenate([np.ones(50), np.zeros(50)])

        cal = ConfidenceCalibrationService(method="platt")
        cal.fit(logits, labels)

        onnx_path = tmp_path / "calibration.onnx"
        _export_platt_onnx(cal, onnx_path)
        assert onnx_path.exists()

        # Compare ONNX output with predict_proba
        test_logits = np.random.randn(20)
        expected = cal.predict_proba(test_logits)

        # ONNX graph takes raw_confidence (sigmoid-transformed logits)
        raw_confidence = 1.0 / (1.0 + np.exp(-test_logits))
        raw_confidence = np.clip(raw_confidence, 1e-6, 1 - 1e-6)
        raw_confidence = raw_confidence.reshape(-1, 1).astype(np.float32)

        import onnxruntime as ort

        sess = ort.InferenceSession(str(onnx_path), providers=["CPUExecutionProvider"])
        onnx_output = sess.run(None, {"raw_confidence": raw_confidence})[0].flatten()

        np.testing.assert_allclose(onnx_output, expected, rtol=1e-5, atol=1e-5)
