"""Confidence calibration for MFSD-UNet predictions.

Implements Platt scaling and temperature scaling to convert
model logits into well-calibrated probabilities.

References:
- Platt, "Probabilistic outputs for support vector machines", 1999
- Guo et al., "On calibration of modern neural networks", ICML 2017
"""

from __future__ import annotations

import pickle
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import structlog

log = structlog.get_logger()


def _import_sklearn():
    """Lazy-import sklearn to avoid hard dependency in test environments."""
    try:
        from sklearn.linear_model import LogisticRegression
        from sklearn.isotonic import IsotonicRegression
        return LogisticRegression, IsotonicRegression
    except ImportError as exc:
        raise ImportError(
            "scikit-learn is required for confidence calibration. "
            "Install it with: pip install scikit-learn"
        ) from exc


@dataclass(frozen=True)
class CalibrationMetrics:
    """Metrics assessing calibration quality."""

    ece: float  # Expected Calibration Error
    mce: float  # Maximum Calibration Error
    brier: float  # Brier score
    n_samples: int

    def to_dict(self) -> dict:
        return {
            "ece": round(self.ece, 4),
            "mce": round(self.mce, 4),
            "brier": round(self.brier, 4),
            "n_samples": self.n_samples,
        }


def compute_ece(
    confidences: np.ndarray, accuracies: np.ndarray, n_bins: int = 15
) -> float:
    """Compute Expected Calibration Error.

    Args:
        confidences: Predicted confidence scores (0-1)
        accuracies: Binary correct/incorrect (0 or 1)
        n_bins: Number of equal-width bins

    Returns:
        ECE value in [0, 1]
    """
    bin_boundaries = np.linspace(0, 1, n_bins + 1)
    ece = 0.0

    for i in range(n_bins):
        low, high = bin_boundaries[i], bin_boundaries[i + 1]
        in_bin = (confidences > low) & (confidences <= high)
        if i == 0:
            in_bin = (confidences >= low) & (confidences <= high)

        prop = in_bin.mean()
        if prop > 0:
            avg_confidence = confidences[in_bin].mean()
            avg_accuracy = accuracies[in_bin].mean()
            ece += np.abs(avg_confidence - avg_accuracy) * prop

    return float(ece)


def compute_mce(
    confidences: np.ndarray, accuracies: np.ndarray, n_bins: int = 15
) -> float:
    """Compute Maximum Calibration Error."""
    bin_boundaries = np.linspace(0, 1, n_bins + 1)
    mce = 0.0

    for i in range(n_bins):
        low, high = bin_boundaries[i], bin_boundaries[i + 1]
        in_bin = (confidences > low) & (confidences <= high)
        if i == 0:
            in_bin = (confidences >= low) & (confidences <= high)

        if in_bin.any():
            avg_confidence = confidences[in_bin].mean()
            avg_accuracy = accuracies[in_bin].mean()
            mce = max(mce, np.abs(avg_confidence - avg_accuracy))

    return float(mce)


def compute_brier(confidences: np.ndarray, accuracies: np.ndarray) -> float:
    """Compute Brier score (mean squared error of probabilities)."""
    return float(np.mean((confidences - accuracies) ** 2))


class ConfidenceCalibrationService:
    """Calibrate model confidence scores using Platt or Isotonic scaling.

    Usage:
        cal = ConfidenceCalibrationService(method="platt")
        cal.fit(val_logits, val_labels)
        calibrated_prob = cal.predict_proba(test_logits)
    """

    def __init__(self, method: str = "platt") -> None:
        if method not in ("platt", "isotonic"):
            raise ValueError("method must be 'platt' or 'isotonic'")
        self.method = method
        self._calibrator: object | None = None
        self._metrics: CalibrationMetrics | None = None

    def fit(self, logits: np.ndarray, labels: np.ndarray) -> CalibrationMetrics:
        """Fit calibrator on validation data.

        Args:
            logits: Raw model logits (N,) or (N, C) — binary or multi-class
            labels: Ground truth labels (N,)
        """
        logits = np.asarray(logits)
        labels = np.asarray(labels)

        # Convert logits to probabilities via sigmoid for binary
        if logits.ndim == 1 or logits.shape[1] == 1:
            probs = 1.0 / (1.0 + np.exp(-logits.squeeze()))
        else:
            # Multi-class: use softmax
            exp_logits = np.exp(logits - np.max(logits, axis=1, keepdims=True))
            probs = exp_logits / exp_logits.sum(axis=1, keepdims=True)
            # For calibration, we typically calibrate the predicted class probability
            pred_class = probs.argmax(axis=1)
            probs = probs[np.arange(len(probs)), pred_class]
            labels = (labels == pred_class).astype(float)

        probs = np.clip(probs, 1e-6, 1 - 1e-6)

        LogisticRegression, IsotonicRegression = _import_sklearn()
        if self.method == "platt":
            self._calibrator = LogisticRegression(C=1e10, solver="lbfgs", max_iter=1000)
            self._calibrator.fit(probs.reshape(-1, 1), labels)
        else:  # isotonic
            self._calibrator = IsotonicRegression(out_of_bounds="clip")
            self._calibrator.fit(probs, labels)

        # Compute calibration metrics on training data
        calibrated = self.predict_proba(logits)
        accuracies = (labels > 0.5).astype(float)

        ece = compute_ece(calibrated, accuracies)
        mce = compute_mce(calibrated, accuracies)
        brier = compute_brier(calibrated, accuracies)

        self._metrics = CalibrationMetrics(
            ece=ece, mce=mce, brier=brier, n_samples=len(labels)
        )

        log.info(
            "calibration_fitted",
            method=self.method,
            ece=ece,
            mce=mce,
            brier=brier,
            n_samples=len(labels),
        )
        return self._metrics

    def predict_proba(self, logits: np.ndarray) -> np.ndarray:
        """Return calibrated probabilities for given logits."""
        if self._calibrator is None:
            raise RuntimeError("Calibrator not fitted. Call fit() first.")

        logits = np.asarray(logits)
        if logits.ndim == 1 or logits.shape[1] == 1:
            probs = 1.0 / (1.0 + np.exp(-logits.squeeze()))
        else:
            exp_logits = np.exp(logits - np.max(logits, axis=1, keepdims=True))
            probs = exp_logits / exp_logits.sum(axis=1, keepdims=True)
            pred_class = probs.argmax(axis=1)
            probs = probs[np.arange(len(probs)), pred_class]

        probs = np.clip(probs, 1e-6, 1 - 1e-6)

        if self.method == "platt":
            calibrated = self._calibrator.predict_proba(probs.reshape(-1, 1))[:, 1]
        else:
            calibrated = self._calibrator.transform(probs)

        return np.clip(calibrated, 0.0, 1.0)

    def get_confidence_bucket(self, confidence: float) -> str:
        """Map confidence to discrete bucket for UI display."""
        if confidence < 0.7:
            return "low"
        if confidence < 0.9:
            return "medium"
        return "high"

    def save(self, path: str | Path) -> None:
        """Serialize calibrator to disk."""
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "wb") as f:
            pickle.dump(
                {
                    "method": self.method,
                    "calibrator": self._calibrator,
                    "metrics": self._metrics,
                },
                f,
            )
        log.info("calibration_saved", path=str(path))

    def load(self, path: str | Path) -> None:
        """Deserialize calibrator from disk."""
        with open(path, "rb") as f:
            data = pickle.load(f)
        self.method = data["method"]
        self._calibrator = data["calibrator"]
        self._metrics = data["metrics"]
        log.info("calibration_loaded", path=str(path), method=self.method)

    @property
    def metrics(self) -> CalibrationMetrics | None:
        return self._metrics

    @property
    def is_fitted(self) -> bool:
        return self._calibrator is not None
