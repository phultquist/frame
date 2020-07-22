import PIL.Image
import numpy as np
import requests
from io import BytesIO
import sys

'''
path = 'docs/graduation.png'
if len(sys.argv) > 1:
    path = 'docs/'+sys.argv[1]+'.png'

img = PIL.Image.open(path)
'''

url = 'https://i.scdn.co/image/ab67616d0000b2730cd942c1a864afa4e92d04f2'

response = requests.get(url)
img = PIL.Image.open(BytesIO(response.content))


img = img.resize((16, 16))
img.show()
imgpx = np.array(img)
finalpx = []
for ri in range(len(imgpx)):
    if ri % 2 == 1:
        imgpx[ri] = imgpx[ri][::-1]  # flips every 2 rows
    for ci in range(len(imgpx[0])):
        finalpx.append((imgpx[ri][ci][0], imgpx[ri][ci][1], imgpx[ri][ci][2]))