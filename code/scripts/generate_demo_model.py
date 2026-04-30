"""Generate a minimal demo ONNX model for Carotis-AI local demos.

This creates a lightweight substitute for the real MFSD-UNet model so the
full stack can be demonstrated without a trained model.

The ONNX graph replicates the production contract EXACTLY:
  Input  : "input"         — (1, 1, 512, 512) float32
  Output : "segmentation"  — (1, 1, 512, 512) float32  (Sigmoid activation)
           "stenosis"      — (1, 1)            float32  (NASCET % in 0-100 range)
           "vulnerability" — (1, 4)            float32  (marker probabilities)

Stenosis is derived from GlobalAveragePool(input) × 65.0, so different DICOM
inputs produce different (but reproducible) numeric results.

Usage:
    python scripts/generate_demo_model.py
    python scripts/generate_demo_model.py --output data/models/mfsd_unet.onnx
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


# ---------------------------------------------------------------------------
# Ensure the lightweight `onnx` package is available without requiring the
# caller to pre-install it (it is NOT a runtime dependency of the backend).
# ---------------------------------------------------------------------------
def _ensure_onnx() -> None:
    try:
        import onnx  # noqa: F401
    except ImportError:
        print("  [setup] onnx not found — installing (one-time, ~20 MB)...")
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "onnx>=1.14.0", "--quiet"]
        )
        print("  [setup] onnx installed.")


def build_demo_model(output_path: Path) -> None:
    """Construct and save the demo ONNX model."""
    _ensure_onnx()

    import numpy as np
    from onnx import TensorProto, checker, helper, numpy_helper, save

    # ---- Inputs / outputs ------------------------------------------------
    inp = helper.make_tensor_value_info("input", TensorProto.FLOAT, [1, 1, 512, 512])
    out_seg = helper.make_tensor_value_info(
        "segmentation", TensorProto.FLOAT, [1, 1, 512, 512]
    )
    out_sten = helper.make_tensor_value_info("stenosis", TensorProto.FLOAT, [1, 1])
    out_vuln = helper.make_tensor_value_info("vulnerability", TensorProto.FLOAT, [1, 4])

    # ---- Initializers (constants embedded in the graph) ------------------
    # Scale factor for stenosis output
    scale_val = numpy_helper.from_array(
        np.array([65.0], dtype=np.float32), name="scale_65"
    )
    # Stenosis Reshape target: [1, 1]
    sten_shape_val = numpy_helper.from_array(
        np.array([1, 1], dtype=np.int64), name="sten_shape"
    )
    # Fixed vulnerability marker probabilities (plausible demo values)
    vuln_val = numpy_helper.from_array(
        np.array([[0.35, 0.28, 0.42, 0.18]], dtype=np.float32), name="vuln_const"
    )

    # ---- Nodes -----------------------------------------------------------
    nodes = [
        # segmentation: Sigmoid(input) → plausible-looking mask
        helper.make_node("Sigmoid", inputs=["input"], outputs=["segmentation"]),
        # stenosis: GAP(input) → (1,1,1,1) → Mul by 65 → Reshape to (1,1)
        helper.make_node("GlobalAveragePool", inputs=["input"], outputs=["gap_out"]),
        helper.make_node(
            "Mul", inputs=["gap_out", "scale_65"], outputs=["sten_scaled"]
        ),
        helper.make_node(
            "Reshape", inputs=["sten_scaled", "sten_shape"], outputs=["stenosis"]
        ),
        # vulnerability: identity from initializer constant
        helper.make_node("Identity", inputs=["vuln_const"], outputs=["vulnerability"]),
    ]

    graph = helper.make_graph(
        nodes,
        "mfsd_unet_demo",
        [inp],
        [out_seg, out_sten, out_vuln],
        initializer=[scale_val, sten_shape_val, vuln_val],
    )

    model = helper.make_model(
        graph,
        opset_imports=[helper.make_opsetid("", 17)],
        doc_string=(
            "Carotis-AI MFSD-UNet DEMO model — "
            "same I/O signature as production, non-clinical outputs. "
            "Replace with trained weights for clinical use."
        ),
    )
    model.ir_version = 8

    checker.check_model(model)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    save(model, str(output_path))
    size_kb = output_path.stat().st_size // 1024
    print(f"  [ok] Demo model saved -> {output_path}  ({size_kb} KB)")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate Carotis-AI demo ONNX model")
    parser.add_argument(
        "--output",
        default="data/models/mfsd_unet.onnx",
        help="Output path for the .onnx file (default: data/models/mfsd_unet.onnx)",
    )
    args = parser.parse_args()

    output_path = Path(args.output)
    if not output_path.is_absolute():
        # Resolve relative to the code/ directory (parent of scripts/)
        root = Path(__file__).parent.parent
        output_path = root / output_path

    print(f"Generating Carotis-AI demo ONNX model -> {output_path}")
    build_demo_model(output_path)


if __name__ == "__main__":
    main()
