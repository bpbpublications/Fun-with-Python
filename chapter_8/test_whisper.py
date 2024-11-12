import whisper
import sounddevice as sd
from scipy.io.wavfile import write

fs = 44100
seconds = 5

myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
print("Start talking")
sd.wait()

print("Write output")
write("output.wav", fs, myrecording)

print("Analyze text")

model = whisper.load_model("base")
result = model.transcribe("output.wav")
analized_text = result["text"]

print(f"What you said: {analized_text}")
