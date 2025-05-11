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
    fps = 30.0
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


for sig in (signal.SIGINT, signal.SIGTERM, signal.SIGHUP):
    signal.signal(sig, handle_exit)


def is_throttled():
    """Checks for Undervoltages"""
    status = subprocess.run(['vcgencmd', 'get_throttled'],
                            capture_output=True, text=True, check=True)
    status = status.stdout.strip()
    return status in ['throttled=0x1', 'throttled=0x4']


def set_speed_manual(i):
    """Method to manually pulse throttle"""
    car.set_speed(0.0 if (i//10) % 8  == 0 else 0.25)


def control_loop():
    start = time.time()
    time_off_line = 0
    for i in range(Params.NUM_ITERATIONS):
        if is_throttled():
            print("UNDERVOLTAGE DETECTED")
            break

        set_speed_manual(i)
        frame = camera.get_latest_frame()  # Capture the latest frame
        steering_error = line_detector.calc_error(frame, roi=Params.ROI_STEER)
        
        if steering_error is None:
            if (abs(car.current_steering_pos()) > Params.STEERING_THRESHOLD
                    and time_off_line < Params.TIME_OFF_LINE_LIMIT):
                time_off_line += 1 # Likely went off line, try to recover
            else:
                print("END OF LINE DETECTED")
                break
        else:
            time_off_line = 0

        output = steering_controller.calc_output(steering_error)
        car.set_steering(output)
        
        img = visualize(frame, steering_error, car.current_steering_pos())
        logger.write(img)
        
    print(f"FPS: {np.round(i / (time.time() - start), 2)}")
    car.stop()


if __name__ == "__main__":
    print("Beginning Control Loop")
    time.sleep(1)
    control_loop()
    logger.close()
