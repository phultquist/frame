import spotify
print(spotify.song())

import spotipy
import os
from spotipy.oauth2 import SpotifyOAuth
from secrets import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, username

os.environ["SPOTIPY_CLIENT_ID"] = SPOTIPY_CLIENT_ID
os.environ["SPOTIPY_CLIENT_SECRET"] = SPOTIPY_CLIENT_SECRET

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri="http://192.168.68.117:3000/",
                                               scope="user-library-read",
                                               username="jdiaalhsw8zdhpcdv391bj5we",
                                               show_dialog=True,
                                               cache_path=None))

results = sp.current_user_saved_tracks()
for idx, item in enumerate(results['items']):
    track = item['track']
    print(idx, track['artists'][0]['name'], " – ", track['name'])

# import spotipy
# from spotipy.oauth2 import SpotifyClientCredentials
# import os
# from secrets import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, username

# os.environ["SPOTIPY_CLIENT_ID"] = SPOTIPY_CLIENT_ID
# os.environ["SPOTIPY_CLIENT_SECRET"] = SPOTIPY_CLIENT_SECRET

# auth_manager = SpotifyClientCredentials()
# sp = spotipy.Spotify(auth_manager=auth_manager)

# playlists = sp.user_playlists('spotify')
# while playlists:
#     for i, playlist in enumerate(playlists['items']):
#         print("%4d %s %s" % (i + 1 + playlists['offset'], playlist['uri'],  playlist['name']))
#     if playlists['next']:
#         playlists = sp.next(playlists)
#     else:
#         playlists = None

# print(sp.currently_playing())