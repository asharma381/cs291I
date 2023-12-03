import json

JSON_PATH = "gdino_dot_sep_25.json"
data = json.load(open(JSON_PATH))
cleaned_data = {}

for img, nouns in data.items():
    all_nouns = set()
    for noun in nouns:
        all_nouns.update(sn.replace("##", "") for sn in noun.split(" "))
    cleaned_data[img.split("/")[1]] = sorted(all_nouns)

json.dump(cleaned_data, open(f"{JSON_PATH.split('.')[0]}_cleaned.json", "w"))
