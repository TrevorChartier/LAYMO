""" 
This module defines the functions necessary for detecting how far the
center of a blue line is from the center of an img.
"""
import numpy as np
import cv2
import time


def calc_error(img: np.ndarray, roi: tuple[float, float]):
    """
    Calculates a normalized error value representing how far the detected line is from the horizontal center 
    of the image within a specified vertical region of interest (ROI).

    Args:
        img (np.ndarray): The input image in which to detect the line.
        roi (tuple of float): A tuple (bottom, top) specifying the vertical region of interest as proportional 
                              values between 0.0 and 1.0. 
                              - `bottom` defines the lower vertical bound of the ROI (0.0 = bottom of the image).
                              - `top` defines the upper vertical bound of the ROI (1.0 = top of the image).

    Returns:
        float: A normalized error value in the range [-1, 1], where:
               -1.0 indicates the line is at the far left,
                0.0 indicates the line is perfectly centered,
                1.0 indicates the line is at the far right.
        None: If no line is detected in the image

    Raises:
        ValueError: bottom must be less than top, and both must be within the range [0, 1].
    """
    cropped_img = __crop(img, bottom=roi[0], top=roi[1])
    processed_img = __preprocess(cropped_img)
    line_center = __get_line_center_x(processed_img)

    if line_center is None:
        return None  # No line in frame

    frame_center = img.shape[1] // 2
    error = line_center - frame_center
    normalized_error = error / frame_center  # Scale to range [-1,1]
    return np.round(normalized_error, 2)


def visualize(img: np.ndarray, roi: tuple[float, float]):
    """ 
    Display the image and overlay the calculated line center for visualization
    and debugging

    Args:
        Takes the same parameters as `calc_error`

    Additional Dependency: 
        matplotlib
    """
    import matplotlib.pyplot as plt

    start = time.time()
    err = calc_error(img=img, roi=roi)
    print("Processing time: ", np.round(time.time()-start, 6))
    print("Error: ", err)

    if err is not None:
        # Recalculate line center from error value
        line_center = err * (img.shape[1] // 2) + img.shape[1]//2
        plt.imshow(img)
        plt.axvline(x=np.mean(line_center), color='red',
                    linewidth=2)  # Vertical line at x position
        plt.show()
    else:
        print("No Line")


def __crop(img: np.ndarray, bottom: float, top: float) -> np.ndarray:
    """
    Crops the image vertically between the given proportional bounds.

    See `calc_error` for more details on how the crop parameters are used.

    Args:
        img (np.ndarray): The input image.
        bottom (float): Lower vertical bound (0.0 = bottom, 1.0 = top).
        top (float): Upper vertical bound. Must be greater than `bottom`.

    Returns:
        np.ndarray: The cropped image.

    Raises:
        ValueError: See `calc_error`
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


def __preprocess(img: np.ndarray) -> np.ndarray:
    """Converts (BGR) image to a binary image based on blue channel"""
    img = cv2.GaussianBlur(img, (23, 23), 0)
    threshold = 220
    img = img[:, :, 0]
    img[img >= threshold] = 255
    img[img < threshold] = 0
    return img


def __get_line_center_x(img: np.ndarray) -> int:
    """"
    Computes the horizontal center (x-coordinate) of the bounding box that contains
    a blue line in the img.

    Args:
        img (np.ndarray): A 3D NumPy array representing the input img. The
        img is expected to contain a single prominent blue line.

    Returns:
        int: The column index of the center of the bounding box surrounding the
        detected line in the img.

    """
    rows, cols = np.where(img == 255)
    if cols.size < .03 * img.size:
        return None  # Line is probably not in frame
    return np.round(np.mean(cols), 0)
