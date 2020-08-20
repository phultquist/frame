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
    
def set_brightness():
    global brt
    brt = math.sqrt(light.lux()) / 18
    print('Set brightness automatically to '+str(brt))

max_brightness = 0.60
min_brightness = 0.07
brt = 0.07

if get_argument(1) != None and get_argument(1) != "test" and get_argument(1) != 'auto':
    brt = int(get_argument(1)) / (max_brightness * 100)

if get_argument(1) == 'auto':
    import light
    import math
    set_brightness()

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
    pixels = neopixel.NeoPixel(board.D12, 256, auto_write=False)


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

            finalpx.append((int(brt * r), int(brt * g), int(brt * b)))

    return finalpx

#####################
### Update Pixels ###
#####################


def update_pixels(finalpx):
    if setLeds:
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
    set_brightness()
    if (imgurl == last_image_url) or (imgurl == None):
        # note: this specifies if the image url is the same or not. Meaning, that if two songs are from the same album it won't do anything; it won't print the song name or anything.
        pass
    else:
        print(song.get('name'))
        px = manipulate(imgurl)
        update_pixels(px)

    return song

steps = 14

def animate(oldpixels, newpixels):
    # global pixels
    stepcount = 0
    while stepcount < steps:
        pix = []
        for l in range(len(oldpixels)):
            temppixel = [0,0,0]
            for j in range(3):
                temppixel[j] = int(calc_pixel(oldpixels[l][j], newpixels[l][j], stepcount))
            pix.append(temppixel)


        for i in range(len(oldpixels)):
            pixels[i] = (pix[i][0], pix[i][1], pix[i][2])
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
    
