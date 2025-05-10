"""This module is the main controller for the Laymo Car"""

import subprocess
import sys
import signal
import time

import line_detector

from car import Car
from camera_manager import CameraManager
from pid import PID
from params import Params


car = Car(steering_pin=Params.STEERING_PIN, throttle_pin=Params.THROTTLE_PIN)
camera = CameraManager()
steering_controller = PID(
    kp=Params.KP_STEER, ki=Params.KI_STEER, kd=Params.KD_STEER)


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
    car.set_speed(0.23 if (i // 15) % 3 == 0 else 0.0)


def control_loop():
    time_off_line = 0
    for i in range(Params.NUM_ITERATIONS):
        if is_throttled():
            print("UNDERVOLTAGE DETECTED")
            car.stop()

        set_speed_manual(i)
        frame = camera.get_latest_frame()
        steering_error = line_detector.calc_error(frame, roi=[0.2, 0.8])

        if steering_error is None:
            if (abs(car.current_steering_pos()) > Params.STEERING_THRESHOLD
                    and time_off_line < Params.TIME_OFF_LINE_LIMIT):
                time_off_line += 1
                continue  # Likely went off line, try to recover
            print("END OF LINE DETECTED")
            car.stop()
            break

        time_off_line = 0

        output = steering_controller.calc_output(steering_error)
        car.set_steering(output)
    car.stop()


if __name__ == "__main__":
    print("Beginning Control Loop")
    time.sleep(1)
    control_loop()
