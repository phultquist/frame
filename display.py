import time
import board
import neopixel
from mbdtf import *

seconds = 0

pixels = neopixel.NeoPixel(board.D18, 256)

pixels = mbdtf

# pixels.fill((238, 37, 65))

for i in range(len(mbdtf)):
    pixels[i] = mbdtf[i]
