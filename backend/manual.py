# %%
import os
import matplotlib.pyplot as plt
from random import randint
from collections import Counter, defaultdict
from IPython.display import display, Markdown

# %%


METHOD_1 = "all_bad_locs"
METHOD_2 = "all_good_locs"

image_path_prefix = "images/annotated"
img_file_list = sorted(
    set(os.listdir(f"{image_path_prefix}/{METHOD_1}"))
    & set(os.listdir(f"{image_path_prefix}/{METHOD_2}"))
)

counts = Counter()
object_counts = defaultdict(lambda: Counter())

# %%

ls = img_file_list[:3]
for i, file in enumerate(ls):
    object = file.split("_")[1].split(".")[0]
    display(Markdown(f"In the image below, where should a **{object}** be placed?"))
    fig, (ax1, ax2) = plt.subplots(
        1, 2, figsize=(10, 15), gridspec_kw={"wspace": 0, "hspace": 0}
    )
    img_1 = plt.imread(f"{image_path_prefix}/{METHOD_1}/{file}")
    img_2 = plt.imread(f"{image_path_prefix}/{METHOD_2}/{file}")

    rand = randint(0, 1)
    if rand == 0:
        ax1.imshow(img_1)
        ax1.axis("off")
        ax2.imshow(img_2)
        ax2.axis("off")
        # fig.show()
        plt.show()
    else:
        ax1.imshow(img_2)
        ax1.axis("off")
        ax2.imshow(img_1)
        ax2.axis("off")
        # fig.show()
        plt.show()

    ret = input("Enter '[' or ']' or anything else")
    if ret in {"[", "]"}:
        if (rand == 0 and ret == "[") or (rand == 1 and ret == "]"):
            counts[METHOD_1] += 1
            object_counts[object][METHOD_1] += 1
        else:
            counts[METHOD_2] += 1
            object_counts[object][METHOD_2] += 1
    else:
        counts["tie"] += 1
        object_counts[object]["tie"] += 1

    print(f"{i + 1}/{len(ls)}")

print(dict(counts))
print(dict(object_counts))


# %%
