""" Computes scores for Stage 2. """

import json
import sys

from absl import app, flags
from sentence_transformers import SentenceTransformer, util
from tqdm import tqdm
from utils import load_json

FLAGS = flags.FLAGS
flags.DEFINE_string("score", "", "Path to score json file.")
flags.DEFINE_string("truth", "", "Path to ground truth json file.")

model = SentenceTransformer("all-MiniLM-L6-v2")


def main(unused_argv):
    model_data = load_json(FLAGS.score)
    ground_truth = load_json(FLAGS.truth)

    # Compute Scores
    avg_target_noun_freq = 0
    sBERT_score = 0

    for i, img in enumerate(tqdm(model_data)):
        print(img)

        target_noun_freq = 0
        avg_sBERT_score_img = 0

        for obj in ground_truth[img]:
            candidate_noun = model_data[img][obj]
            if candidate_noun in ground_truth[img][obj]:
                target_noun_freq += 1

            max_sBERT_obj = -1 * sys.maxsize
            for reference_noun in ground_truth[img][obj]:
                # Compute sBERT between candidate_nouns and noun
                print(reference_noun, candidate_noun)
                scores = util.cos_sim(
                    model.encode(candidate_noun, convert_to_tensor=True),
                    model.encode(reference_noun, convert_to_tensor=True),
                )
                max_sBERT_obj = max(max_sBERT_obj, scores[0][0])
            avg_sBERT_score_img += max_sBERT_obj
            print(max_sBERT_obj)
        avg_sBERT_score_img /= len(ground_truth[img])
        target_noun_freq /= len(ground_truth[img])
        print(avg_sBERT_score_img)
        print(target_noun_freq)
        avg_target_noun_freq += target_noun_freq
        sBERT_score += avg_sBERT_score_img

    avg_target_noun_freq /= len(model_data)
    sBERT_score /= len(model_data)
    print("Avg Target Noun Freq", avg_target_noun_freq)
    print("sBERT Score", sBERT_score.tolist())


if __name__ == "__main__":
    app.run(main)
