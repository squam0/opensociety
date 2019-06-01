IMAGE_PATH_BASE = "../data/images/"

image_dict = {
    "terrain": {
        "grass": "greengrass.png"
    }
}

for category in image_dict:
    for image in image_dict[category]:
        image_dict[category][image] = "".join((IMAGE_PATH_BASE,
            image_dict[category][image]))
