import logging
import whisper
import sounddevice as sd
from scipy.io.wavfile import write

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

    def run(self):
        if self.record_audio():
            self.analized_text = self.audio_to_text()
            logging.info(f"Translated text: {self.analized_text}")
            if self.is_keyword_in_text:
                logging.info("Hello, I can't talk yet but I heard you")

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

    @property
    def is_keyword_in_text(self) -> bool:
        return "speaker" in self.analized_text.lower() or "hey speaker" in self.analized_text.lower()


if __name__ == "__main__":
    smart_speaker = SmartSpeaker()
    smart_speaker.run()
