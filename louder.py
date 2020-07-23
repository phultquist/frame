from pydub import AudioSegment
from pydub.playback import play

song = AudioSegment.from_mp3("output.mp3")

# boost volume by 6dB
louder_song = song + 6

# reduce volume by 3dB
quieter_song = song - 3

#Play song
play(louder_song)

#save louder song 
louder_song.export("output_loud.mp3", format='mp3')