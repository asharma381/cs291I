import json

data = json.load(open("gpt4v_dirty.json"))
for img, placements in data.items():
    for obj in placements:
        new = placements[obj].replace(".", "").lower()
        sold = new.split(" ")
        if len(sold) > 1:
            new = sold[-1]
        placements[obj] = new

json.dump(data, open("gpt4v.json", "w"))