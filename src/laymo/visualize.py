""" This module is for generating visualizations of frame and error for  logs """

import numpy as np
import cv2
import matplotlib.pyplot as plt

from laymo.line_detector import preprocess
from laymo.params import Params

def visualize(img: np.ndarray, error: float, steering: float = None) -> np.ndarray:
    roi = Params.ROI_STEER
    img_h, img_w = img.shape[:2]

    # Preprocess and convert grayscale to color for blending
    processed = preprocess(img)
    processed_rgb = cv2.cvtColor(processed, cv2.COLOR_GRAY2BGR)

    # Blend preprocessed image with original image
    overlay = cv2.addWeighted(processed_rgb, 0.9, img, 0.8, 0)

    # Draw horizontal lines for ROI
    y1 = int(img_h * (1 - roi[0]))
    y2 = int(img_h * (1 - roi[1]))
    cv2.line(overlay, (0, y1), (img_w, y1), (0, 255, 0), 2)
    cv2.line(overlay, (0, y2), (img_w, y2), (0, 255, 0), 2)

    # Draw vertical line for error (center)
    if error is not None:
        center_x = int(error * (img_w // 2) + img_w // 2)
        cv2.line(overlay, (center_x, 0), (center_x, img_h), (0, 0, 255), 2)

    # Add Data as Text
    cv2.putText(overlay, f"Error: {error}", (10, 28), cv2.FONT_HERSHEY_SIMPLEX,
                0.6, (255, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(overlay, f"Steering: {steering}", (10, 62), cv2.FONT_HERSHEY_SIMPLEX,
                0.6, (255, 0, 0), 2, cv2.LINE_AA)

    return overlay