# encrypt

```sh
pip install pycryptodomex
```

# create key

```python
from Cryptodome.Random import get_random_bytes

with open('mykey.pem','wb') as f:
    f.write(get_random_bytes(16))
```

## encrypt

```python
enc = FilesEncoder()
enc.encrypt_file('data.txt')
```

## decrypt

```python
enc = FilesEncoder()
enc.decrypt_file('data.txt.bin')
```
