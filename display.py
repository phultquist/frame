import time
import board
import neopixel

n = 150
b = 0

seconds = 0

pixels = neopixel.NeoPixel(board.D18, n)

pixels.fill((255, 255, 255))
