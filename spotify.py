import spotipy
import spotipy.util as util
import json
from secrets import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET

import os

os.environ["SPOTIPY_CLIENT_ID"] = SPOTIPY_CLIENT_ID
os.environ["SPOTIPY_CLIENT_SECRET"] = SPOTIPY_CLIENT_SECRET

loginUsername = "jdiaalhsw8zdhpcdv391bj5we"
scope = 'user-read-private user-read-playback-state user-modify-playback-state'  # what the program is allowed to modify

birdy_uri = 'spotify:artist:2WX2uTcsvV5OnS0inACecP'
token = util.prompt_for_user_token(loginUsername,
                            scope, 
                            client_id=SPOTIPY_CLIENT_ID, 
                            client_secret=SPOTIPY_CLIENT_SECRET,
                            redirect_uri="http://localhost:3000/")

sp = spotipy.Spotify(auth=token)


def song():
    playing = sp.currently_playing()

    image_url = (playing.get("item").get("album").get("images")[2].get('url'))
    name = playing.get("item").get("name")
    return image_url
# spotify.currently_playing()
# results = spotify.artist_albums(birdy_uri, album_type='album')
# albums = results['items']
# while results['next']:
#     results = spotify.next(results)
#     albums.extend(results['items'])

# for album in albums:
#     print(album['name'])