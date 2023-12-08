import json
from PIL import Image
import numpy as np
from collections import defaultdict
import matplotlib.pyplot as plt

classnames = json.load(open("masks/classnames.json"))
ground_truth = json.load(open("../eval/stage_3/ground_truth_seg.json"))
ground_truth_with_mask = json.load(open("../eval/stage_3/ground_truth_with_mask.json"))


# placements_2d = json.load(open("../eval/stage_3/bad_data.json"))
# placements_2d = json.load(open("../eval/stage_3/good_data.json"))

dino = json.load(open("../eval/stage_3/gpt4_dino_clipseg.json"))
gpt4v = json.load(open("../eval/stage_3/gpt4v_clipseg.json"))
# placements_2d = json.load(open("../eval/stage_3/gpt4_clip_clipseg.json"))


all_surfaces = {
    "shelf",
    "sink",
    "table",
    "blanket",
    "couch",
    "counter",
    "wall",
    "chair",
    "pillow",
    "book",
    "floor",
    "rug",
    "stool",
    "bed",
}

successes = {}

surface_to_ids = defaultdict(list)
for surface in all_surfaces:
    for i, class_surface in enumerate(classnames):
        if surface == class_surface:
            surface_to_ids[surface].append(i + 1)

total_placements = 0
num_times_in_mask = 0
total_score = 0
for img, objs_to_place in ground_truth_with_mask.items():
    # if img not in placements_2d:
    #     print("STOPPING HERE", img)
    #     break
    mask = Image.open(f"masks/{img}")
    np_mask = np.array(mask.getdata())
    np_mask = np_mask.reshape((mask.height, mask.width))

    for obj in objs_to_place:
        gt_locs = ground_truth[img][obj]
        valid_mask = np.zeros_like(np_mask)
        for gt_loc in gt_locs:
            for id in surface_to_ids[gt_loc]:
                valid_mask += np.where(np_mask == id, 1, 0)
        

        xd, yd = dino[img][obj]
        in_mask = valid_mask[round(yd), round(xd)]
        num_times_in_mask += in_mask
        total_placements += 1

        coords = np.argwhere(valid_mask == 1 - in_mask)
        distances = np.linalg.norm(coords - np.array([round(yd), round(xd)]), axis=1)
        closest_index = np.argmin(distances)
        closest_coords = coords[closest_index]
        closest_y, closest_x = closest_coords
        closest_dist = np.min(distances)
        dinodiff = pow(-1, 1 - in_mask) * closest_dist

        x, y = gpt4v[img][obj]
        in_mask = valid_mask[round(y), round(x)]
        num_times_in_mask += in_mask
        total_placements += 1

        coords = np.argwhere(valid_mask == 1 - in_mask)
        distances = np.linalg.norm(coords - np.array([round(y), round(x)]), axis=1)
        closest_index = np.argmin(distances)
        closest_coords = coords[closest_index]
        closest_y, closest_x = closest_coords
        closest_dist = np.min(distances)
        gpt4vdiff = pow(-1, 1 - in_mask) * closest_dist

        diff = gpt4vdiff - dinodiff
        if diff > 100:
            successes[img] = successes.get(img, []) + [(obj, diff, *gt_locs)]
            # print(f"Placement for {obj} in {img}. Valid locs: {gt_locs}")
            # plt.imshow(valid_mask)

            # plt.scatter(x, y, s=50, c="green", marker="o")
            # plt.scatter(xd, yd, s=50, c="red", marker="o")

            # # print(x, y)
            # # plt.scatter(closest_x, closest_y, s=20, c="red", marker="o")
            # # print(pow(-1, 1 - in_mask) * closest_dist)

            # plt.show()
        
json.dump(successes, open("failures2.json", "w"))
    

print(f"In mask {num_times_in_mask} out of {total_placements} times, which is {num_times_in_mask / total_placements * 100}% of the time")
print(f"Total score: {total_score / total_placements}")
    #     print(f"Showing {gt_locs} which are the valid placements for {obj}")
    #     plt.imshow(valid_mask)
    #     x, y = placements_2d[img][obj]
    #     plt.scatter(x, y, s=100, c="red", marker="o")
    #     plt.show()
        

    # for obj in objs_to_place:

# total_placements = 0
# num_times_in_mask = 0
# for each image
#     for each object that we are placing in the image
#         initialize empty valid mask for this mask M
#         for each surface that is a valid location for the object
#             for each id that corresponds to the surface
#                 union this id's mask into M
#         1. if M[x,y] = 1, num_times_in_mask += 1
#         total_placements += 1
#
# prop_time_in_mask = num_times_in_mask / total_placements


