steps = 28
stepcount = 0

def animate(oldpixels, newpixels, frame):
    global stepcount
    pix = []

    

    frame += 1
    return pix

def calc_pixel(old, new, stepno):
    p = ((new - old)/steps) * stepno + old
    if p > 255:
        p = 255
    if p < 0:
        p = 0
    return p
    