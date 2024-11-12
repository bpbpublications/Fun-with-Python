import sounddevice as sd
from scipy.io.wavfile import write

fs = 44100
seconds = 3

myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
print("Start talking")
sd.wait()
print("Write output")

write("output.wav", fs, myrecording)
