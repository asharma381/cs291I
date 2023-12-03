import json
import re

JSON_PATH = "vilt.json"

data = json.load(open(JSON_PATH))
cleaned_data = {}

for img, nouns in data.items():
    cleaned_data[img.split("/")[1]] = sorted(set(noun.replace(",", "").replace("\"", "") for noun in nouns if len(noun) > 0))

json.dump(cleaned_data, open(f"{JSON_PATH.split('.')[0]}_cleaned.json", "w"))
