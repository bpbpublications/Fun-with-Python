from cryptography.fernet import Fernet

with open("key", "rb") as f:
    key = f.read()

with open("cc.json", "rb") as f:
    data = f.read()

fernet = Fernet(key)
encrypted = fernet.encrypt(data)

with open("cc.data", "wb") as f:
    f.write(encrypted)
