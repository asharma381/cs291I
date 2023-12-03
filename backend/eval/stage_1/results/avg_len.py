import json

# JSON_FILE = "../vilt/vilt_cleaned.json"
JSON_FILE = "../gdino/gdino_comma_sep_25_cleaned.json"


data = json.load(open(JSON_FILE))

total = 0
for img, nouns in data.items():
    total += len(nouns)

avg = total / len(data)
print("Average number of nouns per image:", avg)
