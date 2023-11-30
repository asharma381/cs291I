import os
import random
from PIL import Image, ImageDraw, ImageFont

padding = 50

# Path to the folders
all_bad_locs_folder = 'all_bad_locs'
all_good_locs_folder = 'all_good_locs'

# Get the list of image files in the folders
all_bad_locs_files = os.listdir(all_bad_locs_folder)
all_good_locs_files = os.listdir(all_good_locs_folder)

# Set the font for the labels
font = ImageFont.truetype("arial.ttf", 25)

for filename in sorted(set(all_bad_locs_files) & set(all_good_locs_files)):
    bad_image = Image.open(os.path.join(all_bad_locs_folder, filename))
    good_image = Image.open(os.path.join(all_good_locs_folder, filename))

    if bad_image.width != good_image.width or bad_image.height != good_image.height:
        print(f"Skipping {filename} because the images are not the same size")
        break
    width = bad_image.width
    height = bad_image.height

    side_by_side_image = Image.new('RGB', (width + width + padding, height + padding), (255, 255, 255))
    draw = ImageDraw.Draw(side_by_side_image)

    if random.random() < 0.5:
        side_by_side_image.paste(bad_image, (0, 0))
        side_by_side_image.paste(good_image, (width + padding, 0))
        output_filename = filename.split(".")[0] + "_left_bad.png"
    else:
        side_by_side_image.paste(bad_image, (width + padding, 0))
        side_by_side_image.paste(good_image, (0, 0))
        output_filename = filename.split(".")[0] + "_left_good.png"
    
    draw.text((width // 2, height + padding // 2), 'Image 1', fill='black', font=font, anchor="mm")
    draw.text((width + padding + width // 2, height + padding // 2), 'Image 2', fill='black', font=font, anchor="mm")
    side_by_side_image.save(f"good_bad/{output_filename}")
    
