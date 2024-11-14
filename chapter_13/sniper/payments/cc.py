import json
from cryptography.fernet import Fernet


class PaymentCreditCard:
    def __init__(self, enc_key):
        self.encryption_key = enc_key

    def load_cc_settings(self):
        enc = Fernet(self.encryption_key)
        with open("cc.data", "rb") as f:
            encoded_data = f.read()
            data = json.loads(enc.decrypt(encoded_data))
            return data

    def pay(self):
        # here we can include logic how to perform payment
        return self.__load_cc_settings()
