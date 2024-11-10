from chatterbot import ChatBot


def chatbot():
    return ChatBot(
        'Trainer',
        storage_adapter='chatterbot.storage.SQLStorageAdapter',
        database_uri='sqlite:///chatbot.sqlite3'
    )
