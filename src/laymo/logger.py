""" This module implements the Logger class """

import cv2

from laymo.params import Params

class Logger():
    """ Handles video logging and visualization of the Laymo car's perception and control outputs."""
    def __init__(self, path):
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')  
        self.writer = cv2.VideoWriter('data/output_video.mp4',
                              fourcc, 50.0,
                              (Params.FRAME_WIDTH, Params.FRAME_HEIGHT)
                              )
        
    def write(self, frame):
        self.writer.write(frame)
        
    def close(self):
        if self.writer.isOpened():
            self.writer.release()
