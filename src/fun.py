# for when the Frame is idle
import time
from PIL import Image, ImageSequence
import numpy as np

frame_duration = 0.1

# Display individual frames from the loaded animated GIF file
def get_frames(gif_id):
    img = Image.open("./assets/gifs/"+gif_id+".gif")
    frames = np.array([np.array(frame.copy().convert('RGB').getdata(),dtype=np.uint8).reshape(frame.size[1],frame.size[0],3) for frame in ImageSequence.Iterator(img)])

    return frames