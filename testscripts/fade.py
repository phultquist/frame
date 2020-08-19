import time
import board
import neopixel
pixels = neopixel.NeoPixel(board.D12, 256, brightness=0.1, auto_write=False)

v = 200
mult = 1
color = [0, 0, 0]
newcolor= [255, 0, 0]
steps = 28
stepcount = 0

while True:
    if stepcount > steps:
        stepcount = 0
    
    # for the life of me, i have no idea why this has to be a loop. i tried pixels = mbdtf and every time it showed funky colors, so here we are
    updated = [0,0,0]
    for j in range(3):
        updated[j] = calc_pixel(color[j], newcolor[j], stepcount)

    for i in range(256):
        pixels[i] = (updated[0], updated[1], updated[2])
    pixels.show()
    
    stepcount += 1

def calc_pixel(old, new, stepno):
    p = ((new - old)/steps) * stepno + old
    if p > 255:
        p = 255
    if p < 0:
        p = 0
    return p
    