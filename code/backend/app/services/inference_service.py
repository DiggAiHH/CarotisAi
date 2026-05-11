from __future__ import annotations

import asyncio
import base64
import hashlib
import os
import uuid
from datetime import datetime, timezone
from io import BytesIO

import numpy as np
import onnxruntime as ort
import pydicom
import structlog
from PIL import Image
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.core.config import get_settings
from app.db.models import AuditEvent
from app.schemas.inference import PredictionResponse
from app.services.anonymization_service import AnonymizationService
from app.services.confidence_calibration_service import ConfidenceCalibrationService
from app.services.gradcam import generate_gradcam_heatmap

logger = structlog.get_logger()


class InferenceService:
    def __init__(
        self,
        model_path: str,
        fallback_demo: bool = False,
        db_session_factory: async_sessionmaker | None = None,
    ):
        self.logger = logger.bind(service="inference")
        self.db_session_factory = db_session_factory
        self.model_path = model_path

        # Load calibration if available
        self._calibrator: ConfidenceCalibrationService | None = None
        cal_path = os.path.join(os.path.dirname(model_path), "calibration.pkl")
        if os.path.exists(cal_path):
            self._calibrator = ConfidenceCalibrationService()
            self._calibrator.load(cal_path)
            self.logger.info("calibration_loaded", path=cal_path)

        try:
            sess_options = ort.SessionOptions()
            sess_options.graph_optimization_level = (
                ort.GraphOptimizationLevel.ORT_ENABLE_ALL
            )
            sess_options.intra_op_num_threads = 4
            sess_options.inter_op_num_threads = 2
            sess_options.enable_cpu_mem_arena = True
            self.session = ort.InferenceSession(
                model_path,
                sess_options=sess_options,
                providers=["CPUExecutionProvider"],
            )
            self.model_loaded = True
            self.logger.info("model_loaded", path=model_path, threads=4)
        except Exception as exc:
            if fallback_demo:
                self.logger.warning(
                    "model_load_failed_using_fallback",
                    path=model_path,
                    error=str(exc),
                )
                self.session = None
                self.model_loaded = False
            else:
                raise

    async def predict(self, dicom_bytes: bytes) -> PredictionResponse:
        case_id = self._hash_bytes(dicom_bytes)
        log = self.logger.bind(request_id=case_id)
        log.info("inference_started")

        # 1. DICOM dekodieren
        ds = await asyncio.to_thread(pydicom.dcmread, BytesIO(dicom_bytes))

        # 2. Anonymisierungs-Check
        anon_service = AnonymizationService()
        is_anon, pii_found = await asyncio.to_thread(
            anon_service.check_only, dicom_bytes
        )
        if not is_anon:
            log.error(
                "non_anonymized_dicom_rejected",
                pii_tags=pii_found,
            )
            raise ValueError(
                f"Non-anonymized DICOM rejected. PII tags found: {pii_found}"
            )

        # 3. Preprocessing with proper HU windowing (carotid soft-tissue)
        pixel_array = ds.pixel_array.astype(np.float32)
        # Apply rescale slope/intercept if present
        slope = float(getattr(ds, "RescaleSlope", 1.0))
        intercept = float(getattr(ds, "RescaleIntercept", 0.0))
        hu_array = pixel_array * slope + intercept

        # Window/level to soft-tissue window optimized for carotid CTA
        settings = get_settings()
        input_array = await asyncio.to_thread(
            self._build_model_input_batch,
            hu_array,
            settings.enable_inference_tta,
        )

        # 4. Inference
        if self.session is None:
            log.error("inference_called_without_model")
            raise RuntimeError("ONNX model not loaded")

        input_name = self.session.get_inputs()[0].name
        outputs = await asyncio.to_thread(
            self.session.run, None, {input_name: input_array}
        )

        # 5. Postprocessing
        # Assumption: outputs[0]=segmentation, [1]=stenosis, [2]=vulnerability
        seg = self._sigmoid(outputs[0]).mean(axis=0, keepdims=True)
        stenosis_values = np.asarray(outputs[1], dtype=np.float32).reshape(
            input_array.shape[0], -1
        )[:, 0]
        stenosis = float(np.clip(np.mean(stenosis_values), 0.0, 100.0))
        vuln_raw = self._sigmoid(
            np.asarray(outputs[2], dtype=np.float32).reshape(input_array.shape[0], -1)
        ).mean(axis=0)
        vulnerability_markers = {
            "intraplaque_hemorrhage": float(vuln_raw[0]),
            "thin_fibrous_cap": float(vuln_raw[1]),
            "lipid_rich_necrotic_core": float(vuln_raw[2]),
            "systolic_motion_anomaly": float(vuln_raw[3]),
        }

        # 5.5 Confidence calibration
        raw_confidence = float(np.max(seg))
        confidence_bucket = "medium"
        calibrated = False
        if self._calibrator is not None and self._calibrator.is_fitted:
            try:
                calibrated_conf = self._calibrator.predict_proba(
                    np.array([raw_confidence * 10 - 5])  # rough logit approx
                )[0]
                raw_confidence = float(calibrated_conf)
                calibrated = True
            except Exception:
                pass
        confidence_bucket = ConfidenceCalibrationService().get_confidence_bucket(
            raw_confidence
        )

        # 6. Grad-CAM (optimized with fewer perturbation blocks for speed)
        heatmap = await asyncio.to_thread(
            generate_gradcam_heatmap,
            self.session,
            input_array,
            target_class=0,
            blocks=8,  # 8x8 = 64 evaluations instead of 256
        )
        heatmap_pil = Image.fromarray(heatmap)
        buffer = BytesIO()
        await asyncio.to_thread(heatmap_pil.save, buffer, format="PNG")
        heatmap_b64 = base64.b64encode(buffer.getvalue()).decode()

        # 7. Audit-Event
        audit_id = str(uuid.uuid4())
        if self.db_session_factory is not None:
            async with self.db_session_factory() as session:
                audit = AuditEvent(
                    event_type="inference",
                    actor="inference_service",
                    payload_json="{}",  # placeholder; real payload later
                )
                session.add(audit)
                await session.commit()

        log.info(
            "inference_completed",
            stenosis=stenosis,
            model_loaded=self.model_loaded,
        )

        return PredictionResponse(
            case_id=case_id,
            stenosis_pct_nascet=stenosis,
            confidence=raw_confidence,
            confidence_bucket=confidence_bucket,
            calibrated=calibrated,
            vulnerability_markers=vulnerability_markers,
            heatmap_b64=heatmap_b64,
            model_version=get_settings().model_version,
            model_sha=get_settings().model_sha or "unknown",
            audit_id=audit_id,
            captured_at=datetime.now(timezone.utc),
        )

    @staticmethod
    def _build_model_input_batch(
        hu_array: np.ndarray, enable_tta: bool = False
    ) -> np.ndarray:
        """Create one or more W/L-normalized model inputs.

        TTA is disabled by default and must be validated before clinical use.
        """
        import cv2

        windows = [(40.0, 400.0)]
        if enable_tta:
            windows.extend([(60.0, 360.0), (80.0, 500.0)])

        inputs = []
        for window_center, window_width in windows:
            low = window_center - window_width / 2
            high = window_center + window_width / 2
            windowed = np.clip(hu_array, low, high)
            normalised = (windowed - low) / (high - low)
            resized = cv2.resize(normalised, (512, 512), interpolation=cv2.INTER_LINEAR)
            inputs.append(resized[np.newaxis, :, :].astype(np.float32))
        return np.stack(inputs, axis=0)

    @staticmethod
    def _sigmoid(x: np.ndarray) -> np.ndarray:
        return 1.0 / (1.0 + np.exp(-x))

    def close(self) -> None:
        """Release ONNX Runtime session resources."""
        if hasattr(self, "session") and self.session is not None:
            try:
                self.session._model_meta  # force init if lazy
            except Exception:
                pass
            # ort.InferenceSession has no explicit close, but we can
            # release the reference and let GC handle it.
            self.session = None
            self.model_loaded = False
            self.logger.info("inference_service_closed")

    @staticmethod
    def _hash_bytes(data: bytes) -> str:
        return hashlib.sha256(data).hexdigest()
