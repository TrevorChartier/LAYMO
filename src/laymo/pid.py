"""Provides the PID class for Proportional-Integral-Derivative control.

Usage:
        controller = PID(kp=1.0,ki=1.0,kd=1.0)
        correction = controller.calc_correction(error=4.2)
"""

import numpy as np


class PID:
    """Implements a Proportional-Integral-Derivative (PID) controller.

    The PID controller calculates a corrective output based on the
    current error, its cumulative sum (integral), and the rate of
    change (derivative).
    """

    def __init__(self, ki: float, kp: float, kd: float):
        """Initializes PID controller
        
        Args:
            kp (float): Proportional gain coefficient.
            ki (float): Integral gain coefficient.
            kd (float): Derivative gain coefficient.
        """
        self.__kp = kp
        self.__ki = ki
        self.__kd = kd
        self.__previous_error = 0.0
        self.__error_sum = 0.0

    def calc_output(self, error: float | None) -> float | None:
        """
        Calculate the PID controller output based on the current error.

        Args:
            error (float or None): The difference between the setpoint
            and the actual value. If None, the output is None.

        Returns:
            float or None: The PID correction output, rounded to two 
            decimals, or None if input error is None.
        """
        if error is None:
            return None
        
        self.__error_sum += error
        output = (self.__kp * error
                  + self.__kd * (error - self.__previous_error)
                  + self.__ki * self.__error_sum)
        self.__previous_error = error

        return np.round(output, 2)
