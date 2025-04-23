"""This module implements the Car class"""

import sys
import signal
from adafruit_servokit import ServoKit


class Car:
    """ 
    Class for Controlling RC Car through PCA9685

    Usage:
        car = Car(steering_pin=STEERING_PIN, throttle_pin=THROTTLE_PIN)
        car.set_steering(0.5)
    """
    __MIN_SPEED = 0.17
    __TOP_SPEED = 0.8

    __CENTER = 83
    __MAX_ANGLE = 35

    def __init__(self, steering_pin: int, throttle_pin: int):
        kit = ServoKit(channels=16)
        self.__steering = kit.servo[steering_pin]
        self.__motor = kit.continuous_servo[throttle_pin]

        self.set_steering(0)

    def set_steering(self, position: float):
        """
        Sets the steering position to the specified value. Automatically
        clamps and adjusts to the range of the cars physical steering limits.

        Args:
            position (int): Position from center to set the steering. The valid range
            is between [-1, 1] where a value of 0 corresponds to straight.
        """
        clamped_position = Car.__clamp(position, min_val=-1, max_val=1)
        angle_from_center = round(clamped_position * self.__MAX_ANGLE, 2)

        self.__steering.angle = self.__CENTER + angle_from_center

    def set_speed(self, speed: float):
        """
        Sets the cars speed to the specified value. Automatically
        clamps and adjusts to the range of the cars physical limits.

        Args:
            speed (float): The valid range is between [-1 and 1] where
            negative values are reverse and 0 is stopped.
        """
        clamped_speed = Car.__clamp(speed, min_val=-1, max_val=1)
        scaled_speed = round(clamped_speed * self.__TOP_SPEED, 2)

        if (abs(scaled_speed) < self.__MIN_SPEED):
            scaled_speed = 0

        self.__motor.throttle = scaled_speed

    def stop(self, signum=None, frame=None):
        """Stop the car and exit the program"""
        print("\nStopping car...")
        self.set_speed(0)
        self.set_steering(0)
        sys.exit(0)

    def __clamp(value, min_val, max_val):
        return min(max(value, min_val), max_val)
