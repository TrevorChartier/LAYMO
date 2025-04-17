""" 
Class for configuring and capturing frames from PiCamera

Usage:
    camera = CameraManager()
    frame = CameraManager.get_latest_frame()
"""
from picamera2 import Picamera2
from libcamera import ColorSpace
import numpy as np

class CameraManager:
    
    def __init__(self):
        self.__camera = Picamera2()
        
        # Could play around with .align_configuration() for speed?
        camera_config = self.__camera.create_video_configuration(
            colour_space=ColorSpace.Sycc(),
            main={
                "size": (640, 480),
                "format": "RGB888",
                },
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

                