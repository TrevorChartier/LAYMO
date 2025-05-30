"""Provides the CameraManager class for capturing frames from the 
PiCamera.

Usage:
        camera = CameraManager()
        frame = camera.get_latest_frame()
"""


from picamera2 import Picamera2
from libcamera import ColorSpace
import numpy as np

from laymo import params

class CameraManager:
    """Manages PiCamera initialization and frame capture."""

    def __init__(self):
        self.__camera = Picamera2()

        camera_config = self.__camera.create_video_configuration(
            main={
                "size": (params.FRAME_WIDTH, params.FRAME_HEIGHT),
                "format": "RGB888"
            },
            controls={
                # Request 50 FPS
                "FrameDurationLimits": (int(1e6 / 50), int(1e6 / 50))  
            },
            colour_space=ColorSpace.Sycc()
        )

        self.__camera.configure(camera_config)
        self.__camera.start()

    def get_latest_frame(self) -> np.ndarray:
        """Retrieve the most recent frame.

        Returns: 
            np.ndarray: Copy of latest frame as a numpy array
        """
        return self.__camera.capture_array()
