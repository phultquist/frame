import time
import board
import neopixel
pixels = neopixel.NeoPixel(board.D12, 256, brightness=0.1, auto_write=True)

v = 0
while True:
    if v > 15:
        v = 0
    # for the life of me, i have no idea why this has to be a loop. i tried pixels = mbdtf and every time it showed funky colors, so here we are
    pixels[v] = (200, 200, 200)
    v += 1

