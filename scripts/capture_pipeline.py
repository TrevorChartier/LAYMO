import matplotlib.pyplot as plt
import time
import numpy as np
import cv2

from laymo.camera_manager import CameraManager
from laymo.line_detector import calc_error, preprocess
from laymo.params import Params

cam = CameraManager()
img = cam.get_latest_frame()
filepath = "data"
roi = Params.ROI_STEER

start = time.time()
err = calc_error(img=img, roi=roi)
print("Processing time: ", np.round(time.time()-start, 6))
print("Error: ", err)

img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
plt.imshow(img_rgb)
# Horizontal Lines Representing Cropped Region
plt.axhline(y=img.shape[0] - roi[0]*img.shape[0], color='green')
plt.axhline(y=img.shape[0] - roi[1]*img.shape[0], color='green')

if err is not None:
    # Recalculate line center from error value
    line_center = err * (img.shape[1] // 2) + img.shape[1]//2
    plt.axvline(x=np.mean(line_center), color='red',
                linewidth=2)  # Red Line at Detected Line Center  
else:
    print("No Line")

plt.savefig(f'{filepath}/detected_line.png')

# Write binary image after processing to file
processed_img = preprocess(img) 
cv2.imwrite(f'{filepath}/processed_image.png', processed_img)

# Write blue channel of image to file
blue_channel = img[:, :, 0]
cv2.imwrite(f'{filepath}/blue_channel_image.png', blue_channel)