import spotipy
import spotipy.util as util
from secrets import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, username
import exceptions
import os
import json
import time
import settings
import listen
from datetime import datetime
import random

os.environ["SPOTIPY_CLIENT_ID"] = SPOTIPY_CLIENT_ID
os.environ["SPOTIPY_CLIENT_SECRET"] = SPOTIPY_CLIENT_SECRET

loginUsername = username
# what the program is allowed to modify
scope = 'user-read-private user-read-playback-state user-modify-playback-state'

token = util.prompt_for_user_token(loginUsername, scope, client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri="http://localhost:3000/")

sp = spotipy.Spotify(auth=token)

pause_time = 0
screen_off = False
shutoff_time = 60 # seconds

show_clock = True

def song():
    # print("song called")
    global pause_time
    global screen_off
    global sp

    current_settings = settings.get()
    if current_settings["mode"] == "listen":
        if current_settings["listenTrigger"] == True:
            settings.setTrigger("listenTrigger")
            return listen.recognize()
        else:
            return listen.last()
            # return exceptions.exc_object('off', 'screen off')
    
    try:
        playing = sp.currently_playing()
    except spotipy.client.SpotifyException:
        # re-authenticate when token expires
        token = util.prompt_for_user_token(loginUsername, scope, client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri="http://localhost:3000/")
        print("New Spotify Token")
        sp = spotipy.Spotify(auth=token)
        try:
            playing = sp.currently_playing()
        except:
            return exceptions.exc_object('error', 'spotify api error')
            print("unable to get current song")

    clock_setting = settings.check("showClock")
    # print(clock_setting)

    if clock_setting == "true":
        show_clock = True
    else:
        show_clock = False
    
    if (playing == None) or (not (playing.get('is_playing'))):
        if not show_clock:
            if pause_time == 0:
                pause_time = time.time()
            if (time.time() - pause_time) > shutoff_time:
                if not screen_off:
                    print('Shutting off...')
                screen_off = True
                return exceptions.exc_object('off', 'screen off')
        else:
            return exceptions.exc_object('time', datetime.now().strftime("%H%M")+settings.check("clock")+settings.check("clockColor"))

        return exceptions.exc_object('paused', json.dumps(playing))
    else: 
        screen_off = False
        pause_time = 0

    try:
        images_returned = playing.get("item").get("album").get("images")
        image_url = (images_returned[len(images_returned) - 1].get('url'))
    except:
        return exceptions.exc_object('error', json.dumps(playing))

    artists = playing.get("item").get("album").get('artists')
    name = playing.get("item").get('name')
    artist_names = ""

    for i in range(len(artists)):
        artist_names += artists[i].get('name')
        if not (i == len(artists) - 1):
            artist_names += ', '

    return {
        "image_url": image_url,
        "name": name,
        "artist_names": artist_names,
        "fullsize_image_url": images_returned[0].get('url'),
        "raw": "spotify",
        # "raw": json.dumps(playing),
        "ready": True,
        "playing": True,
        "force": False,
        "exception": False,
        "type": "song"
    }
