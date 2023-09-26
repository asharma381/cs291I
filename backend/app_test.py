from models.shap_e import do_text_to_3d
from models.clip_seg import do_get_centers
from models.sam import do_get_boxes
from models.clip_decoder import do_get_texts
from models.pos_tag import do_get_nouns
from models.gpt import do_get_best_noun
import requests
from pyngrok import ngrok
from sys import argv
from flask import Flask, send_file, request
import io
import base64
from PIL import Image
import matplotlib.pyplot as plt


# # Set up ngrok
# ngrokToken = "2OoIGWxJlB5NFeejg3ht6Ez0wCi_5i3BG9dRdWcozUQZrftxW"
# ngrok.set_auth_token(ngrokToken)
# public_url = ngrok.connect(5000).data["public_url"]
# print(public_url)

# # Send url to CSIL
# requests.post("http://128.111.30.213:6969/url", json={"url": public_url})

# # Create Flask app
# app = Flask(__name__)
# app.config["MAX_CONTENT_LENGTH"] = 5_000_000_000_000_000

# scriptName = argv[0]


# @app.route("/")
# def hello():
#     retString = "Hello Hollerer"
#     return retString


# @app.route("/get_placement", methods=["POST"])
def get_placement():
    # import time;
    # t0 = time.time()
    prompt = "a cake"
    image = Image.open("desk_narrow.jpg")
    # Decode image
    # data = request.get_data(as_text=True)
    # dataImg = data.split("<ENCODING")[1]
    # dataImg = dataImg.split("</ENCODING>")[0]
    # image_bytes = base64.b64decode(str(dataImg))
    # image = Image.open(io.BytesIO(image_bytes))

    # dataPrompt = data.split("<PROMPT>")[1]
    # prompt = dataPrompt.split("</PROMPT>")[0]

    print("\n\nPROMPT:" + prompt)

    # Get bounding boxes
    print("In get_placement")
    boxes = do_get_boxes(image)
    print("Got boxes")
    # Get text for each bounding box
    captions = do_get_texts(image, boxes)
    print("Got texts")
    # Get all nouns
    nouns = do_get_nouns(captions)
    print("Got nouns")
    # Get clip segmentation for each noun with strong response
    centers = do_get_centers(image, nouns)
    print("Got centers")
    print(centers)
    # Get best noun from GPT
    best_noun = do_get_best_noun(centers.keys(), prompt)
    x, y, _ = centers[best_noun]
    print('Got best noun: centers["' + best_noun + '"] = ' + str(x) + ", " + str(y))
    
    fig,ax = plt.subplots(1)
    ax.set_aspect('equal')


    # Show the image
    import numpy as np
    ax.imshow(np.asarray(image))
    ax.scatter(x, y, s=50, c="C0", marker="+")


    # Show the image
    plt.savefig("test_cake_desk_narrow.png", dpi=300)

    # t1 = time.time()
    # print("Total time: " + str(t1 - t0))
    # return {"x": x, "y": y}

get_placement()


# @app.route("/text_to_3d", methods=["POST"])
# def text_to_3d():
#     if not request.json:
#         return "No JSON received", 400
#     prompt = request.json["prompt"]
#     full_path = do_text_to_3d(prompt)
#     return send_file(full_path)


# if __name__ == "__main__":
#     app.run(host="0.0.0.0")


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
}
