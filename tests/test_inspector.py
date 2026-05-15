import numpy as np
from app.engine.inspector import VisionQAEngine

def test_identical_images():
    img = np.zeros((100, 100, 3), dtype=np.uint8)
    res = VisionQAEngine.compare_frames(img, img)
    assert res["passed"] is True
    assert res["mean_squared_error"] == 0.0
    assert res["assessment"] == "PERFECT_MATCH"

def test_anomaly_detection():
    img1 = np.zeros((100, 100, 3), dtype=np.uint8)
    img2 = img1.copy()
    img2[40:60, 40:60] = 255  # Distinct white square artifact
    res = VisionQAEngine.compare_frames(img1, img2)
    assert res["passed"] is False
    assert res["assessment"] == "DEFECT_DETECTED"
    assert res["anomaly_contours_detected"] >= 1
