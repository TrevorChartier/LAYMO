# LAYMO

**Autonomous Vision-Based Line-Following RC Car with Raspberry Pi**

![Demo GIF](https://github.com/TrevorChartier/TrevorChartier.github.io/blob/main/assets/project-photos/laymo/split_screen.gif)

---

## Overview  
Laymo is an autonomous RC car platform that uses a Raspberry Pi and camera module to detect and follow a colored tape line in real time. It demonstrates embedded hardware integration, low-latency computer vision, and closed-loop control on resource-constrained hardware. It is implemented in Python and structured as a pip-installable package.


For an in-depth look at the methods: [View the Report](https://trevorchartier.com/assets/project-photos/laymo/LAYMO_Methods.pdf)

---

## Software Features
- **Modularity Codebase** structured into reusable modules for perception, control, and interfacing that can be imported into other projects via pip:
  
   ![UML](https://github.com/TrevorChartier/TrevorChartier.github.io/blob/main/assets/project-photos/laymo/uml.png)
  
- **Real-time line detection** using channel isolated thresholding:
  
  ![Vision Pipeline](https://github.com/TrevorChartier/TrevorChartier.github.io/blob/main/assets/project-photos/laymo/cv_pipe.png)

  
- **PID-based control** for smooth, proportional steering corrections:

$$
u(t) = K_p e(t) + K_i \int_0^t e(\tau)\,d\tau + K_d \frac{de(t)}{dt}
$$

---
## Hardware

![Car Components](https://github.com/TrevorChartier/TrevorChartier.github.io/blob/main/assets/project-photos/laymo/labeled_car.png)


Laymo interfaces with a custom hardware stack including:

- Commercially available RC car
- Raspberry Pi 5
- PCA9685 driver for precise PWM control of ESC and servo
- DC-DC Buck converter for regulating voltage of on-board power supply
- Arducam 5MP OV5647 camera


![Wiring Diagram](https://github.com/TrevorChartier/TrevorChartier.github.io/blob/main/assets/project-photos/laymo/wiring.png)


## Installation

This package is structured for standard Python packaging. If needed in another project:

```bash
pip install git+https://github.com/TrevorChartier/LAYMO.git
```
All dependencies are automatically installed to your environment.


Then, witin your script, you can import any laymo module:
```python
from laymo.car import Car
```
