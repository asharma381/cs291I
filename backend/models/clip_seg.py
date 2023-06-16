from transformers import CLIPSegProcessor, CLIPSegForImageSegmentation, ViltProcessor, ViltForQuestionAnswering
import torch
from PIL import Image
from typing import Dict, Tuple, List
import scipy.ndimage as ndi
import matplotlib.pyplot as plt
import io
import base64
from pprint import pprint
from itertools import islice
import numpy as np


processor = CLIPSegProcessor.from_pretrained("CIDAS/clipseg-rd64-refined")
model = CLIPSegForImageSegmentation.from_pretrained("CIDAS/clipseg-rd64-refined")

vqa_processor = ViltProcessor.from_pretrained("dandelin/vilt-b32-finetuned-vqa")
vqa_model = ViltForQuestionAnswering.from_pretrained("dandelin/vilt-b32-finetuned-vqa")


def do_filter_nouns(
    image: Image.Image, nouns: List[str]
) -> List[str]:
    # vqa to determine if in image
    prompts = []
    for noun in nouns:
        question = f"Is there a {noun} in the image?"
        encoding = vqa_processor(image, question, return_tensors="pt")
        outputs = vqa_model(**encoding)
        logits = outputs.logits
        idx = logits.argmax(-1).item()
        in_image = vqa_model.config.id2label[idx]
        if "yes" in in_image.lower():
            prompts.append(noun)
        
    print(f"In image: {prompts}")
    return prompts

def do_get_center(image: Image.Image, prompt: str) -> Tuple[int, int]:
    # clip seg
    inputs = processor(
        text=prompt,
        images=image,
        padding="max_length",
        return_tensors="pt",
    )
    # predict
    with torch.no_grad():
        outputs = model(**inputs)  # type: ignore
        preds = outputs.logits

    heatmap = preds.numpy()
    print(heatmap.shape)
    cy, cx = np.unravel_index(heatmap.argmax(), heatmap.shape)
    cx = image.size[0] * cx / 352
    cy = image.size[1] * cy / 352
    print(f"Center for {prompt} is {cx}, {cy}")
    print(f"Type of map: {heatmap.dtype} {type(cx)}")
    return cx, cy



def do_get_centers(
    image: Image.Image, prompts: List[str], k: int = 20
) -> Dict[str, Tuple[int, int]]:
    centers = {}

    # clip seg
    inputs = processor(
        text=prompts,
        images=[image] * len(prompts),
        padding="max_length",
        return_tensors="pt",
    )
    # predict
    with torch.no_grad():
        outputs = model(**inputs)  # type: ignore
        preds = outputs.logits.unsqueeze(1)


    fig, ax = plt.subplots()

    for i in range(len(prompts)):
        heatmap = preds[i][0].numpy()
        heatmap = heatmap - np.min(heatmap)
        cy, cx = np.unravel_index(heatmap.argmax(), heatmap.shape)
        # uncomment for now
        # print(prompts[i], ": (y,x) = ", heatmap[int(cy)][int(cx)])
        val = heatmap[int(cy)][int(cx)]
        cx = image.size[0] * cx / 352
        cy = image.size[1] * cy / 352
        # if prompts[i] == "table":
        #     ax.text(cx, cy, prompts[i], fontsize=10, bbox=dict(facecolor="red", alpha=0.25))
        #     ax.scatter(cx, cy, s=50, c="C0", marker="+")
        #     ax.imshow(image)

        # add to dict
        prompts[i] = prompts[i].replace(",", "")
        centers[prompts[i]] = (cx, cy, val)

    # centers = dict(sorted(centers.items(), key=lambda x: x[1][2], reverse=True))
    sorted_centers = sorted(centers.items(), key=lambda x: x[1][2], reverse=True)
    print(type(sorted_centers))
    if len(centers) > k:
        centers = dict(sorted_centers[:k])
        # centers = list(islice(centers.iter))
    # print(len(centers))

    # heatmap_1 = preds[1][0].numpy()
    # print("SHAPE")
    # print(heatmap_1.shape)
    # import numpy as np

    # heatmap_1 = heatmap_1 - np.min(heatmap_1)
    # heatmap_1 = np.max(heatmap_1) - heatmap_1
    # print(np.unravel_index(heatmap_1.argmax(), heatmap_1.shape))
    # cy, cx = ndi.center_of_mass(heatmap_1)
    # cy, cx = np.unravel_index(heatmap_1.argmax(), heatmap_1.shape)

    # cx = image.size[0] * cx / 352
    # cy = image.size[1] * cy / 352

    # print(np.min(heatmap_1))
    # print(np.max(heatmap_1))
    # print(heatmap_1[250,150])
    # print(heatmap_1[0,0])

    # print(cy, cx)
    fig, ax = plt.subplots()

    ax.scatter(cx, cy, s=160, c="C0", marker="+")
    ax.imshow(image)

    _, ax = plt.subplots(1, len(prompts) + 1, figsize=(3*(len(prompts) + 1), 4))
    [a.axis('off') for a in ax.flatten()]
    ax[0].imshow(image)
    [ax[i+1].imshow(preds[i][0]) for i in range(len(prompts))]
    [ax[i+1].text(0, -15, prompt) for i, prompt in enumerate(prompts)]
    plt.savefig("test.png")
    return centers


if __name__ == "__main__":
    image = Image.open("../narrow.jpg")
    test_nouns = [
        "carpet",
        "coffee",
        "top",
        "cloth",
        "blanket",
        "tablet",
        "view",
        "chairs",
        "seat",
        "sink",
        "chair",
        "floor",
        "holder",
        "building",
        "faucet",
        "hole",
        "up",
        "room",
        "round",
        "pair",
        "cup",
        "background",
        "desk",
        "computer",
        "truck",
        "toothbrush",
        "object",
        "backpack",
        "plate",
        "window",
        "square",
        "piece",
        "photo",
        "keyboard",
        "scissors",
        "envelope",
        "table",
        "forest",
        "tree",
        "laptop",
        "train",
        "wood",
        "metal",
        "ring",
        "close",
        "street",
        "cat",
        "bed",
        "cover",
        "picture",
        "mouse",
        "box",
    ]
    centers = do_get_centers(image, test_nouns)
    print(centers)
    print(list(centers.keys()))


{
    "laptop": (357.95454545454544, 160.26704545454547, 12.976805),
    "backpack": (616.8323863636364, 52.625, 12.740499),
    "computer": (357.95454545454544, 121.99431818181819, 12.189806),
    "keyboard": (294.03409090909093, 265.51704545454544, 12.123257),
    "chair": (712.7130681818181, 461.66477272727275, 11.267924),
    "tablet": (357.95454545454544, 121.99431818181819, 11.215098),
    "chairs": (460.22727272727275, 574.0909090909091, 11.152715),
    "seat": (709.5170454545455, 459.27272727272725, 10.31825),
    "toothbrush": (811.7897727272727, 157.875, 10.054489),
    "blanket": (620.0284090909091, 35.88068181818182, 10.005478),
    "forest": (869.3181818181819, 160.26704545454547, 10.004445),
    "envelope": (549.7159090909091, 291.82954545454544, 9.896426),
    "tree": (869.3181818181819, 153.0909090909091, 9.876694),
    "cloth": (626.4204545454545, 57.40909090909091, 9.35051),
    "window": (799.0056818181819, 155.48295454545453, 9.231896),
    "table": (479.40340909090907, 382.72727272727275, 8.757629),
    "hole": (1029.1193181818182, 650.6363636363636, 8.310701),
    "object": (811.7897727272727, 157.875, 8.168312),
    "pair": (805.3977272727273, 153.0909090909091, 8.025748),
    "plate": (1029.1193181818182, 650.6363636363636, 8.003742),
    "cup": (783.0255681818181, 112.42613636363636, 7.968891),
    "desk": (453.83522727272725, 382.72727272727275, 7.959724),
    "faucet": (805.3977272727273, 153.0909090909091, 7.6755795),
    "metal": (150.2130681818182, 193.7556818181818, 7.559865),
    "photo": (294.03409090909093, 112.42613636363636, 7.4141355),
    "round": (1022.7272727272727, 650.6363636363636, 7.40605),
    "scissors": (814.9857954545455, 155.48295454545453, 7.392294),
    "cover": (549.7159090909091, 291.82954545454544, 7.384019),
    "ring": (210.9375, 181.79545454545453, 7.29897),
    "coffee": (783.0255681818181, 112.42613636363636, 7.2290773),
    "box": (814.9857954545455, 306.1818181818182, 7.19343),
    "floor": (51.13636363636363, 705.6534090909091, 6.9264736),
    "mouse": (201.3494318181818, 117.21022727272727, 6.8171487),
    "train": (853.3380681818181, 157.875, 6.7566004),
    "truck": (869.3181818181819, 186.57954545454547, 6.332479),
    "close": (805.3977272727273, 153.0909090909091, 6.2841945),
    "square": (856.5340909090909, 153.0909090909091, 6.246097),
    "up": (201.3494318181818, 124.38636363636364, 6.1048245),
    "view": (357.95454545454544, 155.48295454545453, 5.8325543),
    "holder": (802.2017045454545, 165.05113636363637, 5.7957926),
    "building": (869.3181818181819, 191.36363636363637, 5.756831),
    "picture": (802.2017045454545, 157.875, 5.7332187),
    "sink": (853.3380681818181, 157.875, 5.637163),
    "piece": (818.1818181818181, 153.0909090909091, 5.5657086),
    "bed": (869.3181818181819, 200.9318181818182, 5.371008),
    "top": (294.03409090909093, 114.81818181818181, 5.2554626),
    "carpet": (917.2585227272727, 459.27272727272725, 5.22156),
    "street": (853.3380681818181, 157.875, 5.107485),
    "cat": (869.3181818181819, 191.36363636363637, 4.901128),
    "background": (357.95454545454544, 148.3068181818182, 4.803027),
    "room": (1013.1392045454545, 423.39204545454544, 4.4373226),
    "wood": (83.0965909090909, 612.3636363636364, 4.1797724),
}
