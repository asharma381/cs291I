import json
import os

import cv2
import numpy as np

RATIO = 1.15694130137
output = {}

for image in sorted(os.listdir("../../all_random_locs")):
    path = "../../all_random_locs/" + image
    img_name = image.split("_")[0] + ".png"
    obj_name = image.split("_")[1].split(".")[0]

    src = cv2.imread(path)
    hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, np.array([0, 200, 200]), np.array([0, 255, 255]))
    index = np.where(mask == 255)
    x, y = np.mean(index[0]), np.mean(index[1])

    if output.get(img_name) is None:
        output[img_name] = {}
        output[img_name][obj_name] = [y * RATIO, x * RATIO]
    else:
        output[img_name][obj_name] = [y * RATIO, x * RATIO]

json.dump(output, open("coords.json", "w"))
