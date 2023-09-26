import csv
from collections import defaultdict
from random import randint

IMAGES_PER_TASK = 6
CSV_NAME = "Gamma_v_Omega.csv"

codename_to_group = {
    "gamma": "good",
    "alpha": "octopus_vqa",
    "chi": "octopus_clipseg",
    "rho": "random",
    "omega": "bad",
}

scores = defaultdict(int)
if __name__ == "__main__":
    with open(CSV_NAME) as csvfile:
        reader = csv.DictReader(csvfile)
        num_fails = 0

        for row in reader:
            i = randint(1, 6)

            if (
                ("omega" in row[f"Input.imgl{i}"] and "gamma" in row[f"Input.imgr{i}"] and row[f"Answer.{i}2.{i}2"] == "false")
                or ("omega" in row[f"Input.imgr{i}"] and "gamma" in row[f"Input.imgl{i}"] and row[f"Answer.{i}1.{i}1"] == "false")
            ):
                num_fails += 1
                print("Fail #" + str(num_fails))
                continue

            for i in range(1, IMAGES_PER_TASK + 1):
                if row[f"Answer.{i}1.{i}1"] == "true":
                    for codename, group in codename_to_group.items():
                        if codename in row[f"Input.imgl{i}"]:
                            scores[group] += 1
                if row[f"Answer.{i}2.{i}2"] == "true":
                    for codename, group in codename_to_group.items():
                        if codename in row[f"Input.imgr{i}"]:
                            scores[group] += 1
                if row[f"Answer.{i}3.{i}3"] == "true":
                    scores["tie"] += 1


print(dict(scores))

