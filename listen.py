import json
import requests
import base64
import sounddevice as sd
from scipy.io.wavfile import write
from io import BytesIO

duration = 6  # seconds
fs = 44100

recorded_file_name = "output.mp3"

# records song and saves to file. easier to save then open, and it overall doesn't take too long.
def record():
    print('Recording...')
    recorded = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()

    write(recorded_file_name, fs, recorded) 

    print('Done Recording')

# recognize the current song playing. also records
def recognize():
    record()
    sound_file = open('./'+recorded_file_name,"rb")
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
        # print(response['result']['artist'])
        imgurl = response['result']['spotify']['album']['images'][0]['url']
    except:
        print('### error 1 ###')
        # print(response)
        imgurl = 'https://i.ibb.co/Q85tMW2/e1.png' # error 1

    print(imgurl)
    return imgurl

recognize()