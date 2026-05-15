import cv2
import numpy as np
from typing import Dict, Any, Tuple

class VisionQAEngine:
    """
    Experimental Computer Vision engine for automated QA in digital media and document publishing.
    Detects layout shifts, font blurring, color calibration drift, and boundary distortions.
    """

    @staticmethod
    def compare_frames(template: np.ndarray, candidate: np.ndarray) -> Dict[str, Any]:
        # Resize to match template if dimensions slightly differ
        if template.shape != candidate.shape:
            candidate = cv2.resize(candidate, (template.shape[1], template.shape[0]))

        # 1. Grayscale & Absolute Difference
        gray_template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
        gray_candidate = cv2.cvtColor(candidate, cv2.COLOR_BGR2GRAY)
        diff = cv2.absdiff(gray_template, gray_candidate)

        # 2. Thresholding to detect distinct anomalies
        _, thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # 3. Calculate Normalized Mean Squared Error (MSE)
        mse = np.mean((gray_template.astype("float") - gray_candidate.astype("float")) ** 2)

        # 4. Color Histogram Drift (B, G, R correlation)
        hist_correlations = []
        for channel in range(3):
            hist_t = cv2.calcHist([template], [channel], None, [256], [0, 256])
            hist_c = cv2.calcHist([candidate], [channel], None, [256], [0, 256])
            cv2.normalize(hist_t, hist_t, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
            cv2.normalize(hist_c, hist_c, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
            corr = cv2.compareHist(hist_t, hist_c, cv2.HISTCMP_CORREL)
            hist_correlations.append(float(corr))

        avg_color_corr = float(np.mean(hist_correlations))

        # Evaluate Pass/Fail status
        passed = bool(mse < 15.0 and avg_color_corr > 0.95 and len(contours) < 3)

        return {
            "passed": passed,
            "mean_squared_error": round(float(mse), 3),
            "color_histogram_correlation": round(avg_color_corr, 4),
            "anomaly_contours_detected": len(contours),
            "assessment": "PERFECT_MATCH" if mse == 0 else ("ACCEPTABLE_TOLERANCE" if passed else "DEFECT_DETECTED")
        }
