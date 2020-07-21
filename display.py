import time
import board
import neopixel
from mbdtf import *

seconds = 0

pixels = neopixel.NeoPixel(board.D18, 256, brightness = 0.05)

# pixels = mbdtf

# pixels.fill((238, 37, 65))

j = 0
step = 256
while j < len(pixels) + 1:
    pixels[j - step:j] = mbdtf[j - step:j]
    j += step

# for i in range(len(mbdtf)):
#     pixels[i] = mbdtf[i]
