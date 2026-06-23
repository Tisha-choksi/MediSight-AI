import torch
import time
import numpy as np


class DeploymentOptimizationAgent:
    def __init__(self):
        self.results = {}

    def optimize(self, model: torch.nn.Module, input_shape=(1, 3, 224, 224)) -> dict:
        dummy_input = torch.randn(input_shape)
        self.results["pytorch"] = self._benchmark(model, dummy_input)

        onnx_path = "model.onnx"
        self._export_onnx(model, dummy_input, onnx_path)
        self.results["onnx"] = self._benchmark_onnx(onnx_path, dummy_input)

        return self.results

    def _export_onnx(self, model: torch.nn.Module, dummy_input, path: str):
        torch.onnx.export(model, dummy_input, path,
                          input_names=["input"], output_names=["output"],
                          dynamic_axes={"input": {0: "batch_size"}})

    def _benchmark(self, model: torch.nn.Module, dummy_input) -> dict:
        model.eval()
        start = time.time()
        with torch.no_grad():
            for _ in range(100):
                model(dummy_input)
        avg_latency = (time.time() - start) / 100 * 1000
        return {"latency_ms": round(avg_latency, 2)}

    def _benchmark_onnx(self, onnx_path: str, dummy_input) -> dict:
        import onnxruntime as ort
        session = ort.InferenceSession(onnx_path)
        start = time.time()
        for _ in range(100):
            session.run(None, {"input": dummy_input.numpy()})
        avg_latency = (time.time() - start) / 100 * 1000
        return {"latency_ms": round(avg_latency, 2)}
