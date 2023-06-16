from transformers import CLIPSegProcessor, CLIPSegForImageSegmentation
import torch
from PIL import Image
from typing import Dict, Tuple
import scipy.ndimage as ndi
import matplotlib.pyplot as plt


processor = CLIPSegProcessor.from_pretrained("CIDAS/clipseg-rd64-refined")
# ADD TO CUDA
model = CLIPSegForImageSegmentation.from_pretrained("CIDAS/clipseg-rd64-refined")

# prompts = ["backpack", "chair", "computer", "desk", "floor", "paper", "pencil", "book", "cutlery", "pancakes", "blueberries", "orange juice", "coffee", "chair", "floor"]

prompts = ["table", "computer"]

def get_centers(image: Image.Image) -> Dict[str, Tuple[int, int]]:
    # image = Image.open("narrow.jpg")
    print("SHAPE:")
    print(image.size)
    inputs = processor(text=prompts, images=[image] * len(prompts), padding="max_length", return_tensors="pt")
    # predict
    with torch.no_grad():
        outputs = model(**inputs)
        preds = outputs.logits.unsqueeze(1)
    # print("after pred")

    
    heatmap_1 = preds[1][0].numpy()
    # print("SHAPE")
    # print(heatmap_1.shape)
    import numpy as np
    heatmap_1 = heatmap_1 - np.min(heatmap_1)
    # heatmap_1 = np.max(heatmap_1) - heatmap_1
    # print(np.unravel_index(heatmap_1.argmax(), heatmap_1.shape))
    # cy, cx = ndi.center_of_mass(heatmap_1)
    cy, cx = np.unravel_index(heatmap_1.argmax(), heatmap_1.shape)

    cx = image.size[0] * cx / 352
    cy = image.size[1] * cy / 352

    # print(np.min(heatmap_1))
    # print(np.max(heatmap_1))
    # print(heatmap_1[250,150])
    # print(heatmap_1[0,0])

    # print(cy, cx)
    fig, ax = plt.subplots()

    ax.scatter(cx, cy, s=160, c='C0', marker='+')
    ax.imshow(image)


    # _, ax = plt.subplots(1, len(prompts) + 1, figsize=(3*(len(prompts) + 1), 4))
    # [a.axis('off') for a in ax.flatten()]
    # ax[0].imshow(image)
    # [ax[i+1].imshow(preds[i][0]) for i in range(len(prompts))]
    # [ax[i+1].text(0, -15, prompt) for i, prompt in enumerate(prompts)]
    plt.savefig("test.png")
    return cx, cy

# get_centers(Image.open("wide.jpg"))