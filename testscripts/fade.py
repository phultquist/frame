import time
import board
import neopixel
pixels = neopixel.NeoPixel(board.D12, 256, brightness=0.1)

v = 0
mult = 1
while True:
    if v > 255 or v < 0:
        mult *= -1
    
    # for the life of me, i have no idea why this has to be a loop. i tried pixels = mbdtf and every time it showed funky colors, so here we are
    print(v)
    pixels[0 - 256:0] = (v, v, v)
    
    v += mult * 3

