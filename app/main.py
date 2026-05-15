from fastapi import FastAPI
from .engine.inspector import VisionQAEngine
import numpy as np

app = FastAPI(
    title="vision-qa-lab",
    description="Learning experiments in automated computer vision quality inspection.",
    version="1.0.0"
)

@app.get("/health")
def health():
    return {"status": "HEALTHY", "engine": "OpenCV-based VisionQA"}

@app.get("/api/v1/demo/benchmark")
def run_synthetic_benchmark():
    # Generate clean reference canvas
    template = np.zeros((300, 300, 3), dtype=np.uint8)
    template[:, :] = (245, 245, 245)

    # Candidate with a small simulated anomaly (e.g. minor text misalignment)
    candidate = template.copy()
    candidate[100:105, 100:150] = (20, 20, 20)

    result = VisionQAEngine.compare_frames(template, candidate)
    return {"benchmark_scenario": "Simulated Misprint Contamination", "results": result}
