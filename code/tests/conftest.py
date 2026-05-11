from __future__ import annotations

import os

# Force in-memory SQLite for ALL tests — prevents stale on-disk DB from leaking
# into tests that don't use the test_client fixture. Must run before any
# app.core.config.get_settings() call (i.e. before any app import).
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"
os.environ.setdefault("API_KEY", "a" * 32)
os.environ.setdefault("ADMIN_API_KEY", "b" * 32)
os.environ.setdefault("ANONYMIZATION_SALT", "s" * 32)
os.environ.setdefault("DEBUG", "true")

import numpy as np
import pydicom
import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from unittest.mock import AsyncMock, MagicMock

from app.core.config import get_settings
from app.schemas.inference import PredictionResponse


@pytest_asyncio.fixture
async def test_client(monkeypatch):
    monkeypatch.setenv("API_KEY", "a" * 32)
    monkeypatch.setenv("ADMIN_API_KEY", "b" * 32)
    monkeypatch.setenv("ANONYMIZATION_SALT", "s" * 32)
    monkeypatch.setenv("DATABASE_URL", "sqlite+aiosqlite:///:memory:")
    monkeypatch.setenv("ONNX_MODEL_PATH", "/tmp/fake.onnx")
    monkeypatch.setenv("DEBUG", "true")
    get_settings.cache_clear()

    from app.db.database import get_engine, reset_db
    from app.main import create_app

    get_engine.cache_clear()
    app = create_app()
    await reset_db()
    mock_svc = MagicMock()
    mock_svc.model_loaded = True
    mock_svc.predict = AsyncMock(
        return_value=PredictionResponse(
            case_id="abc123",
            stenosis_pct_nascet=50.0,
            confidence=0.9,
            vulnerability_markers={},
            heatmap_b64=None,
            model_version="v0.0.0",
            model_sha="abc123",
            audit_id="audit-1",
            captured_at="2026-04-28T12:00:00Z",
        )
    )
    app.state.inference_service = mock_svc

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client


@pytest_asyncio.fixture
async def clean_db(monkeypatch):
    """Isolated in-memory DB fixture for tests that bypass test_client."""
    monkeypatch.setenv("API_KEY", "a" * 32)
    monkeypatch.setenv("ADMIN_API_KEY", "b" * 32)
    monkeypatch.setenv("ANONYMIZATION_SALT", "s" * 32)
    monkeypatch.setenv("DATABASE_URL", "sqlite+aiosqlite:///:memory:")
    monkeypatch.setenv("ONNX_MODEL_PATH", "/tmp/fake.onnx")
    monkeypatch.setenv("DEBUG", "true")
    get_settings.cache_clear()

    from app.db.database import get_engine, reset_db

    get_engine.cache_clear()
    await reset_db()
    yield
    get_engine.cache_clear()


@pytest.fixture
def test_dicom_bytes() -> bytes:
    ds = pydicom.Dataset()
    ds.PatientName = "Test Patient"
    ds.PatientID = "12345"
    ds.Rows = 256
    ds.Columns = 256
    ds.BitsAllocated = 16
    ds.BitsStored = 16
    ds.PixelRepresentation = 0
    ds.SamplesPerPixel = 1
    ds.PhotometricInterpretation = "MONOCHROME2"
    ds.PixelData = np.zeros((256, 256), dtype=np.uint16).tobytes()
    buffer = pydicom.filebase.DicomBytesIO()
    pydicom.dcmwrite(buffer, ds, little_endian=True, implicit_vr=False)
    return buffer.parent.getvalue()


@pytest.fixture
def test_anonymized_dicom() -> bytes:
    ds = pydicom.Dataset()
    ds.Rows = 256
    ds.Columns = 256
    ds.BitsAllocated = 16
    ds.BitsStored = 16
    ds.PixelRepresentation = 0
    ds.SamplesPerPixel = 1
    ds.PhotometricInterpretation = "MONOCHROME2"
    ds.PixelData = np.zeros((256, 256), dtype=np.uint16).tobytes()
    buffer = pydicom.filebase.DicomBytesIO()
    pydicom.dcmwrite(buffer, ds, little_endian=True, implicit_vr=False)
    return buffer.parent.getvalue()


@pytest.fixture
def mock_inference_service(monkeypatch):
    mock = MagicMock()
    mock.predict = AsyncMock(
        return_value=PredictionResponse(
            case_id="abc123",
            stenosis_pct_nascet=50.0,
            confidence=0.9,
            vulnerability_markers={},
            heatmap_b64=None,
            model_version="v0.0.0",
            model_sha="abc123",
            audit_id="audit-1",
            captured_at="2026-04-28T12:00:00Z",
        )
    )

    def mock_init(*args, **kwargs):
        return mock

    monkeypatch.setattr("app.main.InferenceService", mock_init)
    return mock
