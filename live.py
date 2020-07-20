import sounddevice as sd
from scipy.io.wavfile import write

fs = 44100  # Sample rate
seconds = 5  # Duration of recording

audio = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
sd.wait() 
write('recorded.wav', fs, audio) 