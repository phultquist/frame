import time
import board
import neopixel
from random import randrange

pixels = neopixel.NeoPixel(board.D12, 256, brightness=0.1, auto_write=False)

mult = 1
color = [0, 255, 0]
oldpixels = []
newpixels = []
for k in range(256):
    oldpixels.append([randrange(256), randrange(256), randrange(256)])
newcolor= [255, 0, 0]
for k in range(len(oldpixels)):
    newpixels.append([randrange(256), randrange(256), randrange(256)])
steps = 28
stepcount = 0

def calc_pixel(old, new, stepno):
    p = ((new - old)/steps) * stepno + old
    if p > 255:
        p = 255
    if p < 0:
        p = 0
    return p
    

while True:
    if stepcount >= steps:
        # stepcount = 0
        mult *= -1
    if stepcount <= 0:
        mult *= -1
    # for the life of me, i have no idea why this has to be a loop. i tried pixels = mbdtf and every time it showed funky colors, so here we are
    updatedpixels = []
    for l in range(len(oldpixels)):
        pi = [0,0,0]
        for j in range(3):
            pi[j] = int(calc_pixel(oldpixels[l][j], newpixels[l][j], stepcount))
        updatedpixels.append(pi)

    for i in range(len(oldpixels)):
        pixels[i] = (updatedpixels[i][0], updatedpixels[i][1], updatedpixels[i][2])
    pixels.show()
    
    stepcount += 1*mult
