import sounddevice as sd
from scipy.io.wavfile import write

fs = 44100
seconds = 10

print("I am listening... press ctrl+c to stop")
while True:
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
    sd.wait()
    print("Finished and again, recordign size", len(myrecording))
