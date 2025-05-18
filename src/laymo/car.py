"""Provides the Car class for RC car control.

Usage:
        car = Car(steering_pin=STEERING_PIN, throttle_pin=THROTTLE_PIN)
        car.set_steering(0.5)
"""

import sys
import signal
import time
from adafruit_servokit import ServoKit


class Car:
    """Controls an RC car's steering and throttle via PCA9685.

    Provides methods to set steering angle and speed, automatically
    clamping values within physical limits.
    """

    __MIN_SPEED = 0.17
    __CENTER = 83
    __MAX_ANGLE = 35

    def __init__(self, steering_pin: int, throttle_pin: int, max_speed: float = 0.8):
         """Initializes the car controller.

        Args:
            steering_pin (int): PWM channel for steering servo.
            throttle_pin (int): PWM channel for throttle servo.
            max_speed (float, optional): Maximum magnitude of speed (0 to 0.8). Defaults to 0.8.
        """
        kit = ServoKit(channels=16)
        self.__steering = kit.servo[steering_pin]
        self.__motor = kit.continuous_servo[throttle_pin]

        self.set_steering(0)
        self.__current_steering_pos = 0
        
        self.__MAX_SPEED = min(0.8, max_speed)

    def current_steering_pos(self):
        """"Retrieves the current steering position as a value in the range [-1,1]"""
        return self.__current_steering_pos

    def set_steering(self, position: float):
        """Sets the steering position, clamped to physical limits.

        Args:
            position (float or None): Steering position from -1 (full left)
                to 1 (full right). None means no change.
        """
        if position is not None:
            clamped_position = Car.__clamp(position, min_val=-1, max_val=1)
            self.__current_steering_pos = clamped_position
            angle_from_center = round(clamped_position * self.__MAX_ANGLE, 2)
            
            self.__steering.angle = self.__CENTER + angle_from_center      

    def set_speed(self, speed: float):
       """Sets the car speed, clamped and scaled to physical limits.

        Args:
            speed (float): Speed from -1 (full reverse) to 1 (full forward).
                Values below minimum threshold are treated as zero.
        """
        clamped_speed = Car.__clamp(speed, min_val=-1, max_val=1)
        scaled_speed = round(clamped_speed * self.__MAX_SPEED, 2)

        if (abs(scaled_speed) < self.__MIN_SPEED):
            scaled_speed = 0

        self.__motor.throttle = scaled_speed

    def stop(self):
        """Stops the car immediately."""
        print("\nStopping car...")
        self.set_steering(0)
        self.set_speed(-0.9)
        time.sleep(0.45)
        self.set_speed(0)

    @staticmethod
    def __clamp(value, min_val, max_val):
        return min(max(value, min_val), max_val)
