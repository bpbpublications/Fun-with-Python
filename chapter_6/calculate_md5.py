import hashlib


with open("your_filename.png", "rb") as f:
    file_hash = hashlib.md5()
    chunk = f.read(8192)
    while chunk:
        file_hash.update(chunk)
        chunk = f.read(8192)

print(file_hash.hexdigest())


from hashlib import md5


data = "some amazing string"
print(md5(data).hexdigest())
