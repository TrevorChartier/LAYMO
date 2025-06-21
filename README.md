# LAYMO

**Autonomous Vision-Based Line-Following RC Car with Raspberry Pi**

---

## Overview  
Laymo is designed and built as an autonomous RC car platform, using a Raspberry Pi and camera module to detect and follow a colored tape line in real time. It demonstrates embedded hardware integration, low-latency computer vision, and closed-loop control on resource-constrained hardware. It is implemented in Python and structured as a pip-installable package using `pyproject.toml`.

---

## Key Features  
- **Real-time line detection** using channel isolated thresholding 
- **PID-based control** for smooth, proportional steering corrections

---
### Hardware
Laymo interfaces with a custom hardware stack including:

- Commercially available RC car
- Raspberry Pi 5
- PCA9685 driver for precise PWM control of ESC and servo
- DC-DC Buck converter for regulating voltage of on-board power supply
- Arducam 5MP OV5647 camera

### Software
The project emphasizes:

- **Modularity**: Code is structured into reusable modules for perception, control, and interfacing that can be imported into other projects via pip.
- **Hardware-software integration**: Designed to run on physical systems with low-latency (50hz) control loop.

## Installation

This package is structured for standard Python packaging. If needed in another project:

```bash
pip install git+https://github.com/yourname/laymo.git
```
All dependencies are automatically installed to your environment.


Then, witin your script, you can import any laymo module:
```python
from laymo.car import Car
```
