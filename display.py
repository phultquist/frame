import time
import board
import neopixel
from mbdtf import *

n = 150
b = 0

seconds = 0

pixels = neopixel.NeoPixel(board.D18, 256)

pixels.fill((0,0,255))

# for i in range(len(mbdtf)):
#     pixels[i] = mbdtf[i]
