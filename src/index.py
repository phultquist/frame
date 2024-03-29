import requests
import PIL.Image
from io import BytesIO
import numpy as np
import time
import driver
import sys
import exceptions
import numbers
import nonlinearity
import settings
import autobrightness
import clock
import nightshift
import fun

sys.path.append('/resize')
from resize import resize

def get_argument(index):
    try:
        a = sys.argv[index]
        return a
    except:
        return None

max_brightness = 0.50
min_brightness = 0.06
brt = 0.05
night_shift_value = 0

def get_brightness():
    brightness_setting = int(settings.get()['brightness']) / 100
    l = 45

    if settings.check("autobrightness") == False or settings.check("autobrightness") == "false":
        return brightness_setting

    try:
        l = light.lux()
        if (l) > 30:
            l = 30
        elif l < 0:
            l = 0
        l = (l * 10/3) / 100
    except:
        # there can be an overload of brightness, in which an error is thrown
        if setLeds:
            print('Error getting sensor value. Used 45')
    output = (l+(brightness_setting))/2

    # print("sensor: "+str(l), "setting: "+str(brightness_setting), "output: "+str(output))

    # output = autobrightness.get_output_brightness(brightness_setting, l, max_brightness=max_brightness, min_brightness=min_brightness)
    return output


def set_brightness(val):
    global brt
    
    brt = val
    if brt > max_brightness:
        brt = max_brightness
    elif brt < min_brightness:
        brt = min_brightness
    #print('Set brightness automatically to '+str(brt))

if get_argument(1) != None and get_argument(1) != "test" and get_argument(1) != 'auto':
    brt = int(get_argument(1)) / (max_brightness * 100)

if get_argument(1) == 'auto':
    import light
    import math
    set_brightness(get_brightness())

run_server = False

img = None

# if the LED strip is not on you, that is okay, make sure this is set to false; or, use the runtime variable "test"
setLeds = True

if get_argument(1) == 'test':
    setLeds = False

if setLeds:
    import board
    import neopixel
    pixels = neopixel.NeoPixel(board.D12, 256, auto_write=False)

def get_image(song):
    # print(song)
    try:
        imgurl = song.get('image_url')
    except:
        print('### error 1 ###')
        imgurl = exceptions.ERROR_IMAGE  # error 1

    return imgurl

# Finds the image based off of url/path
def find_image(locator):
    global img
    imgsource = locator
    if locator.startswith('http'):
        # try:
        imgresp = requests.get(locator)
        imgsource = BytesIO(imgresp.content)
        # except:
            # imgresp = requests.get(locator)
            # imgsource = BytesIO(imgresp.content)

    img = PIL.Image.open(imgsource)
    
    return img

# Gets the pixels given either the url or the exact image
def get_pixels(imgurl=None, image=None):
    global img

    if (imgurl== None) and not (image==None): # if actual image object passed in
        img = image
    else:
        find_image(imgurl)

    return manipulate()

# Reverses every second row, compensates for non-linearity, etc.
def manipulate():
    global img

    contrast_setting = int(settings.get()['contrast']) / 100 + 0.5
    imgpx = resize.resize(img, contrast_setting)

    # only doing this for testing mode.
    img = PIL.Image.fromarray(imgpx)

    finalpx = []

    for ri in range(len(imgpx)):
        if ri % 2 == 1:
            imgpx[ri] = imgpx[ri][::-1]  # flips every 2 rows
        for ci in range(len(imgpx[0])):
            try:
                # colored pixels
                r = imgpx[ri][ci][0]
                g = imgpx[ri][ci][1]
                b = imgpx[ri][ci][2]
            except:
                # only black and white pixels
                r = imgpx[ri][ci]
                g = imgpx[ri][ci]
                b = imgpx[ri][ci]

            # manipulation of all pixels
            r = int(brt * r)
            g = int(brt * g)
            b = int(brt * b)

            night_shift_setting = settings.check("nightshift")
            if (night_shift_setting == None):
                night_shift_setting = 0

            (r,g,b) = nightshift.adjust(r,g,b, 100-int(night_shift_setting))

            # adjust for bad colors on display
            if brt > 0.15:
                r = nonlinearity.compensate(r)
                g = nonlinearity.compensate(g)
                b = nonlinearity.compensate(b)

            finalpx.append((r, g, b))

    return finalpx

# Update the pixels on the screen
def update_pixels(finalpx, transition=True):
    if setLeds:
        if transition:
            animate(pixels[0:256], finalpx)
        else:
            pixels[0:256] = finalpx[0:256]
            pixels.show()
    else:
        img.show()
        return
def configure_brightness():
    lastbrt = brt

    current = get_brightness()
    if abs(current - lastbrt) > 0.01:
        set_brightness(current)

# Main function to be repeatedly run. Gets song, and brings everything together
def main(last_image_url):
    global night_shift_value, img
    song = driver.song()
    imgurl = get_image(song)

    # set brightness automatically
    lastbrt = brt
    last_night_shift_value = night_shift_value
    night_shift_value = settings.check("nightshift")

    current = get_brightness()

    if abs(current - lastbrt) > 0.01:
        set_brightness(current)

    if song.get('type') == "time":
        time_image = clock.now()
        px = get_pixels(image=time_image)
    elif song.get('type') == "gif":
        current_item = song
        frame_number = 0
        while settings.check("idleMode").startswith("gif") and current_item.get('type') == 'gif':
            configure_brightness()
            gif_id = current_item.get('raw')
            frames = fun.get_frames(gif_id)
            for frame in frames:
                frame_image = PIL.Image.fromarray(frame)
                px = get_pixels(image=frame_image)
                update_pixels(px, transition=False if frame_number != 0 else True)
                
                time.sleep(fun.frame_duration)
                frame_number += 1
            current_item = driver.song()
    else:
        px = get_pixels(imgurl)

    if lastbrt != brt or last_night_shift_value != night_shift_value:
        print('brt updated to ' +str(brt))
        update_pixels(px)
    elif ((imgurl == last_image_url) or (imgurl == None)) and (song.get("force") == False):
        # note: this specifies if the image url is the same or not. Meaning, that if two songs are from the same album it won't do anything
        pass
    else:
        print(song.get('name'))
        display_image_url = song.get('fullsize_image_url')
        if not display_image_url.startswith("http"):
            display_image_url = "https://i.ibb.co/KNq0069/Group-30.png"

        settings.put("albumName", song.get('name'))
        settings.put("imageUrl", display_image_url)
        settings.put("artistName", song.get('artist_names'))
        # img.show()
        update_pixels(px)

    return song

steps = 12

# Animates a set of pixels
def animate(oldpixels, newpixels):
    set_step_count()

    stepcount = 0
    while stepcount < steps:
        pix = []
        for l in range(len(oldpixels)):
            temppixel = [0,0,0]
            for j in range(3):
                temppixel[j] = int(calc_pixel(oldpixels[l][j], newpixels[l][j], stepcount, steps))
            pix.append(temppixel)

        for i in range(len(oldpixels)):
            pixels[i] = (pix[i][0], pix[i][1], pix[i][2])
        pixels.show()
        stepcount += 1

    pixels[0:256] = newpixels[0:256]
    pixels.show()
    
# Sets number of frames on the animatoin
def set_step_count():
    global steps
    steps = int(settings.get()['animation'])

# Used for animation. Calculates the pixel color based on a linear function x1 + x((y2-y1) / dx)
def calc_pixel(old, new, stepno, totalsteps):
    p = ((new - old)/totalsteps) * stepno + old
    if p > 255:
        p = 255
    if p < 0:
        p = 0
    return p