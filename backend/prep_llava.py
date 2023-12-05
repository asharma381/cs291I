import csv
import json
import os

output = [["image", "url", "prompt", "answer"]]

f = sorted(os.listdir("good_bad"))

for i, img in enumerate(f):
    url = (
        "https://raw.githubusercontent.com/asharma381/cs291I/main/backend/good_bad/"
        + str(img)
    )
    prompt = (
        "Which of the two images proposes a more natural location for the "
        + str(img.split("_")[1])
        + ' to be placed? If both locations are equally natural, then select tie. Answer one of the following options: "Image 1", "Image 2", Tie.'
    )

    ans = str(img.split("_")[-1]).replace(".png", "")
    if ans == "good":
        a = "Image 1"
    else:
        a = "Image 2"

    output.append([img, url, prompt, a])

with open("llava_eval.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerows(output)
