# %%
import os
import matplotlib.pyplot as plt
from random import shuffle, randint
from collections import Counter, defaultdict

# %%
thing = "good"
img_file_list = os.listdir(f"all_{thing}_locs")

# other_file_list = os.listdir(f"all_octopus_vqa_locs")

# img_file_list = list(set(img_file_list) & set(other_file_list))


shuffle(img_file_list)

counts = Counter()
object_counts = defaultdict(lambda: Counter())
# map1 = {
#     "[": 0,
#     "]": 1,
# }

# map2 = {
#     0: "good",
#     1: "ours",
# }

# %%

ls = img_file_list[:50]
len_ls = len(ls)
for i, file in enumerate(ls):
    print(file)

    print(f"all_{thing}_locs/{file}")
    object = file.split("_")[1].split(".")[0]
    print(object)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 15), gridspec_kw = {'wspace': 0, 'hspace': 0})
    img_old = plt.imread(f"all_{thing}_locs/{file}")
    img_vqa = plt.imread(f"all_random_locs/{file}")

    rand = randint(0,1)
    if rand == 0:
        ax1.imshow(img_old)
        ax1.axis("off")
        ax2.imshow(img_vqa)
        ax2.axis("off")
        # fig.show()
        plt.show()
    else:
        ax1.imshow(img_vqa)
        ax1.axis("off")
        ax2.imshow(img_old)
        ax2.axis("off")
        # fig.show()
        plt.show()
    


    ret = input("Enter '[' or ']' or anything else")
    if ret in {"[", "]"}:
        if (rand == 0 and ret == "[") or (rand == 1 and ret == "]"):
            counts[thing] += 1
            object_counts[object][thing] += 1
        else:
            counts["ours"] += 1
            object_counts[object]["ours"] += 1
    else:
        counts["tie"] += 1
        object_counts[object]["tie"] += 1



    # if ret in map1:
    #     best = map1[ret]
        
    #     counts[map2[(best + rand) % 2]] += 1
    
    print(f"{i + 1}/{len_ls}")
    
    print(counts)
    print(dict(object_counts))



    
        



# %%
