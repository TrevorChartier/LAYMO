"""This module is the main controller for the Laymo Car"""

import subprocess
import sys
import signal
import time

import line_detector

from car import Car
from camera_manager import CameraManager
from pid import PID


THROTTLE_PIN = 0 # PCA9685 pin of ESC connection
STEERING_PIN = 1 # PCA9685 pin of Servo Connection

car = Car(steering_pin=STEERING_PIN, throttle_pin=THROTTLE_PIN)

# Signal Handlers -- Stop Car if any Error or ^C
signal.signal(signal.SIGINT, car.stop)  
signal.signal(signal.SIGTERM, car.stop) 
signal.signal(signal.SIGHUP, car.stop)

camera = CameraManager()
steering_controller = PID(kp=1.5, ki=0, kd=0)
throttle_controller = PID(kp=3.75, ki=0, kd=0)
time.sleep(1)

def is_throttled():
    """Checks for Undervoltages"""
    status = subprocess.run(['vcgencmd','get_throttled'], capture_output=True, text=True)
    return status.stdout.strip() != 'throttled=0x0'


def set_speed_manual(iteration):
    """Method to manually pulse throttle"""
    if (iteration//10) % 2 == 0:
        car.set_speed(0.2)
    else:
        car.set_speed(0)

RUN_TIME = 5 # Runtime in seconds
NUM_ITERATIONS = 32 * RUN_TIME # Approx 32hz
print("Beginning Control Loop")
for i in range(NUM_ITERATIONS):
    if is_throttled():
        print("UNDERVOLTAGE DETECTED")
        car.stop() 

    frame = camera.get_latest_frame()
    steering_error = line_detector.calc_error(frame, roi=[0.2, 0.7])

    steering_control_output = steering_controller.calc_output(steering_error)
    car.set_steering(steering_control_output)

    if steering_error is None:
        car.stop()
        break # Reached the end of the line

    set_speed_manual(i)

car.stop()
