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
steering_controller = PID(kp=2.3, ki=0.08, kd=0)
time.sleep(1)

def is_throttled():
    """Checks for Undervoltages"""
    status = subprocess.run(['vcgencmd','get_throttled'], capture_output=True, text=True)
    status  = status.stdout.strip()
    return status == 'throttled=0x1' or status == 'throttled=0x4'


def set_speed_manual(iteration):
    """Method to manually pulse throttle"""
    if (iteration//15) % 3 == 0:
        car.set_speed(0.23)
    else:
        car.set_speed(0.0)

time_off_line = 0
RUN_TIME = 25 # Runtime in seconds
NUM_ITERATIONS = 32 * RUN_TIME # Approx 32hz
print("Beginning Control Loop")
for i in range(NUM_ITERATIONS):
    if is_throttled():
        print("UNDERVOLTAGE DETECTED")
        car.stop() 

    set_speed_manual(i)
    frame = camera.get_latest_frame()
    steering_error = line_detector.calc_error(frame, roi=[0.2, 0.8])

    if steering_error is None:
        if abs(car.current_steering_pos()) > 0.7 and time_off_line < 45:
            time_off_line += 1
            continue # Likely went off line, try to recover    
        else:
            print(f"END OF LINE DETECTED")
            car.stop()
            break
              
    time_off_line = 0
        
    steering_control_output = steering_controller.calc_output(steering_error)
    car.set_steering(steering_control_output)

car.stop()
