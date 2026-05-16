import cv2
import numpy as np

def extract_particles(binary_img):
    contours, _ = cv2.findContours(binary_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    areas = []
    for c in contours:
        area = cv2.contourArea(c)
        if area > 5:  # filter noise
            areas.append(area)

    return np.array(areas)

def compute_features(areas):
    if len(areas) == 0:
        return {
            "count": 0,
            "avg_size": 0,
            "variance": 0,
            "density": 0
        }

    return {
        "count": len(areas),
        "avg_size": float(np.mean(areas)),
        "variance": float(np.var(areas)),
        "density": len(areas)  # 简化版
    }