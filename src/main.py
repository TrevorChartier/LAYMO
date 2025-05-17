"""This module is the main controller for the Laymo Car"""

import subprocess
import sys
import signal
import time
import numpy as np

import laymo.line_detector as line_detector
from laymo.visualize import visualize

from laymo.car import Car
from laymo.camera_manager import CameraManager
from laymo.pid import PID
from laymo.params import Params
from laymo.logger import Logger


logger = Logger(
    path="data/log_video.mp4",
)
car = Car(
    steering_pin=Params.STEERING_PIN,
    throttle_pin=Params.THROTTLE_PIN
)
camera = CameraManager()
steering_controller = PID(
    kp=Params.KP_STEER,
    ki=Params.KI_STEER,
    kd=Params.KD_STEER
)


def handle_exit(signum, frame):
    """ Signal Handlers """
    car.stop()
    logger.close()
    sys.exit(signum)


for sig in (signal.SIGINT, signal.SIGTERM, signal.SIGHUP):
    signal.signal(sig, handle_exit)


def set_speed_manual(i):
    """Method to manually pulse throttle"""
    car.set_speed(0.0 if (i//10) % 8  == 0 else 0.25)


def control_loop():
    start = time.time()
    time_off_line = 0
    steering_error = 0
    for i in range(Params.NUM_ITERATIONS):
        set_speed_manual(i)
        frame = camera.get_latest_frame()
        
        try:
            steering_error = line_detector.calc_error(frame, roi=Params.ROI_STEER)
            time_off_line = 0 # reset on successful detection
            
        except line_detector.BadFrame:
            img = visualize(frame, None, car.current_steering_pos())
            logger.write(img)
            continue
        
        except line_detector.LineNotDetected:
            end_of_line = (
                abs(steering_error) < Params.STEERING_THRESHOLD 
                or time_off_line > Params.TIME_OFF_LINE_LIMIT
            )
            if end_of_line:
                print("END OF LINE DETECTED")
                break
            # Attempt recovery using previous steering direction   
            time_off_line += 1
            steering_error = np.sign(steering_error) * 1

        output = steering_controller.calc_output(steering_error)
        car.set_steering(output)
        
        img = visualize(frame, steering_error, car.current_steering_pos())
        logger.write(img)
    car.stop()    
    print(f"FPS: {np.round(i / (time.time() - start), 2)}")


if __name__ == "__main__":
    print("Beginning Control Loop")
    time.sleep(1)
    control_loop()
    print("Control Loop Ended")
    logger.close()
