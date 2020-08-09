import json
import requests
import base64
import sounddevice as sd
from scipy.io.wavfile import write
import PIL.Image
from io import BytesIO
import numpy as np
from datetime import datetime

startTime = datetime.now()
brt = 0.07

# if the LED strip is not on you, that is okay, make sure this is set to false
setLeds=True

if setLeds:
    import board
    import neopixel


####################
### Record Audio ###
####################

duration = 6  # seconds
fs = 44100

print('Recording...')
recorded = sd.rec(int(duration * fs), samplerate=fs, channels=1)
sd.wait()

write('output.mp3', fs, recorded)  # Save as WAV file 

print('Done Recording')

#####################
### Get Image URL ###
#####################

sound_file= open('./output.mp3',"rb")
sound_data_binary = sound_file.read()
sound_data = (base64.b64encode(sound_data_binary))

api_token_file = open('key', 'r')

data = {
    'return': 'spotify',
    'api_token': api_token_file.read().split("\n")[0],
    'audio': sound_data
}

result = requests.post('https://api.audd.io/', data=data)

response = json.loads(result.text)

try:
    print(response['result']['title'])
    print(response['result']['artist'])
    imgurl = response['result']['spotify']['album']['images'][2]['url']
except:
    print('### error 1 ###')
    print(response)
    imgurl = 'https://i.ibb.co/Q85tMW2/e1.png' # error 1


################################
### Get Image and Manipulate ###
################################

imgresp = requests.get(imgurl)
img = PIL.Image.open(BytesIO(imgresp.content))

img = img.resize((16, 16))

if not setLeds:
    pass
    # img.show()

imgpx = np.array(img)
finalpx = []
for ri in range(len(imgpx)):
    if ri % 2 == 1:
        imgpx[ri] = imgpx[ri][::-1]  # flips every 2 rows
    for ci in range(len(imgpx[0])):
        finalpx.append((imgpx[ri][ci][0], imgpx[ri][ci][1], imgpx[ri][ci][2]))


print('Total Time: ' + str(datetime.now() - startTime))

#####################
### Update Pixels ###
#####################

if setLeds:
    pixels = neopixel.NeoPixel(board.D12, 256, brightness = brt)

    j = 0
    step = 256

    # for the life of me, i have no idea why this has to be a loop. i tried pixels = mbdtf and every time it showed funky colors, so here we are
    while j < len(pixels) + 1:
        pixels[j - step:j] = finalpx[j - step:j]
        j += step
