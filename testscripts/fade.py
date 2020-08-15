import time
import board
import neopixel
pixels = neopixel.NeoPixel(board.D12, 256, brightness=0.1)

v = 0
mult = 1
while True:
    if v > 255 or v < 0:
        mult *= -1

    pixels.fill((v, v, v))
    v += mult * 1
    time.sleep(0.05)

