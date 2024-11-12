from os import system


class SmartSpeaker:
    def run(self):
        if self.record_audio():
            self.analized_text = self.audio_to_text()
            logging.info(f"Translated text: {self.analized_text}")
            if self.is_keyword_in_text:
                reply_txt = "Hello, I can't talk yet but I heard you"
                system(f"say {reply_txt}")
