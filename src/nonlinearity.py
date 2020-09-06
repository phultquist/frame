max_pixel_brightness = 255
brightness_gamma = 1.4

def compensate(original):
    # print(original)
    original = int(original)
    if original == 0:
        return 0
    return int((original ** brightness_gamma) * (max_pixel_brightness ** (1 - brightness_gamma)))