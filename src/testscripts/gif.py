import numpy as np
from PIL import Image, ImageSequence

img = Image.open('../assets/gifs/brick.gif')
frames = np.array([np.array(frame.copy().convert('RGB').getdata(),dtype=np.uint8).reshape(frame.size[1],frame.size[0],3) for frame in ImageSequence.Iterator(img)])

first = Image.fromarray(frames[0])
first.show()
print(frames[0])