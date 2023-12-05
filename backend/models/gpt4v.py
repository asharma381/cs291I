import base64
import json
import os

import requests
from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv()
# OpenAI API key
api_key = os.getenv("OPENAI_API_KEY")


# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def get_single_image(image_path, prompt):
    base64_image = encode_image(image_path)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "system",
                "content": "You are an expert in determining where objects should be placed in a scene. You are given an image " +
                "of a scene the name of an object to be placed in the scene. Please respond with a concise answer, one or two " +
                "words, naming the object in the scene on which the new object should be placed."
                # "content": "You are an expert in determining where objects should be placed in a scene. You are given an image " +
                # "of a scene the name of an object to be placed in the scene. Please respond with the pixel coordinates locating " +
                # "where in the scene would be the most natural location to place the object. The image is 561 pixels wide and 427 " +
                # "pixels wide, and the top left corner is the origin."
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"Where would be the most natural location to place a {prompt} in this image?",
                        # "text": f"Where would be the most natural location to place a {prompt} in this image? Give a one word response.",
                        # "text": f"Please answer the following question about the image in a single sentence. Question: {question}",
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                    },
                ],
            }
        ],
        "max_tokens": 200,
        # "response_format": {"type": "json_object"},
    }

    response = requests.post(
        "https://api.openai.com/v1/chat/completions", headers=headers, json=payload
    )

    return (response.json())["choices"][0]["message"]["content"]


# if __name__ == "__main__":
#     # SCENE DES: Please provide a scene description of this image.
#     # OBJ LIST: Please provide a list of objects in this image.
#     # DES + OBJ: Please provide a scene description listing the objects in the image.
#     # DES + OBJ in IMG: Please provide a scene description of this image listing where common indoor objects could be placed. Only list objects which are in the image.

#     # Final Prompt for Nouns:
#     # Please provide a list of nouns (where each noun is in "<NOUN>" tag) that could be used to describe this image. This listing should include where common indoor objects could be placed. Only list objects which are in the image.
#     imgs = sorted(os.listdir("../original_images"))
#     target_image = "../original_images/" + imgs[50]
#     prompt = "Please provide a list of nouns (where each noun is separated by comma, example: object1, object2, object3) that could be used to describe this image. This listing should include where common indoor objects could be placed. Only list objects which are in the image."
#     res = get_single_image(target_image, prompt)

#     output = {}
#     for i, img in tqdm(enumerate(imgs)):
#         target_image = "../original_images/" + str(img)
#         res = get_single_image(target_image, prompt)
#         output[str(img)] = res

#     with open("gpt4v.json", "w") as fp:
#         json.dump(output, fp)

data = json.load(open("../eval/stage_1/ground_truth.json"))
output_data = {}
for img_name, obj_to_placement in tqdm(data.items()):
    if "133" in img_name:
        output_data[img_name] = {}
        for obj, placement in obj_to_placement.items():
            output = get_single_image(f"../images/original_images/{img_name}", obj)
            output_data[img_name][obj] = output
        json.dump(output_data, open("gpt4v.json", "w"))
