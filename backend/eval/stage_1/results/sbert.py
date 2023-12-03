""" Computes scores for Stage 1. """

import json
import sys

from absl import app, flags
from sentence_transformers import SentenceTransformer, util
from tqdm import tqdm

def load_json(filename):
    return json.load(open(filename))

FLAGS = flags.FLAGS
flags.DEFINE_string("score", "", "Path to score json file.")
flags.DEFINE_string("truth", "", "Path to ground truth json file.")

model = SentenceTransformer("all-MiniLM-L6-v2")


def main(unused_argv):
    model_data = load_json(FLAGS.score)
    ground_truth = load_json(FLAGS.truth)

    # Compute Scores
    sBERT_score = 0

    for i, img in enumerate(tqdm(ground_truth)):
        print(img)
        candidate_nouns = model_data[img]
        print("nouns:", candidate_nouns)
        avg_sBERT_score_img = 0
        for obj in ground_truth[img]:
            max_sBERT_obj = -1 * sys.maxsize
            for reference_noun in ground_truth[img][obj]:
                # Compute sBERT between candidate_nouns and noun
                reference_nouns = [reference_noun] * len(candidate_nouns)
                scores = util.cos_sim(
                    model.encode(candidate_nouns, convert_to_tensor=True),
                    model.encode(reference_nouns, convert_to_tensor=True),
                )
                score = max([scores[idx][idx] for idx in range(len(candidate_nouns))])
                max_sBERT_obj = max(max_sBERT_obj, score.tolist())
            avg_sBERT_score_img += max_sBERT_obj
        avg_sBERT_score_img /= len(ground_truth[img])
        sBERT_score += avg_sBERT_score_img
        print("avg_sBERT_score_img:", avg_sBERT_score_img)

    sBERT_score /= len(ground_truth)
    print(sBERT_score)
    # print("truth:", ground_truth[img][obj])
    # print("truth:", ground_truth[img])


if __name__ == "__main__":
    app.run(main)