import json
import requests
import base64
import sounddevice as sd
from scipy.io.wavfile import write
from io import BytesIO
from secrets import AUDD_API_KEY
import exceptions

duration = 6  # seconds
fs = 44100

last_successful_song = exceptions.exc_object("off", "screen off")
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
    global last_successful_song
    record()
    sound_file = open('./'+recorded_file_name,"rb")
    sound_data_binary = sound_file.read()
    sound_data = (base64.b64encode(sound_data_binary))

    data = {
        'return': 'spotify',
        'api_token': AUDD_API_KEY,
        'audio': sound_data
    }

    result = requests.post('https://api.audd.io/', data=data)

    response = json.loads(result.text)
    # print(response)
    name = 'null'
    artist = 'null'
    try:
        name = response['result']['title']
        artist = response['result']['artist']
        # print(name + " - " + artist)
        # print(response['result']['artist'])
        imgurl = response['result']['spotify']['album']['images'][0]['url']
    except:
        # print(response)
        return exceptions.exc_object('off', 'screen off')

    # print(imgurl)
    full_object = {
        "image_url": imgurl,
        "name": name,
        "artist_names": artist,
        "fullsize_image_url": imgurl,
        "raw": "listening",
        # "raw": json.dumps(response),
        "ready": True,
        "playing": True,
        "force": False,
        "exception": False,
        "type": "song"
    }
    last_successful_song = full_object
    return full_object

def last():
    return last_successful_song