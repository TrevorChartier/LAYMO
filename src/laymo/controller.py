"""Controls an autonomous car using camera input and a PID controller.

This module defines the Controller class, which manages the main
control loop for autonomous line-following, including visual line
detection, PID-based steering control, video logging, and safe shutdown
via signal handling.

Usage:
    controller = Controller()
    for sig in (signal.SIGINT, signal.SIGTERM, signal.SIGHUP):
        signal.signal(sig, controller.handle_exit)
    controller.control_loop()
    controller.cleanup()
"""

import time
import numpy as np

from laymo import line_detector
from laymo import params
from laymo.visualize import visualize

from laymo.car import Car
from laymo.camera_manager import CameraManager
from laymo.pid import PID
from laymo.logger import Logger


class Controller:
    """Controls steering and throttle based on visual line detection.

    Initializes and manages the car, camera, PID controller, and logger.
    Executes the main control loop for autonomous line following.
    """

    def __init__(self):
        """Initializes hardware interfaces and controller components."""
        self.__force_stop = False
        self.__logger = Logger(
            path="data/log_video.mp4",
        )
        self.__car = Car(
            steering_pin=params.STEERING_PIN,
            throttle_pin=params.THROTTLE_PIN
        )
        self.__camera = CameraManager()
        self.__steering_controller = PID(
            kp=params.KP_STEER,
            ki=params.KI_STEER,
            kd=params.KD_STEER
        )

    def handle_exit(self, signum, frame):
        """Handles termination signals by triggering a safe stop.

        Args:
            signum: Signal number.
            frame: Current stack frame (unused).
        """
        self.__force_stop = True

    def control_loop(self):
        """Runs the main control loop for line following and logging."""
        start = time.time()
        time_off_line = 0
        steering_error = 0
        for i in range(params.NUM_ITERATIONS):
            if self.__force_stop: break
            self.__set_speed_manual(i)
            frame = self.__camera.get_latest_frame()

            try:
                steering_error = line_detector.calc_error(
                    frame, roi=params.ROI_STEER)
                time_off_line = 0  # reset on successful detection

            except line_detector.BadFrame:
                img = visualize(frame, None, self.__car.current_steering_pos())
                self.__logger.write(img)
                continue

            except line_detector.LineNotDetected:
                end_of_line = (
                    abs(steering_error) < params.STEERING_THRESHOLD
                    or time_off_line > params.TIME_OFF_LINE_LIMIT
                )
                if end_of_line:
                    print("END OF LINE DETECTED")
                    break
                # Attempt recovery using previous steering direction
                time_off_line += 1
                steering_error = np.sign(steering_error) * 1

            output = self.__steering_controller.calc_output(steering_error)
            self.__car.set_steering(output)

            img = visualize(frame, steering_error,
                            self.__car.current_steering_pos())
            self.__logger.write(img)
        self.__car.stop()
        print(f"FPS: {np.round(i / (time.time() - start), 2)}")

    def cleanup(self):
        """Properly closes all resources."""
        self.__logger.close()
        self.__car.set_speed(0)

    def __set_speed_manual(self, i):
        """Manually toggles throttle to pulse the car forward.

        Args:
            i: Current iteration number.
        """
        self.__car.set_speed(0.23 if (i//10) % 8 == 0 else 0.0)
