# import spotify
# print(spotify.song())

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from secrets import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, username

os.environ["SPOTIPY_CLIENT_ID"] = SPOTIPY_CLIENT_ID
os.environ["SPOTIPY_CLIENT_SECRET"] = SPOTIPY_CLIENT_SECRET

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri="http://localhost:3000/",
                                               scope="user-library-read",
                                               username="jdiaalhsw8zdhpcdv391bj5we"))

results = sp.current_user_saved_tracks()
for idx, item in enumerate(results['items']):
    track = item['track']
    print(idx, track['artists'][0]['name'], " – ", track['name'])