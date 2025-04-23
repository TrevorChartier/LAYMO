"""This module is the main controller for the Laymo Car"""

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

# Signal Handlers -- Stop Car ff any Error or ^C
signal.signal(signal.SIGINT, car.stop)  
signal.signal(signal.SIGTERM, car.stop) 

camera = CameraManager()
steering_controller = PID(kp=1, ki=0, kd=0)
time.sleep(1)

RUN_TIME = 5 # Runtime in seconds
NUM_ITERATIONS = 32 * RUN_TIME # Approx 32hz

print("Beginning Control Loop")
for i in range(NUM_ITERATIONS):
    frame = camera.get_latest_frame()
    error = line_detector.calc_error(frame, roi=[0.1, 0.6])
    if error is None:
        print("No Line Detected")
        continue
    steering_control_output = steering_controller.calc_output(error)
    car.set_steering(steering_control_output)

    if (i//10) % 2 == 0:
        car.set_speed(0.2)
    else:
        car.set_speed(0)

car.stop()
