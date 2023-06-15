import matplotlib.pyplot as plt
import numpy as np
import os
import json
from tqdm import tqdm
from PIL import Image



def generate_images(json_name: str, folder_name: str, image_dir: str="exp_imgs"):
    f = open(json_name)
    data = json.load(f)
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)
    for img_path, points in tqdm(data.items()):
        img_path += ".png"
        # img_path = img_path.split("_")[-1].split(".")[0] + ".png"


        if image_dir not in img_path:
            img_path = f"{image_dir}/{img_path}"
        img_name = img_path.split("/")[1].split(".")[0]
        image = Image.open(img_path)
        for name, (x, y) in points.items():
            fig,ax = plt.subplots(1)
            ax.imshow(np.asarray(image))
            ax.scatter(x, y, s=100, c="red", marker="o")
            # Show the image
            plt.axis("off")
            plt.savefig(f"{folder_name}/{img_name}_{name}", bbox_inches='tight', pad_inches=0)
            plt.close()


generate_images("bad_data.json", "all_bad_locs")
