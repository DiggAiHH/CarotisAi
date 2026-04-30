"""Export MFSD-UNet checkpoint to ONNX + benchmark.

Usage:
    python -m ml.inference.onnx_export \
        --checkpoint /data/checkpoints/best.pt \
        --output /models/mfsd_unet.onnx \
        --calibration-pkl /data/calibration.pkl
"""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import numpy as np
import onnx
from onnx import TensorProto, helper, numpy_helper


def _export_platt_onnx(calibrator, output_path: Path) -> None:
    """Export a fitted Platt-scaling calibrator to a standalone ONNX graph.

    Graph:
        raw_confidence -> Mul(coef) -> Add(intercept) -> Sigmoid -> calibrated_confidence
    """
    lr = calibrator._calibrator
    coef = float(lr.coef_[0][0])
    intercept = float(lr.intercept_[0])

    input_info = helper.make_tensor_value_info(
        "raw_confidence", TensorProto.FLOAT, [None, 1]
    )
    output_info = helper.make_tensor_value_info(
        "calibrated_confidence", TensorProto.FLOAT, [None, 1]
    )

    coef_tensor = numpy_helper.from_array(
        np.array([coef], dtype=np.float32), name="coef"
    )
    intercept_tensor = numpy_helper.from_array(
        np.array([intercept], dtype=np.float32), name="intercept"
    )

    mul_node = helper.make_node("Mul", ["raw_confidence", "coef"], ["scaled"])
    add_node = helper.make_node("Add", ["scaled", "intercept"], ["logits"])
    sigmoid_node = helper.make_node("Sigmoid", ["logits"], ["calibrated_confidence"])

    graph = helper.make_graph(
        [mul_node, add_node, sigmoid_node],
        "platt_calibration",
        [input_info],
        [output_info],
        initializer=[coef_tensor, intercept_tensor],
    )

    model = helper.make_model(graph)
    model.opset_import[0].version = 13
    model.ir_version = 8
    onnx.checker.check_model(model)
    onnx.save(model, str(output_path))


def export(args: argparse.Namespace) -> None:
    import torch

    from ml.models.mfsd_unet import MFSDUNet

    device = torch.device("cpu")  # ONNX export always on CPU
    model = MFSDUNet().to(device)

    ckpt = torch.load(args.checkpoint, map_location=device)
    model.load_state_dict(ckpt["model_state_dict"])
    model.eval()

    dummy = torch.zeros(1, 1, 512, 512, device=device)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print("[export] Exporting to ONNX …")
    torch.onnx.export(
        model,
        dummy,
        str(output_path),
        opset_version=17,
        input_names=["input"],
        output_names=["seg_main", "seg_ds1", "seg_ds2", "seg_ds3", "stenosis", "vuln"],
        dynamic_axes={"input": {0: "batch"}},
        do_constant_folding=True,
    )

    # Simplify
    import onnxsim

    print("[export] Simplifying ONNX graph …")
    model_onnx = onnx.load(str(output_path))
    onnx.checker.check_model(model_onnx)
    model_sim, ok = onnxsim.simplify(model_onnx)
    if ok:
        onnx.save(model_sim, str(output_path))
        print("[export] Simplified OK")
    else:
        print("[export] Simplification failed — keeping original")

    # Benchmark
    print("[export] Benchmarking (50 runs) …")
    import onnxruntime as ort

    opts = ort.SessionOptions()
    opts.intra_op_num_threads = 4
    sess = ort.InferenceSession(
        str(output_path), sess_options=opts, providers=["CPUExecutionProvider"]
    )
    dummy_np = np.zeros((1, 1, 512, 512), dtype=np.float32)

    times = []
    for _ in range(50):
        t0 = time.perf_counter()
        sess.run(None, {"input": dummy_np})
        times.append((time.perf_counter() - t0) * 1000)

    times.sort()
    p50 = times[len(times) // 2]
    p95 = times[int(len(times) * 0.95)]
    print(f"[benchmark] p50={p50:.1f}ms  p95={p95:.1f}ms")
    print(f"[export] Done → {output_path}")

    # Optional calibration export
    if args.calibration_pkl:
        cal_path = Path(args.calibration_pkl)
        if not cal_path.exists():
            raise FileNotFoundError(f"Calibration file not found: {cal_path}")

        try:
            from app.services.confidence_calibration_service import (
                ConfidenceCalibrationService,
            )
        except ImportError:
            import sys

            backend_dir = Path(__file__).resolve().parents[2] / "backend"
            if str(backend_dir) not in sys.path:
                sys.path.insert(0, str(backend_dir))
            from app.services.confidence_calibration_service import (
                ConfidenceCalibrationService,
            )

        cal = ConfidenceCalibrationService()
        cal.load(cal_path)

        stem = output_path.stem
        parent = output_path.parent

        if cal.method == "platt":
            cal_output = parent / f"{stem}_calibration.onnx"
            _export_platt_onnx(cal, cal_output)
            print(f"[export] Calibration exported to {cal_output}")
        else:
            print(
                "[export] WARNING: Isotonic ONNX export not yet implemented. "
                "Fallback: Python post-processing."
            )

        meta = {
            "calibration_method": cal.method,
            "calibration_version": "1.0.0",
            "ece": cal.metrics.ece if cal.metrics else None,
            "mce": cal.metrics.mce if cal.metrics else None,
            "brier": cal.metrics.brier if cal.metrics else None,
            "is_fitted": cal.is_fitted,
        }
        meta_path = parent / f"{stem}_calibration_meta.json"
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(meta, f, indent=2)
        print(f"[export] Calibration meta saved to {meta_path}")


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Export MFSD-UNet to ONNX")
    p.add_argument("--checkpoint", required=True)
    p.add_argument("--output", default="/models/mfsd_unet.onnx")
    p.add_argument("--calibration-pkl", default=None)
    return p.parse_args()


if __name__ == "__main__":
    export(_parse_args())
