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
    """
    
    # call crop on the image using roi
    # call preprocess
    # call get line center on preprocessed image
    # subtract line center from image center to get error
    # normalize the error based on the width of the input image
    pass


def _crop(img: np.ndarray, bottom: float, top: float) -> np.ndarray:
    """
    Crops the image vertically between the given proportional bounds.

    See `calc_error` for more details on how the crop parameters are used.

    Args:
        img (np.ndarray): The input image.
        bottom (float): Lower vertical bound (0.0 = bottom, 1.0 = top).
        top (float): Upper vertical bound. Must be greater than `bottom`.

    Returns:
        np.ndarray: The cropped image.
    """
    pass


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

    # Use a contour finding algorithm (built into OpenCV)
    # Might have to filter contours to get the one that is the line
    # Return the vertical center of the contour

    # Below is a rather "dumbed down" approach that takes the average of a binary image
    # I left it here so you can visualize the result of running the script
    # Maybe it will work well enough?? IDK

    # We should handle cases where the line isn't in the image
    # ie length(rows)/length(img) is below some threshold
    rows, cols = np.where(img == 255)
    return np.round(np.mean(cols), 0)


if __name__ == "__main__":
    # This main function can be used for testing and visualizing
    # the effects of our various funcitons as well as the processing time

    # Load an image based on path
    image = np.load("test_images/no_light/right_straight_crack.npy")

    start = time.time()
    processed_img = __preprocess(image)
    line_center = __get_line_center_x(processed_img)
    print("Processing time: ", np.round(time.time()-start, 6))

    import matplotlib.pyplot as plt

    # Visualize the image with the detected center of the line
    plt.imshow(image)
    plt.axvline(x=np.mean(line_center), color='red',
                linewidth=2)  # Vertical line at x position
    plt.show()

    # Visualize intermediate step
    # Press any key in preview window to exit
    cv2.imshow('img', processed_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
