from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest


def test_dynamic_quantization_export_creates_int8_model(tmp_path: Path):
    pytest.importorskip("onnxruntime")
    pytest.importorskip("sympy")

    import onnx
    from onnx import TensorProto, helper, numpy_helper

    from ml.inference.onnx_export import _quantize_dynamic_onnx

    input_info = helper.make_tensor_value_info("input", TensorProto.FLOAT, [None, 4])
    output_info = helper.make_tensor_value_info("output", TensorProto.FLOAT, [None, 2])
    weight = numpy_helper.from_array(np.ones((4, 2), dtype=np.float32), name="weight")
    matmul = helper.make_node("MatMul", ["input", "weight"], ["output"])
    graph = helper.make_graph(
        [matmul],
        "quantization_smoke",
        [input_info],
        [output_info],
        initializer=[weight],
    )
    model = helper.make_model(graph)
    model.opset_import[0].version = 17
    model.ir_version = 8

    fp32_path = tmp_path / "model.onnx"
    int8_path = tmp_path / "model.int8.onnx"
    onnx.save(model, str(fp32_path))

    _quantize_dynamic_onnx(fp32_path, int8_path)

    assert int8_path.exists()
    quantized = onnx.load(str(int8_path))
    op_types = {node.op_type for node in quantized.graph.node}
    assert "MatMulInteger" in op_types or "DynamicQuantizeLinear" in op_types
