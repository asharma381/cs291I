import matplotlib.pyplot as plt
import numpy as np
import os
import json
from tqdm import tqdm
from PIL import Image
from random import randint



def generate_random_images(json_name: str, folder_name: str, image_dir: str="exp_imgs"):
    f = open(json_name)
    data = json.load(f)
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)
    for img_path, points in tqdm(data.items()):
        if image_dir not in img_path:
            img_path = f"{image_dir}/{img_path}"
            

            img_path += ".png"


        img_name = img_path.split("/")[1].split(".")[0]
        image = Image.open(img_path)
        # print(points)
        for name, _ in points.items():
            fig,ax = plt.subplots(1)
            ax.imshow(np.asarray(image))
            x = randint(0, image.size[0] - 1)
            y = randint(0, image.size[1] - 1)
            # print(image.size)
            ax.scatter(x, y, s=100, c="red", marker="o")
            # Show the image
            plt.axis("off")
            plt.savefig(f"{folder_name}/{img_name}_{name}", bbox_inches='tight', pad_inches=0)
            plt.close()
            # print(f"{folder_name}/{img_name}_{name}")


generate_random_images("good_data1.json", "all_random_locs")
