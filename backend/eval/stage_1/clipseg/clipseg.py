from models.clip_seg import do_get_centers
import json
from PIL import Image
from tqdm import tqdm

unfiltered = json.load(open("eval/stage_1/scp/scp_data.json"))
results = {}
for img, predictions in tqdm(unfiltered.items()):
    nouns = predictions["nouns"]
    img_path = img
    image = Image.open(f"images/{img_path}")
    centers = do_get_centers(image, nouns)
    for noun, center in centers.items():
        centers[noun] = [float(c) for c in center]
    results[img] = centers
    json.dump(results, open("clipsegcpu.json", "w"))
