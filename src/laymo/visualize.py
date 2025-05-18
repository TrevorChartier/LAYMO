"""Provides visualization utilities for overlaying image processing 
results and control metrics.
"""

import numpy as np
import cv2

from laymo.line_detector import preprocess
from laymo.params import Params


def visualize(
    img: np.ndarray, error: float | None, steering: float | None = None
) -> np.ndarray:
    """Creates a visual overlay on the input image showing the steering
    region of interest (ROI),the detected line error relative to the image
    center, and optional steering information.

    Args:
        img (np.ndarray): Original color image frame (BGR) to annotate.
        error (float | None, optional): Normalized lateral error of 
            detected line in range [-1, 1].
        steering (float | None, optional): Current steering command.
            Defaults to None.

    Returns:
        np.ndarray: Annotated image with ROI lines, error position, and
            steering text overlayed.
    """
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

    # Draw vertical line for error
    if error is not None:
        center_x = int(error * (img_w // 2) + img_w // 2)
        cv2.line(overlay, (center_x, 0), (center_x, img_h), (0, 0, 255), 2)

    # Add Metrics
    cv2.putText(
        overlay, f"Error: {error}", (10, 28),
        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2, cv2.LINE_AA
    )
    cv2.putText(
        overlay, f"Steering: {steering}", (10, 62),
        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2, cv2.LINE_AA
    )

    return overlay
