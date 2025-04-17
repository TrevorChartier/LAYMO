"""
This Module Implements the PID Class for Creating
Proportional Integral Derivative Controllers

Usage:
    controller = PID(kp=1.0,ki=1.0,kd=1.0)
    correction = controller.calc_correction(error=4.2)
"""
class PID:
    
    def __init__(self, ki: float, kp: float, kd: float):
        pass
    
    def calc_correction(self, error: float) -> float:
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