""" Hyperparameter Settings for LAYMO (utilized in main.py)"""

class Params():
 
    # PCA9685 pins
    THROTTLE_PIN = 0
    STEERING_PIN = 1
    
    # Controller Gains
    KP_STEER = 1.6
    KI_STEER = 0.0
    KD_STEER = 7.2
    
    # Runtime Settings
    __LOOP_HZ = 53
    __RUNTIME_SECS = 20
    NUM_ITERATIONS = int(__LOOP_HZ * __RUNTIME_SECS)
    
    # Image Processing (main.py)
    ROI_STEER = [0.48, 0.7]
    
    # Image Processing (line_detector.py)
    BINARY_THRESHOLD = 220
    MIN_LINE_THRESHOLD = 0.03
    MAX_LINE_THRESHOLD = 0.4
    
    # Second Chance Thresholds
    STEERING_THRESHOLD = 0.7
    TIME_OFF_LINE_LIMIT = 40
    
    # Camera Params
    FRAME_WIDTH = 640  
    FRAME_HEIGHT = 480 