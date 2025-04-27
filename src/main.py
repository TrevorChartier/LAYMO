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

car = Car(steering_pin=STEERING_PIN, throttle_pin=THROTTLE_PIN, max_speed=0.5)

# Signal Handlers -- Stop Car if any Error or ^C
signal.signal(signal.SIGINT, car.stop)  
signal.signal(signal.SIGTERM, car.stop) 

camera = CameraManager()
steering_controller = PID(kp=1.5, ki=0, kd=0)
throttle_controller = PID(kp=3.75, ki=0, kd=0)
time.sleep(1)

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
    frame = camera.get_latest_frame()
    steering_error = line_detector.calc_error(frame, roi=[0.1, 0.6])

    steering_control_output = steering_controller.calc_output(steering_error)
    car.set_steering(steering_control_output)

    if steering_error is None and (abs(car.current_steering_pos()) < 0.75):
        break # Reached the end of the line

    # Adjust speed
    throttle_error = abs(line_detector.calc_error(frame, roi=[0.3,1]))
    if throttle_error is not None:
        throttle_control_output = throttle_controller.calc_output(throttle_error)
        car.set_speed(1/(throttle_control_output + 1))
    else:
        set_speed_manual(i)

car.stop()
