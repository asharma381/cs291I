import json
import re

import matplotlib.pyplot as plt
from PIL import Image

data = json.load(open("gpt4v_s3.json", "r"))
pattern = r"\((\d+), (\d+)\)"

output = {}

for img, obj_to_loc in data.items():
    output[img] = {}
    for obj, locs in obj_to_loc.items():
        print(img, locs)
        match = re.search(pattern, locs)
        if match:
            x = int(match.group(1))
            y = int(match.group(2))
            print("X Coordinate:", x)
            print("Y Coordinate:", y)
            output[img][obj] = [x, y]

            # plt.imshow(Image.open("../original_images/" + str(img)))
            # plt.scatter(x, y, s=10, c="red", marker="o")
            # plt.show()

        else:
            print("Coordinates not found in the string.")
json.dump(output, open("gpt4v_s3_clean.json", "w"))
