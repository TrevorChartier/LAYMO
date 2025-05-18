"""Functions for detecting the horizontal offset of a blue line's 
center in an image.

The module processes an image to determine how far the center of a
detected blue line is from the image's horizontal center within a
specified vertical region of interest.
"""

import numpy as np
import cv2

from laymo import params


class LineNotDetected(Exception):
    """Raised when the blue line is not detected or insufficient
    pixels are found.
    """



class BadFrame(Exception):
    """Raised when too many pixels are detected, indicating a
    corrupted or invalid frame.
    """


def calc_error(img: np.ndarray, roi: tuple[float, float]) -> float:
    """Gets error of the blue line center relative to the image center.
    
    Calculates a normalized error value representing how far the
    detected line is from the horizontal center of the image within
    a specified vertical region of interest (ROI).

    Args:
        img (np.ndarray): Input image (BGR).
        roi (tuple[float, float]): Vertical region of interest as
            (bottom, top) proportions, where 0.0 is bottom and 1.0 is
            top of the image. Must satisfy 0 ≤ bottom < top ≤ 1.

   Returns:
        float: Normalized error in [-1, 1], where -1 is far left, 0 is
            center, and 1 is far right.

    Raises:
        ValueError: bottom must be less than top, 
            and both must be within the range [0, 1].
        LineNotDetected: If no line is detected.
        BadFrame: If frame is invalid.
    """
    cropped_img = __crop(img, bottom=roi[0], top=roi[1])
    processed_img = preprocess(cropped_img)
    line_center = __get_line_center_x(processed_img)

    frame_center = img.shape[1] // 2
    error = line_center - frame_center
    normalized_error = error / frame_center  # Scale to range [-1,1]
    return np.round(normalized_error, 2)


def __crop(img: np.ndarray, bottom: float, top: float) -> np.ndarray:
    """Vertically crops the image between the proportional bounds.

    See `calc_error` for more details on how the crop parameters are used.

    Args:
        img (np.ndarray): Input image.
        bottom (float): Lower vertical bound (0.0 = bottom).
        top (float): Upper vertical bound (1.0 = top), must be > bottom.

    Returns:
        np.ndarray: Cropped image.

    Raises:
        ValueError: If bounds are not within [0, 1] or bottom ≥ top.
    """
    if (bottom >= top or bottom < 0 or bottom > 1 or top < 0 or top > 1):
        raise ValueError(
            "Invalid crop parameters: expected 0 ≤ bottom < top ≤ 1."
        )

    img_height = img.shape[0]
    bottom_row = img_height - (int)(img_height * bottom)
    top_row = img_height - (int)(img_height * top)

    cropped_img = img[top_row:bottom_row, :]
    return cropped_img


def preprocess(img: np.ndarray) -> np.ndarray:
    """Converts (BGR) image to a binary image based on blue channel

    Args:
        img (np.ndarray): Input BGR image.

    Returns:
        np.ndarray: Binary image with white pixels indicating blue areas.
    """
    img = cv2.GaussianBlur(img, (23, 23), 0)
    img = img[:, :, 0]
    img[img >= params.BINARY_THRESHOLD] = 255
    img[img < params.BINARY_THRESHOLD] = 0
    return img


def __get_line_center_x(img: np.ndarray) -> int:
    """Compute horizontal center of the detected blue line in a binary image.

    Args:
        img (np.ndarray): Binary image where line pixels are 255.

    Returns:
        int: X-coordinate of the line center.

    Raises:
        LineNotDetected: If detected line pixels are below minimum threshold.
        BadFrame: If detected pixels exceed maximum threshold, 
            indicating invalid frame.
    """
    rows, cols = np.where(img == 255)
    if cols.size < params.MIN_LINE_THRESHOLD * img.size:
        raise LineNotDetected()
    if cols.size > params.MAX_LINE_THRESHOLD * img.size:
        raise BadFrame()
    return np.round(np.mean(cols), 0)
