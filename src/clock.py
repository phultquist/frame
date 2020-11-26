from datetime import datetime
import PIL.Image
import numpy as np
import settings

to_display = '0000'

black_replacement = [0,0,0,255]
gray_replacement = [0,0,0,255]


def get_image_ref(style, digit):
    return 'assets/clock/'+style+'-'+str(digit)+'.png'

def get_image(src):
    img = PIL.Image.open(src)
    # img.show()
    return img

all_images = []

def set_digit_images():
    global all_images
    all_images = []
    for i in range(10):
        clock_style = settings.get()["clock"]
        if not (clock_style == "modern"):
            clock_style = "classic"
        ref = get_image_ref(clock_style, i)
        all_images.append(get_image(ref))

def combine_horizontally(n1, n2):
    n1 = int(n1)
    n2 = int(n2)
    first_num_pixels = np.array(all_images[n1]).tolist()
    second_num_pixels = np.array(all_images[n2]).tolist()

    new_image_pixels = []

    for y in range(len(first_num_pixels)):
        row = first_num_pixels[y]
        while len(row) < 8:
            row.append([130,130,130,255])

        for x in range(8):
            row2 = second_num_pixels[y]
            while len(row2) < 8:
                row2.insert(0, [130,130,130,255])
            row.append(row2[x])

        new_image_pixels.append(np.uint8(row))

    return new_image_pixels

def combine_vertically(top, bottom):
    all_px = top
    colors_to_replace = [
        ([0, 0, 0, 255], black_replacement), # replace black with...
        ([136, 136, 136, 255], gray_replacement) # replace gray with...
    ]
    # print(colors_to_replace)
    while len(top) < 8:
        newrow = [[130,130,130,255]] * 16
        newrow = np.uint8(newrow)
        top.append(newrow)

    while len(bottom) < 8:
        newrow = [[130,130,130,255]] * 16
        newrow = np.uint8(newrow)
        bottom.insert(0, newrow)

    for y in range(len(bottom)):
        all_px.append(bottom[y])
    # print(all_px)
    for pair in colors_to_replace:
        for y in range(len(all_px)):
            for x in range(len(all_px[y])):
                if (all_px[y][x] == pair[0]).all():
                    all_px[y][x] = pair[1]

    return all_px

def now():
    set_digit_images()
    global to_display
    global black_replacement
    black_replacement = settings.check("clockColor").split(",")
    black_replacement.append(255)
    # print(settings.check("clockColor").split(','))

    use_24_hour_clock = settings.check("clockTiming") == "24"
    to_display = datetime.now().strftime("%I%M")

    if use_24_hour_clock:
        to_display = datetime.now().strftime("%H%M")

    to_display = str(to_display)
    if len(to_display) != 4:
        to_display = '0000'

    top = combine_horizontally(to_display[0], to_display[1])
    bottom = combine_horizontally(to_display[2], to_display[3])

    combined = combine_vertically(top, bottom)
    im = PIL.Image.fromarray(np.array(combined))

    return im

now()
