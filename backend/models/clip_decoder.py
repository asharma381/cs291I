from typing import List
from PIL import Image
from PIL import Image
import torch
import matplotlib.pyplot as plt
from clip_text_decoder.model import ImageCaptionInferenceModel


def do_get_texts(image: Image.Image, boxes: List[List[int]]) -> List[str]:
    dc_model = ImageCaptionInferenceModel.load("checkpoints/pretrained-model-1.4.0.pt")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    dc_model.to(device)

    captions = []
    print("START:------------")
    i = 0
    for x, y, w, h in boxes:
        cropped = image.crop((x, y, x + w, y + h))
        caption = dc_model(cropped, beam_size=1)
        cropped.save(f"caption_imgs/{i}_{caption}.png")
        print(caption)
        # fig, ax = plt.subplots(1, 1, figsize=(6, 6))
        # ax.imshow(cropped)
        # plt.savefig("clip_decoder" + str(x)+ ".png")
        # print(caption)
        caption_list = caption.lower().replace(".", "").split(" ")
        captions.extend(caption_list)
        i += 1
    print("END:--------------")
    return captions


if __name__ == "__main__":
    print("hi")
    image = Image.open("../narrow.jpg")
    boxes = [
        [479, 202, 181, 155],
        [254, 468, 312, 286],
        [836, 45, 288, 283],
        [1060, 0, 64, 45],
        [15, 0, 29, 31],
        [80, 470, 101, 161],
        [12, 558, 121, 133],
        [291, 667, 388, 172],
        [119, 68, 298, 298],
        [248, 297, 94, 55],
        [0, 570, 93, 269],
        [896, 525, 228, 137],
        [161, 304, 94, 60],
        [759, 526, 365, 140],
        [0, 0, 57, 565],
        [837, 164, 57, 25],
        [0, 0, 132, 691],
        [829, 326, 179, 114],
        [828, 275, 77, 41],
        [590, 644, 31, 26],
        [173, 232, 212, 75],
        [774, 227, 146, 46],
        [148, 230, 30, 77],
        [759, 623, 145, 44],
        [666, 660, 103, 105],
        [567, 104, 115, 37],
        [215, 559, 40, 67],
        [215, 577, 30, 49],
        [566, 507, 115, 59],
        [947, 434, 60, 39],
        [849, 650, 33, 31],
        [764, 221, 182, 98],
        [414, 0, 317, 205],
        [0, 315, 1124, 524],
        [40, 0, 1049, 43],
        [0, 0, 1124, 838],
        [255, 470, 424, 369],
        [119, 69, 263, 159],
        [682, 431, 237, 200],
        [663, 409, 461, 354],
        [19, 34, 984, 448],
        [763, 98, 182, 221],
        [148, 216, 269, 149],
        [622, 0, 464, 44],
        [547, 22, 98, 84],
        [766, 98, 167, 123],
        [1063, 804, 61, 36],
        [1007, 0, 86, 44],
    ]
    print(do_get_texts(image, boxes))
