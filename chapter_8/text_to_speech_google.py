from gtts import gTTS
import os
import playsound


def text2speak(text):
    tts = gTTS(text=text, lang="en")
    filename = "tmp.mp3"
    tts.save(filename)
    playsound.playsound(filename)
    os.remove(filename)


text2speak("Hello there, nice to meet you!")
