import sounddevice as sd
from scipy.io.wavfile import write
duration = 7  # seconds
fs = 44100


recorded = sd.rec(int(duration * fs), samplerate=fs, channels=1)
sd.wait()
print(recorded)
write('output.wav', fs, recorded)  # Save as WAV file 