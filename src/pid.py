"""This Module Implements the PID Class"""


class PID:
    """
    Class for Creating Proportional Integral Derivative Controllers

    Usage:
        controller = PID(kp=1.0,ki=1.0,kd=1.0)
        correction = controller.calc_correction(error=4.2)
    """
    def __init__(self, ki: float, kp: float, kd: float):
        self.__kp = kp
        self.__ki = ki
        self.__kd = kd
        self.__previous_error = 0.0
        self.__error_sum = 0.0

    def calc_output(self, error: float) -> float:
        """
        Computes the control output (correction) using the PID formula
        based on the current error value.

        Args:
            error (float): The difference between the desired setpoint 
                        and the current process value.

        Returns:
            float: The computed correction value based on the proportional, 
                integral, and derivative terms.
        """
        self.__error_sum += error
        output = (self.__kp * error
                  + self.__kd * (error - self.__previous_error)
                  + self.__ki * self.__error_sum)
        self.__previous_error = error

        return output
