import os
import playsound
from gtts import gTTS
from tempfile import mkstemp


def text2speak(text):
    tts = gTTS(text=text, lang="en")
    filename = mkstemp()[1]
    tts.save(filename)
    playsound.playsound(filename)
    os.remove(filename)


text2speak("Hello there, nice to meet you!")
