""" Hyperparameter Settings for LAYMO (utilized in main.py)"""

class Params():
 
    # PCA9685 pins
    THROTTLE_PIN = 0
    STEERING_PIN = 1
    
    # Controller Gains
    KP_STEER = 1.5
    KI_STEER = 0.0
    KD_STEER = 0.0
    
    # Runtime Settings
    __LOOP_HZ = 32
    __RUNTIME_SECS = 10
    NUM_ITERATIONS = __LOOP_HZ * __RUNTIME_SECS
    
    # Image Processing (main.py)
    ROI_STEER = [0.1, 0.5]
    
    # Image Processing (line_detector.py)
    BINARY_THRESHOLD = 220
    LINE_DETECTED_THRESHOLD = 0.03
    
    # Second Chance Thresholds
    STEERING_THRESHOLD = 0.7
    TIME_OFF_LINE_LIMIT = 45