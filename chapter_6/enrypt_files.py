from Cryptodome import Random
from Cryptodome.Cipher import AES


class FilesEncoder:
    def __init__(self):
        with open("mykey.pem", "rb") as f:
            self.hashing_key = f.read()

    def __make_padding(self, s):
        return s + b"\0" * (AES.block_size - len(s) % AES.block_size)

    def __encode(self, message):
        message = self.__make_padding(message)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.hashing_key, AES.MODE_CBC, iv)
        return iv + cipher.encrypt(message)

    def __decode(self, data):
        iv = data[: AES.block_size]
        cipher = AES.new(self.hashing_key, AES.MODE_CBC, iv)
        plaintext = cipher.decrypt(data[AES.block_size :])
        return plaintext.rstrip(b"\0")

    def encrypt_file(self, file_name):
        with open(file_name, "rb") as f:
            data = f.read()

        encdoded = self.__encode(data)
        enc_filename = f"{file_name}.bin"
        with open(enc_filename, "wb") as fo:
            fo.write(encdoded)
        print(f"Encrypted file {file_name} to {enc_filename}")

    def decrypt_file(self, file_name):
        with open(file_name, "rb") as f:
            data = f.read()

        decoded = self.__decode(data)
        output_file_name = file_name[:-4]
        with open(output_file_name, "wb") as f:
            f.write(decoded)
        print(f"Decrypted file {file_name} to {output_file_name}")


if __name__ == "__main__":
    enc = FilesEncoder()
    enc.encrypt_file("data.txt")
    enc.decrypt_file("data.txt.bin")
