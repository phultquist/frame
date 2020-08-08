import spotipy
import spotipy.util as util
from secrets import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, username
import exceptions
import os
import json

os.environ["SPOTIPY_CLIENT_ID"] = SPOTIPY_CLIENT_ID
os.environ["SPOTIPY_CLIENT_SECRET"] = SPOTIPY_CLIENT_SECRET

loginUsername = username
# what the program is allowed to modify
scope = 'user-read-private user-read-playback-state user-modify-playback-state'

birdy_uri = 'spotify:artist:2WX2uTcsvV5OnS0inACecP'
token = util.prompt_for_user_token(loginUsername,
                                   scope,
                                   client_id=SPOTIPY_CLIENT_ID,
                                   client_secret=SPOTIPY_CLIENT_SECRET,
                                   redirect_uri="http://localhost:3000/")

sp = spotipy.Spotify(auth=token)


def song():
    playing = sp.currently_playing()
    if (playing == None) or (not (playing.get('is_playing'))):
        return exceptions.exc_object(False, json.dumps(playing))

    try:
        images_returned = playing.get("item").get("album").get("images")
        image_url = (images_returned[len(images_returned) - 1].get('url'))
    except:
        return exceptions.exc_object(False, json.dumps(playing))

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
        "raw": json.dumps(playing),
        "ready": True,
        "playing": True
    }
