from models.clip_seg import do_filter_nouns
import json
from PIL import Image
from tqdm import tqdm

unfiltered = json.load(open("../scp/scp_data.json"))
results = {}
for img, predictions in tqdm(unfiltered.items()):
    nouns = predictions["nouns"]
    img_path = img
    image = Image.open(img_path)
    filtered_nouns = do_filter_nouns(image, nouns)
    results[img] = filtered_nouns
    json.dump(results, open("vilt.json", "w"))
