import logging
from neuralintents import GenericAssistant

LOGGING_FORMAT = "%(asctime)s %(message)s"
logging.basicConfig(level=logging.INFO, format=LOGGING_FORMAT)


def greetings_callback():
    logging.info("Your greetings")


def stocks_callback():
    logging.info("Your stocks")


mappings = {"greeting": greetings_callback, "stocks": stocks_callback}

assistant = GenericAssistant("intents.json", model_name="test_model", intent_methods=mappings)
assistant.train_model()
assistant.save_model()

while True:
    message = input("Message: ")
    if message == "STOP":
        break
    else:
        assistant.request(message)
