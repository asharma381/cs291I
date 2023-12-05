import csv
import json

output = [["image", "prompt", "path"]]

with open("good_data1.json", "r") as f:
    data1 = json.load(f)

with open("good_data2.json", "r") as f:
    data2 = json.load(f)

for k, v in data1.items():
    image = (
        "https://raw.githubusercontent.com/asharma381/cs291I/main/backend/original_images/"
        + str(k)
        + ".png"
    )
    print(image)
    for obj in v:
        print(obj)
        prompt = "Add a " + obj
        path = str(k) + "_" + obj + ".png"
        print(path)
        output.append([image, prompt, path])

for k, v in data2.items():
    image = (
        "https://raw.githubusercontent.com/asharma381/cs291I/main/backend/original_images/"
        + str(k)
    )
    print(image)
    for obj in v:
        print(obj)
        a = str(k).split(".")[0]
        prompt = "Add a " + obj
        path = a + "_" + obj + ".png"
        print(path)
        output.append([image, prompt, path])


with open("pix2pix.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerows(output)
