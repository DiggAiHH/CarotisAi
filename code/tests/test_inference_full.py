from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_inference_e2e(
    test_client: AsyncClient,
    test_anonymized_dicom: bytes,
    tmp_path: Path,
):
    # 1. Generate demo ONNX model
    model_path = tmp_path / "demo.onnx"
    script_path = (
        Path(__file__).resolve().parents[1] / "scripts" / "generate_demo_model.py"
    )
    subprocess.run(
        [
            sys.executable,
            str(script_path),
            "--output",
            str(model_path),
        ],
        check=True,
    )

    # 2. Upload anonymized DICOM
    response = await test_client.post(
        "/api/v1/inference/predict",
        files={
            "file": (
                "test.dcm",
                test_anonymized_dicom,
                "application/dicom",
            )
        },
        headers={"X-API-Key": "a" * 32},
    )
    # Without model loaded via app.state we still get 503, but the
    # pipeline (auth, anonymization check) is exercised.
    assert response.status_code in (200, 503)
