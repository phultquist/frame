import json
import requests
import base64
import sounddevice as sd
from scipy.io.wavfile import write
import PIL.Image
from io import BytesIO
import numpy as np
import spotify
import time
import sys
import exceptions

def get_argument(index):
    try:
        a = sys.argv[index]
        return a
    except:
        return False
        
brt = 0.07

if get_argument(1) != False and type(get_argument(1)) is int:
    brt = int(sys.argv[1]) / 100

if get_argument(2) == 'noserver':
    run_server = False
else:
    run_server = True

# print(brt)
if brt > 1:
    brt = 1

if brt < 0:
    brt = 0

img = None

# if the LED strip is not on you, that is okay, make sure this is set to false
setLeds=True

if get_argument(1) == 'test':
    setLeds = False

if setLeds:
    import board
    import neopixel
    pixels = neopixel.NeoPixel(board.D18, 256, brightness = brt)

def get_image(song):
    try:
        imgurl = song.get('image_url')
    except:
        print('### error 1 ###')
        imgurl = exceptions.ERROR_IMAGE # error 1

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

time_since_pause = 0

def main(last_image_url):
    global time_since_pause

    song = spotify.song()
    imgurl = get_image(song)
    if (imgurl == last_image_url) or (imgurl == None):
        pass
    else:
        print(song.get('name'))
        px = manipulate(imgurl)
        update_pixels(px)
    
    if (song.get('playing') == False) and (time_since_pause == 0):
        time_since_pause = time.time()
    elif (song.get('playing') == False) and not (time_since_pause == 0):
        if (time.time() - time_since_pause > 5): #fifteen seconds till shutoff
            #don't play
            print("time to shut off")
            return False
            pass
    else:
        time_since_pause = 0

    return song