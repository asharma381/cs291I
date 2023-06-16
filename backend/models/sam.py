from PIL import Image
from typing import List
import numpy as np
import matplotlib.pyplot as plt
from segment_anything import sam_model_registry, SamAutomaticMaskGenerator

def show_mask(mask, box, ax, random_color=False):
    import numpy as np
    if random_color:
        color = np.concatenate([np.random.random(3), np.array([0.6])], axis=0)
    else:
        color = np.array([30/255, 144/255, 255/255, 0.6])
    h, w = mask.shape[-2:]
    mask_image = mask.reshape(h, w, 1) * color.reshape(1, 1, -1)
    ax.imshow(mask_image)

def do_get_boxes(image: Image.Image) -> List[List[int]]:
    image = np.array(image)
    sam_checkpoint = "checkpoints/sam_vit_h_4b8939.pth" # change back to 'checkpoints/'
    model_type = "vit_h"
    device = "cuda"

    sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
    sam.to(device=device)

    mask_generator = SamAutomaticMaskGenerator(
        model=sam,
        points_per_side=16,
        pred_iou_thresh=0.86,
        stability_score_thresh=0.92,
        # crop_n_layers=0,
        # crop_n_points_downscale_factor=2,
        min_mask_region_area=10_000,  # Requires open-cv to run post-processing
    )

    masks = mask_generator.generate(image)
    boxes = [mask["bbox"] for mask in masks]

    # visualize masks / boxes
    # fig, ax = plt.subplots(1, 1, figsize=(6, 6))
    # ax.imshow(image)
    # box = np.array(boxes)
    # print(len(masks))
    # for i, mask in enumerate(masks):
    #     show_mask(np.array(mask["segmentation"]), np.array(boxes), ax, random_color=False)
    #     x1, y1, x2, y2 = box[i][0], box[i][1], box[i][2], box[i][3]
    #     if i % 5 == 0:
    #         plt.savefig("sam" + str(i) + ".png")
    
    # plt.savefig("sam.png")    
    
    return [mask["bbox"] for mask in masks]


if __name__ == "__main__":
    image = Image.open("narrow.jpg")
    # print("calling func")
    print(do_get_boxes(image))
