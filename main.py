from car import Car
import time
import sys 
import signal

THROTTLE_PIN = 0 # PCA9685 pin of ESC connection
STEERING_PIN = 1 # PCA9685 pin of Servo Connection

car = Car(steering_pin=STEERING_PIN, throttle_pin=THROTTLE_PIN)

# Signal Handlers -- Stop Car ff any Error or ^C
signal.signal(signal.SIGINT, car.stop)  
signal.signal(signal.SIGTERM, car.stop) 

time.sleep(1)

# Swivel Steering
car.set_steering(-1)
time.sleep(0.5)
car.set_steering(1)
time.sleep(0.5)
car.set_steering(0)
time.sleep(1)

# Rev Throttle
car.set_speed(-0.25)
time.sleep(0.5)


# Stop Car
car.stop()
