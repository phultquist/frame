import json
import requests
import base64
import sounddevice as sd
from scipy.io.wavfile import write
import PIL.Image
from io import BytesIO
import numpy as np
from datetime import datetime
import spotify
import time
import sys

startTime = datetime.now()

try:
    brt = int(sys.argv[1]) / 100
except:
    brt = 0.07

# print(brt)

img = None

# if the LED strip is not on you, that is okay, make sure this is set to false
setLeds=True

if setLeds:
    import board
    import neopixel
    time.sleep(1)
    pixels = neopixel.NeoPixel(board.D18, 256, brightness = brt)

def get_image():
    try:
        imgurl = spotify.song()
    except:
        print('### error 1 ###')
        imgurl = 'https://i.ibb.co/Q85tMW2/e1.png' # error 1

    return imgurl


################################
### Get Image and Manipulate ###
################################

def manipulate(imgurl):
    imgresp = requests.get(imgurl)
    global img
    img = PIL.Image.open(BytesIO(imgresp.content))

    img = img.resize((16, 16))

    imgpx = np.array(img)
    finalpx = []
    for ri in range(len(imgpx)):
        if ri % 2 == 1:
            imgpx[ri] = imgpx[ri][::-1]  # flips every 2 rows
        for ci in range(len(imgpx[0])):
            # print(imgpx)
            try:
                r = imgpx[ri][ci][0]
                g = imgpx[ri][ci][1]
                b = imgpx[ri][ci][2]
            except:
                r = imgpx[ri][ci]
                g = imgpx[ri][ci]
                b = imgpx[ri][ci]
            # print(imgpx[ri][ci][1])
            # print(imgpx[ri][ci][2])
            finalpx.append((r, g, b))
        # print('something is wrong with the image with url ' + imgurl)

    return finalpx

#####################
### Update Pixels ###
#####################

def update_pixels(finalpx):
    if setLeds:
        j = 0
        step = 256

        # for the life of me, i have no idea why this has to be a loop. i tried pixels = mbdtf and every time it showed funky colors, so here we are
        while j < len(pixels) + 1:
            pixels[j - step:j] = finalpx[j - step:j]
            j += step
    else:
        # img.show()
        return

def main(last_image_url):
    imgurl = get_image()
    if (imgurl == last_image_url) or (imgurl == None):
        pass
    else:
        px = manipulate(imgurl)
        update_pixels(px)
    return imgurl