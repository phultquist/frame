import time
import board
import neopixel
pixels = neopixel.NeoPixel(board.D12, 256, brightness=0.1, auto_write=False)

v = 200
mult = 1
while True:
    if v > 255 or v < 0:
        if v > 255:
            v = 255
        else:
            v = 0
        mult *= -1
    
    # for the life of me, i have no idea why this has to be a loop. i tried pixels = mbdtf and every time it showed funky colors, so here we are
    for i in range(256):
        pixels[i] = (v, v, v)
    pixels.show()
    
    v += mult * 9

