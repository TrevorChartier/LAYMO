"""This module implements the CameraManager class"""

from picamera2 import Picamera2
from libcamera import ColorSpace
import numpy as np

from laymo.params import Params

class CameraManager:
    """ 
    Class for configuring and capturing frames from PiCamera

    Usage:
        camera = CameraManager()
        frame = CameraManager.get_latest_frame()
    """
    def __init__(self):
        self.__camera = Picamera2()

        # Could play around with .align_configuration() for speed?
        camera_config = self.__camera.create_video_configuration(
            main={
                "size": (Params.FRAME_WIDTH, Params.FRAME_HEIGHT),
                "format": "RGB888"
            },
            controls={
                "FrameDurationLimits": (int(1e6 / 50), int(1e6 / 50))  # Request 50 FPS
            },
            colour_space=ColorSpace.Sycc()
        )

        self.__camera.configure(camera_config)
        self.__camera.start()

    def get_latest_frame(self) -> np.ndarray:
        """
        Retrieve the most recent frame

        Returns: 
            frame (np.ndarray): Copy of latest frame as a numpy array
        """
        return self.__camera.capture_array()
