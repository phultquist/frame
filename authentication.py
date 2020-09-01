# import spotify
# print(spotify.song())

import spotipy
import os
from spotipy.oauth2 import SpotifyOAuth
from secrets import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, username
import ip

print(ip.ip)

scope = 'user-read-private user-read-playback-state user-modify-playback-state'

os.environ["SPOTIPY_CLIENT_ID"] = SPOTIPY_CLIENT_ID
os.environ["SPOTIPY_CLIENT_SECRET"] = SPOTIPY_CLIENT_SECRET

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri="http://"+str(ip.ip)+":3000/",
                                               scope=scope,
                                               username=username,
                                               show_dialog=True,
                                               cache_path=None))

results = sp.currently_playing()
print(results)