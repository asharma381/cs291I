# fields = [
#     "obj1",
#     "imgl1",
#     "imgr1",
#     "obj2",
#     "imgl2",
#     "imgr2",
#     "obj3",
#     "imgl3",
#     "imgr3",
# ]

# fields = [
#     f"{entity}{i}"
#     for i in range(1, 4)
#     for entity in ["obj", "imgl", "imgr"]
# ]
# print(fields)


import os
from random import sample
import json

# good = "all_octopus_vqa_locs/"
# octopus = "all_octopus_old_locs/"

# good_ls = set(os.listdir(good))
# octo_ls = set(os.listdir(octopus))

# print(good_ls - octo_ls)

# print(len(os.listdir(good)))
# print(len(os.listdir(octopus)))

ls = os.listdir("all_bad_locs")
ls1 = os.listdir("all_octopus_old_locs")

intersection = set(ls) & set(ls1)

sam = sample(list(intersection), 120)
with open('list_120.json', 'w') as f:
    json.dump(sam, f)