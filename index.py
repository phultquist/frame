import requests
import PIL.Image
from io import BytesIO
import numpy as np
import spotify
import sys
import exceptions
import numbers
import nonlinearity


def get_argument(index):
    try:
        a = sys.argv[index]
        return a
    except:
        return None

max_brightness = 0.60
min_brightness = 0.07
brt = 0.07

if get_argument(1) != None and get_argument(1) != "test" and get_argument(1) != 'auto':
    brt = int(get_argument(1)) / (max_brightness * 100)

if get_argument(1) == 'auto':
    import light
    import math
    brt = math.sqrt(light.lux()) / 18
    print('Set brightness automatically to '+str(brt))

if get_argument(2) == 'noserver':
    run_server = False
else:
    run_server = True

# print(brt)
if brt > max_brightness:
    brt = 1

if brt < min_brightness:
    brt = min_brightness

img = None

# if the LED strip is not on you, that is okay, make sure this is set to false; or, use the runtime variable "test"
setLeds = True

if get_argument(1) == 'test':
    setLeds = False

if setLeds:
    # import lux
    # lux.light
    import board
    import neopixel
    pixels = neopixel.NeoPixel(board.D12, 256, brightness=brt, auto_write=False)


def get_image(song):
    try:
        imgurl = song.get('image_url')
    except:
        print('### error 1 ###')
        imgurl = exceptions.ERROR_IMAGE  # error 1

    return imgurl


################################
### Get Image and Manipulate ###
################################

def manipulate(imgurl):
    global img
    imgcontent = imgurl
    if imgurl.startswith('http'):
        imgresp = requests.get(imgurl)
        imgcontent = BytesIO(imgresp.content)

    img = PIL.Image.open(imgcontent)
    img = img.resize((16, 16))

    imgpx = np.array(img)
    finalpx = []

    for ri in range(len(imgpx)):
        if ri % 2 == 1:
            imgpx[ri] = imgpx[ri][::-1]  # flips every 2 rows
        for ci in range(len(imgpx[0])):
            try:
                r = imgpx[ri][ci][0]
                g = imgpx[ri][ci][1]
                b = imgpx[ri][ci][2]
            except:
                r = imgpx[ri][ci]
                g = imgpx[ri][ci]
                b = imgpx[ri][ci]

            if brt > 0.15:
                r = nonlinearity.compensate(r)
                g = nonlinearity.compensate(g)
                b = nonlinearity.compensate(b)

            finalpx.append((r, g, b))

    return finalpx

#####################
### Update Pixels ###
#####################


def update_pixels(finalpx):
    if setLeds:
        j = 0
        step = 256

        # for the life of me, i have no idea why this has to be a loop. i tried pixels = mbdtf and every time it showed funky colors, so here we are
        animate(pixels[0:256], finalpx)
        # pixels[0:256] = finalpx[0:256]
        # while j < len(pixels) + 1:
        #     pixels[j - step:j] = finalpx[j - step:j]
        #     j += step
    else:
        # img.show()
        return


def main(last_image_url):
    song = spotify.song()
    imgurl = get_image(song)
    if (imgurl == last_image_url) or (imgurl == None):
        # note: this specifies if the image url is the same or not. Meaning, that if two songs are from the same album it won't do anything; it won't print the song name or anything.
        pass
    else:
        print(song.get('name'))
        px = manipulate(imgurl)
        update_pixels(px)

    return song

stepcount = 0
steps = 28

def animate(oldpixels, newpixels):
    global stepcount
    pix = []
    while stepcount < steps:
        for l in range(len(oldpixels)):
            pi = [0,0,0]
            for j in range(3):
                pi[j] = int(calc_pixel(oldpixels[l][j], newpixels[l][j], stepcount))
            pi = tuple(pi)
            pix.append(pi)
        print(pix[0])
        pixels[0:256] = pix[0:256]
        pixels.show()
        stepcount += 1

    pixels[0:256] = newpixels[0:256]
    pixels.show()
    
    
def calc_pixel(old, new, stepno):
    p = ((new - old)/steps) * stepno + old
    if p > 255:
        p = 255
    if p < 0:
        p = 0
    return p
    
