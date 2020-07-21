import time
import board
import neopixel
from mbdtf import *

seconds = 0

pixels = neopixel.NeoPixel(board.D18, 256)

# pixels = mbdtf

# pixels.fill((238, 37, 65))

j = 0
step = 2
while j < len(pixels):
    pixels[j - step:j] = mbdtf[j - step:j]

# for i in range(len(mbdtf)):
#     pixels[i] = mbdtf[i]
