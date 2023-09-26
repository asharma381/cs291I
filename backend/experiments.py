from models.clip_seg import do_get_centers, do_filter_nouns, do_get_center
from models.sam import do_get_boxes
from models.clip_decoder import do_get_texts
from models.pos_tag import do_get_nouns
from models.gpt import do_get_best_noun
import io
import json
from PIL import Image
from tqdm import tqdm


def get_centers(image):
    # Get bounding boxes
    print("In get_placement")
    boxes = do_get_boxes(image)
    print("Got boxes")
    # Get text for each bounding box
    captions = do_get_texts(image, boxes)
    print("Got texts")
    # Get all nouns
    nouns = do_get_nouns(captions)
    print(f"Got nouns: {nouns}")
    # Get clip segmentation for each noun with strong response
    centers = do_get_centers(image, nouns)
    print("Got centers")
    print(centers)
    return centers

def get_placement(centers, prompt):
    # Get best noun from GPT
    best_noun = do_get_best_noun(centers.keys(), prompt)
    try:
        x, y, _ = centers[best_noun]
    except KeyError as e:
        # handle key error
        print('GPT failed us :(')
        x, y = -1, -1
    print('Got best noun for ', prompt, ': centers["' + best_noun + '"] = ' + str(x) + ", " + str(y))
    return x, y

def vqa_pipeline(image):
    # Get bounding boxes
    print("In get_placement")
    boxes = do_get_boxes(image)
    print("Got boxes")
    # Get text for each bounding box
    captions = do_get_texts(image, boxes)
    captions += ["floor"]
    # print("Got texts")
    # print(captions)
    # Get all nouns
    nouns = do_get_nouns(captions)
    print(f"Got nouns: {nouns}")
    filtered = do_filter_nouns(image, nouns)
    print(f"Filtered: {filtered}")
    return filtered

def get_info():
    f = open('octopus_exp.json')
    fails = 0
    count = 0
    data = json.load(f)
    scenes = list(data.keys())
    for n, i in enumerate(scenes):
        for o in list(data[i].keys()):
            if data[i][o][0] == -1:
                fails += 1
            count += 1
    print("Total", count, "objects in", len(scenes), "scenes")
    print("GPT-4 got", fails, "wrong!")

# TEST CODE TO CREATE FIGURES:
image = Image.open("desk_narrow.jpg")
filtered_nouns = vqa_pipeline(image)

# ACTUAL CODE:
# if __name__ == "__main__":
#     output_data = {}
#     f = open('good_data2.json')
#     data = json.load(f)
#     scenes = list(data.keys())
#     for n, i in enumerate(scenes):
#         print("Processing image #", n)
#         # img_path = 'exp_imgs/rgb_training_' + i + '.mat.png'
#         img_path = 'exp_imgs/' + i
#         output_data[img_path] = {}
#         image = Image.open(img_path)
#         # print(img_path)
#         objs = list(data[i].keys())
#         centers = get_centers(image)
        
#         for o in objs:
#             x, y = get_placement(centers, o)
#             # x, y = 342.65625, 337.23295454545456
#             output_data[img_path][o] = [x,y]
            
#             # with open("octopus_exp.json", "r") as file:
#                 # data_file = json.load(file)
#             # data_file = open("octopus_exp.json")
#             # json.dump(output_data, data_file)
#             json.dump(output_data, open("octopus_exp_2_old.json", "w"))



# if __name__ == "__main__":
#     output_data = {}
#     f = open('good_data1.json')
#     data = json.load(f)
#     scenes = list(data.keys())
#     for idx, image_name in enumerate(tqdm(scenes[:2])):
#         print("Processing image #", idx)
#         img_path = 'exp_imgs/' + image_name + '.png'
#         output_data[img_path] = {}
#         image = Image.open(img_path)

#         objs = list(data[image_name].keys())
#         filtered_nouns = vqa_pipeline(image)
#         print(f"Filtered: {filtered_nouns}")
        
#         for o in objs:
#             print(f"Object is: {o}")
#             best_loc = do_get_best_noun(filtered_nouns, o)
#             print(f"Best loc: {best_loc}")
#             x, y = do_get_center(image, best_loc)
#             print(f"Center: {x}, {y}")

#             # x, y = get_placement(centers, o)
#             # x, y = 342.65625, 337.23295454545456
#             output_data[img_path][o] = [int(x),int(y)]
            
#             # with open("octopus_exp.json", "r") as file:
#                 # data_file = json.load(file)
#             # data_file = open("octopus_exp.json")
#             # json.dump(output_data, data_file)
#             json.dump(output_data, open("octopus_exp_11_vqa.json", "w"))
            
            
# {'plant': (68.53125, 163.76420454545453, 11.681584), 'frame': (49.40625, 100.6846590909091, 11.030077), 
# 'tree': (89.25, 154.0596590909091, 10.210669), 'umbrella': (102.0, 19.40909090909091, 10.088939), 
# 'computer': (62.15625, 116.45454545454545, 9.77256), 'cabinet': (355.40625, 226.84375, 9.655558), 
# 'window': (270.9375, 72.7840909090909, 9.61083), 'sign': (49.40625, 92.19318181818181, 9.325917), 
# 'cupboard': (454.21875, 41.24431818181818, 9.264847), 'doorway': (299.625, 19.40909090909091, 8.996163), 
# 'flowers': (74.90625, 154.0596590909091, 8.796289), 'clock': (49.40625, 92.19318181818181, 8.651147), 
# 'towel': (235.875, 359.0681818181818, 8.460478), 'pole': (97.21875, 16.982954545454547, 8.366844), 
# 'sink': (176.90625, 240.1875, 8.26944), 'door': (471.75, 84.91477272727273, 8.217298), 
# 'vase': (159.375, 194.0909090909091, 7.989516), 'flower': (86.0625, 101.89772727272727, 7.813607), 
# "child's": (76.5, 115.24147727272727, 7.662731), 'hydrant': (159.375, 194.0909090909091, 7.3937397)}


# huggingface/tokenizers: The current process just got forked, after parallelism has already been used. Disabling parallelism to avoid deadlocks...
# To disable this warning, you can either:
#         - Avoid using `tokenizers` before the fork if possible
#         - Explicitly set the environment variable TOKENIZERS_PARALLELISM=(true | false)
# Got best noun for  apple : centers["tree"] = 89.25, 154.0596590909091
# GPT failed us :(
# Got best noun for  cake : centers["table"] = -1, -1
# Got best noun for  cup : centers["sink"] = 176.90625, 240.1875
# Got best noun for  plate : centers["cabinet"] = 355.40625, 226.84375
# Got best noun for  vase : centers["cabinet"] = 355.40625, 226.84375
# Got best noun for  stool : centers["pole"] = 97.21875, 16.982954545454547
# GPT failed us :(
# Got best noun for  painting : centers["wall"] = -1, -1
# Got best noun for  lamp : centers["cabinet"] = 355.40625, 226.84375
# GPT failed us :(
# Got best noun for  book : centers["shelf"] = -1, -1
# Got best noun for  bag : centers["hydrant"] = 159.375, 194.0909090909091
# Got best noun for  shoes : centers["hydrant"] = 159.375, 194.0909090909091
# GPT failed us :(
# Got best noun for  pencil : centers["table"] = -1, -1
# Got best noun for  cat : centers["tree"] = 89.25, 154.0596590909091
# GPT failed us :(
# Got best noun for  computer : centers["desk"] = -1, -1