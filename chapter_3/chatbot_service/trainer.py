
from chatbot import chatbot
from chatterbot.trainers import ChatterBotCorpusTrainer

_chatbot = chatbot()
trainer = ChatterBotCorpusTrainer(_chatbot)
trainer.train("chatterbot.corpus.english")
