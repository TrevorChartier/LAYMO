""" 
This module defines the functions necessary for detecting how far the
center of a blue line is from the center of an image.
"""
import numpy as np


def calc_error(image: np.ndarray):
    pass


def _crop_frame(image: np.ndarray) -> np.ndarray:
    pass


def _get_line_center_x(image: np.ndarray) -> int:
    """"
    Computes the horizontal center (x-coordinate) of the bounding box that contains
    a blue line in the image.

    Args:
        image (np.ndarray): A 3D NumPy array representing the input image. The
        image is expected to contain a single prominent blue line.
    
    Returns:
        int: The column index of the center of the bounding box surrounding the
        detected line in the image.
    
    """
    pass 