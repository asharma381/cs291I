from collections import Counter
from pprint import pprint
# %%

individiaul = {
    "cake": Counter({"tie": 4, "good": 1}),
    "plate": Counter({"good": 3, "ours": 1}),
    "book": Counter({"tie": 3, "good": 2}),
    "lamp": Counter({"tie": 3, "good": 1}),
    "cup": Counter({"tie": 3, "good": 2}),
    "cat": Counter({"good": 2, "tie": 1}),
    "painting": Counter({"tie": 4, "good": 1}),
    "pencil": Counter({"tie": 3}),
    "bag": Counter({"good": 2}),
    "computer": Counter({"tie": 1, "good": 1}),
    "apple": Counter({"tie": 2}),
    "stool": Counter({"tie": 2}),
    "vase": Counter({"good": 3, "tie": 1}),
    "shoes": Counter({"tie": 1}),
    "cushion": Counter({"tie": 2, "ours": 1}),
}


luke = {
    "apple": Counter({"tie": 3, "good": 2}),
    "plate": Counter({"good": 2}),
    "cushion": Counter({"good": 2, "ours": 1}),
    "shoes": Counter({"ours": 1}),
    "book": Counter({"good": 2, "ours": 1}),
    "stool": Counter({"tie": 4, "good": 1}),
    "vase": Counter({"good": 4}),
    "cat": Counter({"good": 3, "tie": 2}),
    "lamp": Counter({"good": 3}),
    "computer": Counter({"tie": 2, "ours": 1}),
    "pencil": Counter({"good": 2, "tie": 2}),
    "cup": Counter({"good": 1, "tie": 1}),
    "cake": Counter({"good": 2, "tie": 1}),
    "painting": Counter({"tie": 2, "good": 1}),
    "bag": Counter({"tie": 4}),
}

pprint(individiaul)

pprint(luke)
