import os
import csv
import numpy as np
from random import shuffle

if __name__ == "__main__":
    good = "all_good_locs/"
    good_s3 = "gamma"
    octopus = "all_octopus_vqa_locs/"
    octopu_s3 = "alpha"

    s3_url = "https://291i.s3.amazonaws.com"

    items = np.array(os.listdir(good)[:12])
    items = items.reshape((len(items) // 3,3))


    with open("mturk.csv", "w", newline="") as csvfile:
        fields = [
            "obj1",
            "imgl1",
            "imgr1",
            "obj2",
            "imgl2",
            "imgr2",
            "obj3",
            "imgl3",
            "imgr3",
        ]
        csv_writer = csv.DictWriter(csvfile, fieldnames=fields)
        csv_writer.writerow(
            {field: field for field in fields}
        )
        for row_data in items:
            row_dict = {}
            for i, img_name in enumerate(row_data):
                i += 1
                obj = img_name.split("_")[1].split(".")[0]
                row_dict[f"obj{i}"] = obj

                order = ["l", "r"]
                shuffle(order)

                row_dict[f"img{order[0]}{i}"] = f"{s3_url}/{good_s3}/{img_name}"
                row_dict[f"img{order[1]}{i}"] = f"{s3_url}/{octopu_s3}/{img_name}"
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