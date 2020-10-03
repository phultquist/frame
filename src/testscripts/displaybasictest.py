import board
import neopixel
pixels = neopixel.NeoPixel(board.D12, 256)

j = 0
step = 256

# for the life of me, i have no idea why this has to be a loop. i tried pixels = mbdtf and every time it showed funky colors, so here we are
while j < len(pixels) + 1:
    pixels[j - step:j] = (255,255,255)
    j += step