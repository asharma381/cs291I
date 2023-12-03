import json
import re

JSON_PATH = "clipseg.json"
K = 10

data = json.load(open(JSON_PATH))
cleaned_data = {}

for img, centers in data.items():
    sorted_centers = sorted(centers.items(), key=lambda x: x[1][2], reverse=True)[:K]

    cleaned_data[img.split("/")[1]] = sorted(dict(sorted_centers).keys())

json.dump(cleaned_data, open(f"{JSON_PATH.split('.')[0]}_{K}_cleaned.json", "w"))
