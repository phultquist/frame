import board
import neopixel
pixels = neopixel.NeoPixel(board.D12, 30)

pixels[0] = (255, 0, 0)
