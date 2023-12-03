import json

JSON_PATH = "scp.json"

data = json.load(open(JSON_PATH))
cleaned_data = {}

for img, info in data.items():
    cleaned_data[img.split("/")[1]] = sorted(info["nouns"])

json.dump(cleaned_data, open(f"{JSON_PATH.split('.')[0]}_cleaned.json", "w"))
