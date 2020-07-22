import json
import requests
import base64
import sounddevice as sd
from scipy.io.wavfile import write
from PIL import ImageFile


### record audio ###

duration = 3  # seconds
fs = 44100

recorded = sd.rec(int(duration * fs), samplerate=fs, channels=1)
sd.wait()

write('output.mp3', fs, recorded)  # Save as WAV file 



### get image url ###

image_file= open('./output.mp3',"rb")
image_data_binary = image_file.read()
image_data = (base64.b64encode(image_data_binary))

print('recording done')

data = {
    'return': 'spotify',
    'api_token': '0295a1c0139a030849dd81359d92122a',
    'audio': image_data
}

result = requests.post('https://api.audd.io/', data=data)

response = json.loads(result.text)
print(response['result']['title'])
print(response['result']['artist'])
imgurl = response['result']['spotify']['album']['images'][0]['url']



### get resize image ###