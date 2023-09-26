import csv
from collections import defaultdict

IMAGES_PER_TASK = 6
CSV_NAME = "Gamma_v_Alpha_20.csv"

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
            fail = False
            for i in range(1, IMAGES_PER_TASK + 1):
                if (
                    ("omega" in row[f"Input.imgl{i}"] and "gamma" in row[f"Input.imgr{i}"] and row[f"Answer.{i}2.{i}2"] == "false")
                    or ("omega" in row[f"Input.imgr{i}"] and "gamma" in row[f"Input.imgl{i}"] and row[f"Answer.{i}1.{i}1"] == "false")
                ):
                    fail = True
                    num_fails += 1
                    print("fail #" + str(num_fails))

            if not fail:
                for i in range(1, IMAGES_PER_TASK + 1):
                    # UPDATE THIS LINE TO CHECK IF CURRENT TASK IS ATTENTION CHECK
                    if "omega" in row[f"Input.imgl{i}"] or "omega" in row[f"Input.imgr{i}"]:
                        continue
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

