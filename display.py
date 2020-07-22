import time
import board
import neopixel
from cover import finalpx

pixels = neopixel.NeoPixel(board.D18, 256, brightness = 0.1)

j = 0
step = 256

# for the life of me, i have no idea why this has to be a loop. i tried pixels = mbdtf and every time it showed funky colors, so here we are
while j < len(pixels) + 1:
    pixels[j - step:j] = finalpx[j - step:j]
    j += step