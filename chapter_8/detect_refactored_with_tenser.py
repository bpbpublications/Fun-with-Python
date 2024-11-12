import logging
import random
import whisper
import sounddevice as sd
from datetime import datetime
from os import system
from scipy.io.wavfile import write
from neuralintents import GenericAssistant

FS = 44100
SECONDS = 5
RECORDING_FILE = "output.wav"
LOGGING_FORMAT = "%(asctime)s %(message)s"

logging.basicConfig(level=logging.INFO, format=LOGGING_FORMAT)


class SmartSpeaker:
    def __init__(self):
        self._current_text = None
        self.model = whisper.load_model("base.en", download_root=".")
        logging.info("Model loaded")

    def audio2text(self):
        if self.record_audio():
            self.analized_text = self.audio_to_text()
            logging.info(f"Translated text: {self.analized_text}")
            return self.analized_text

    def run(self, assistant):
        self.assistant = assistant
        analyzed_text = self.audio2text()
        if analyzed_text and self.is_keyword_in_text:
            self.__say("Yes, how can I help you?")
            new_analyzed_text = self.audio2text()
            if new_analyzed_text:
                self.assistant.request(new_analyzed_text)

    def record_audio(self) -> bool:
        try:
            myrecording = sd.rec(int(SECONDS * FS), samplerate=FS, channels=1)
            logging.info("Start talking")
            sd.wait()

            logging.info("Write output")
            write("output.wav", FS, myrecording)
        except Exception as e:
            logging.error(f"We crashed: {e}")
            return False
        return True

    def audio_to_text(self) -> str:
        logging.info("Analyze text")
        result = self.model.transcribe("output.wav")
        return result["text"]

    def get_response(self, tag):
        list_of_intents = self.assistant.intents["intents"]
        for i in list_of_intents:
            if i["tag"] == tag:
                return random.choice(i["responses"])

    def __say(self, message):
        system(f"say {message}")

    @property
    def is_keyword_in_text(self) -> bool:
        return "speaker" in self.analized_text.lower() or "hey speaker" in self.analized_text.lower()

    def callback_greetings(self):
        response = self.get_response("greetings")
        self.__say(response)

    def callback_time(self):
        current_time = datetime.now().strftime("%I:%M%p")
        response = self.get_response("time")
        response = response.format(time=current_time)
        self.__say(response)


if __name__ == "__main__":
    smart_speaker = SmartSpeaker()
    mappings = {"greetings": smart_speaker.callback_greetings, "time": smart_speaker.callback_time}

    assistant = GenericAssistant("intents_speaker.json", model_name="test_model", intent_methods=mappings)
    assistant.train_model()
    assistant.save_model()
    smart_speaker.run(assistant)
