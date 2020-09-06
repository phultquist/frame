def update_pixels(finalpx):
    if setLeds:
        pixels = neopixel.NeoPixel(board.D18, 256, brightness = brt)

        j = 0
        step = 256

        # for the life of me, i have no idea why this has to be a loop. i tried pixels = mbdtf and every time it showed funky colors, so here we are
        while j < len(pixels) + 1:
            pixels[j - step:j] = finalpx[j - step:j]
            j += step
    else:
        img.show()