# drives the program, finds what to put on the screen

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
    if current_settings["asleep"] == "true" or current_settings["asleep"] == True:
        settings.put("albumName", "Frame is Asleep")
        settings.put("imageUrl", "https://i.ibb.co/2d9xQNk/Group-31.png")
        return exceptions.exc_object('off', 'screen off')

    if current_settings["mode"] == "listen":
        if current_settings["listenTrigger"] == True or current_settings["listenTrigger"] == "true":
            settings.setTrigger("listenTrigger")
            return listen.recognize()
        else:
            return listen.last()
            # return exceptions.exc_object('off', 'screen off')
    listen.reset_last_successful_song()

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

    idle_setting = settings.check("idleMode") # can be clock, gif:[gif_id], off, false (off means the same thing as false)

    if idle_setting == "off":
        idle_setting = "false"
    
    if (playing == None) or (not (playing.get('is_playing'))):
        if idle_setting == "false":
            # no clock, no gif
            if pause_time == 0:
                pause_time = time.time()
            if (time.time() - pause_time) > shutoff_time:
                if not screen_off:
                    print('Shutting off...')
                screen_off = True
                return exceptions.exc_object('off', 'screen off')
        elif idle_setting == "clock":
            # a composite index, that way if anything changes the clock updates :)
            return exceptions.exc_object('time', datetime.now().strftime("%H%M")+settings.check("clock")+settings.check("clockColor")+settings.check("clockTiming"))
        elif idle_setting.startswith("gif"):
            try:
                gif_id = idle_setting.split(':')[1] # format is gif:[gif_id]
                return exceptions.exc_object('gif', gif_id)
            except Exception as e:
                print(e)
                return exceptions.exc_object('error', "error with gif: "+idle_setting)

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
        "ready": True,
        "playing": True,
        "force": False,
        "exception": False,
        "type": "song"
    }
