import json
from tqdm import tqdm
from PIL import Image
from models.sam import do_get_boxes
from models.clip_decoder import do_get_texts
from models.pos_tag import do_get_nouns

output_data = {}
f = open('good_data2.json')
data = json.load(f)
scenes = list(data.keys())
skip = True
for img in tqdm(scenes):
    img_path = f"original_images/{img}"
    output_data[img_path] = {}
    image = Image.open(img_path)

    boxes = do_get_boxes(image)
    captions = do_get_texts(image, boxes)
    output_data[img_path]["captions"] = captions
    nouns = do_get_nouns(captions)
    output_data[img_path]["nouns"] = nouns
    json.dump(output_data, open("scp_data_2.json", "w"))
