import matplotlib.pyplot as plt
import time
import numpy as np
import cv2

from laymo.camera_manager import CameraManager
from laymo.line_detector import calc_error, preprocess, BadFrame, LineNotDetected
from laymo.params import Params
from laymo.pid import PID
from laymo.visualize import visualize

cam = CameraManager()
steering_controller = PID(
    kp=Params.KP_STEER, ki=Params.KI_STEER, kd=Params.KD_STEER)

frame = cam.get_latest_frame()
filepath = "data/test_img"
roi = Params.ROI_STEER

try:
    err = calc_error(img=frame, roi=roi)
except (BadFrame, LineNotDetected):
    err = None

output = steering_controller.calc_output(err)

img = visualize(frame, err, output)
cv2.imwrite(f'{filepath}/detected_line.png', img)

blue_channel = frame[:, :, 0]
cv2.imwrite(f'{filepath}/blue_channel_image.png', blue_channel)