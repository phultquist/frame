from datetime import datetime
import PIL.Image
import numpy as np

to_display = '0000'

def get_image_ref(style, digit):
    return 'assets/clock/'+style+'-'+str(digit)+'.png'


def get_image(src):
    img = PIL.Image.open(src)
    # img.show()
    return img


all_images = []

for i in range(10):
    ref = get_image_ref('modern', i)
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
            row.append([0, 0, 0, 255])

        for x in range(8):
            row2 = second_num_pixels[y]
            while len(row2) < 8:
                row2.insert(0, [0,0,0,255])

            row.append(row2[x])

        new_image_pixels.append(np.uint8(row))

    # im = PIL.Image.fromarray(np.array(new_image_pixels))
    # im.show()
    return new_image_pixels

def combine_vertically(top, bottom):
    all_px = top

    while len(top) < 8:
        newrow = [[0,0,0,255]] * 16
        newrow = np.uint8(newrow)
        top.append(newrow)

    while len(bottom) < 8:
        newrow = [[0,0,0,255]] * 16
        newrow = np.uint8(newrow)
        bottom.insert(0, newrow)

    for y in range(len(bottom)):
        all_px.append(bottom[y])

    return all_px

def now():
    global to_display
    to_display = datetime.now().strftime("%H%M")

    to_display = str(to_display)
    if len(to_display) > 4:
        to_display = '0000'

    top = combine_horizontally(to_display[0], to_display[1])
    bottom = combine_horizontally(to_display[2], to_display[3])

    combined = combine_vertically(top, bottom)
    im = PIL.Image.fromarray(np.array(combined))
    # im.show()
    im.save('assets/time.png', 'PNG')

now()