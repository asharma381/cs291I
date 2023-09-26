import os
import csv
import numpy as np
from random import shuffle, randint
import json

IMAGES_PER_TASK = 5
ATTENTION_CHECK = True

if ATTENTION_CHECK:
    IMAGES_PER_TASK += 1

codename_to_group = {
    "gamma": "good",
    "alpha": "octopus_vqa",
    "chi": "octopus_clipseg",
    "rho": "random",
    "omega": "bad",
}

bad_imgs = os.listdir("all_bad_locs")

if __name__ == "__main__":
    # good = "all_good_locs/"
    first_s3 = "gamma"
    # octopus = "all_octopus_vqa_locs/"
    second_s3 = "omega"

    bad_s3 = "omega"
    good_s3 = "gamma"

    s3_url = "https://291i.s3.amazonaws.com"

    f = open("list_120.json")
    file_names = json.load(f)
    items = np.array(file_names)
    items = items.reshape((len(items) // IMAGES_PER_TASK, IMAGES_PER_TASK))

    with open(f"mturk_{first_s3}_{second_s3}.csv", "w", newline="") as csvfile:
        fields = [
            f"{entity}{i}"
            for i in range(1, IMAGES_PER_TASK + 1)
            for entity in ["obj", "imgl", "imgr"]
        ]
        csv_writer = csv.DictWriter(csvfile, fieldnames=fields)
        csv_writer.writeheader()
        for row_data in items[:10]:
            row_dict = {}
            chosen = randint(1, IMAGES_PER_TASK)
            for i, img_name in enumerate(row_data):
                i += 1
                obj = img_name.split("_")[1].split(".")[0]
                row_dict[f"obj{i}"] = obj

                order = ["l", "r"]
                shuffle(order)

                if i != chosen:
                    row_dict[f"img{order[0]}{i}"] = f"{s3_url}/{first_s3}/{img_name}"
                    row_dict[f"img{order[1]}{i}"] = f"{s3_url}/{second_s3}/{img_name}"
                else:
                    row_dict[f"img{order[0]}{i}"] = f"{s3_url}/{bad_s3}/{img_name}"
                    row_dict[f"img{order[1]}{i}"] = f"{s3_url}/{good_s3}/{img_name}"
            
            csv_writer.writerow(row_dict)



"""
import os
import csv

if __name__ == "__main__":
    good = "all_good_locs/"
    octopus = "all_octopus_vqa_locs/"
    
    items = os.listdir(good)
    
    with open('mturk.csv', 'w', newline='') as csvfile:
        fields = ['object', 'imgl', 'imgr']
        csv_writer = csv.writer(csvfile, fieldnames=fields, delimiter=' ')
        for i in list(items):
            img = i[:i.index("_")]
            obj = i[i.index("_")+1:i.index(".")]
            csv_writer.writerow({'object': f'{obj}', 'imgl': f'https://291i.s3.amazonaws.com/{good}/{i}', 'imgr': f'https://291i.s3.amazonaws.com/{octopus}/{i}'})
"""