from __future__ import annotations

import asyncio
import base64
import hashlib
import uuid
from datetime import datetime, timezone
from io import BytesIO

import numpy as np
import onnxruntime as ort
import pydicom
import structlog
from PIL import Image
from sqlalchemy.ext.asyncio import async_sessionmaker

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
        import os

        cal_path = os.path.join(os.path.dirname(model_path), "calibration.pkl")
        if os.path.exists(cal_path):
            self._calibrator = ConfidenceCalibrationService()
            self._calibrator.load(cal_path)
            self.logger.info("calibration_loaded", path=cal_path)

        try:
            self.session = ort.InferenceSession(model_path)
            self.model_loaded = True
            self.logger.info("model_loaded", path=model_path)
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

        # 3. Preprocessing
        pixel_array = ds.pixel_array.astype(np.float32)
        pixel_array = (pixel_array - pixel_array.min()) / (
            pixel_array.max() - pixel_array.min() + 1e-8
        )
        img = Image.fromarray(pixel_array)
        img_resized = await asyncio.to_thread(img.resize, (512, 512))
        pixel_array = np.array(img_resized)
        input_array = pixel_array[np.newaxis, np.newaxis, :, :]  # NCHW

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
        seg = self._sigmoid(outputs[0])
        stenosis = float(np.clip(outputs[1][0], 0.0, 100.0))
        vuln_raw = self._sigmoid(outputs[2][0])
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

        # 6. Grad-CAM
        heatmap = await asyncio.to_thread(
            generate_gradcam_heatmap,
            self.session,
            input_array,
            target_class=0,
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
            model_version="v0.3.2",
            model_sha="abc123d",
            audit_id=audit_id,
            captured_at=datetime.now(timezone.utc),
        )

    @staticmethod
    def _sigmoid(x: np.ndarray) -> np.ndarray:
        return 1.0 / (1.0 + np.exp(-x))

    @staticmethod
    def _hash_bytes(data: bytes) -> str:
        return hashlib.sha256(data).hexdigest()
