"""
Entry point for running the Laymo Car controller.

Initializes the Controller, sets up signal handlers, and starts the control loop.
"""

import subprocess
import sys
import signal
import time

from laymo.controller import Controller   
    
def main(): 
    controller = Controller()
    for sig in (signal.SIGINT, signal.SIGTERM, signal.SIGHUP):
        signal.signal(sig, controller.handle_exit)
    print("Beginning Control Loop")
    time.sleep(1)
    controller.control_loop()
    controller.cleanup()


if __name__ == "__main__":
    main()
