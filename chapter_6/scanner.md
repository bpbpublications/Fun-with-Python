# simple

## MD5

```python
from hashlib import md5

data = b"some amazing string"
print(md5(data).hexdigest())
```

## SHA-256

```python
from hashlib import sha256

data = b"some amazing string"
print(sha256(data).hexdigest())
```


# recurrency

## memory

```python
def check_for_virus(file_path):
    """pseudo code for scanning file if it contains virus"""
    pass

@click.command()
@click.option("--fpath", help="Path to start scanning", required=True)
def main(fpath):
    for file_path_to_scan in scanner(fpath):
        check_for_virus(file_path_to_scan)
```

## non recurrency

```python
import click
import os

def scanner(file_path):
    for (root, dirs, files) in os.walk(file_path, topdown=True):
        for f in files:
          yield os.path.join(root, f)


@click.command()
@click.option("--fpath", help="Path to start scanning", required=True)
def main(fpath):
    print(list(scanner(fpath)))


if __name__ == '__main__':
    main()
```

# scanning and calculating

Scanning and calculating SHA 256

```python
import click
import os
from hashlib import sha256

def scanner(file_path):
    for (root, dirs, files) in os.walk(file_path, topdown=True):
        for f in files:
          yield os.path.join(root, f)


@click.command()
@click.option("--fpath", help="Path to start scanning", required=True)
def main(fpath):
    for file_path in scanner(fpath):
        with open(file_path, 'rb') as f:
		      print(f"File: {file_path}, hash: {sha256(f.read()).hexdigest()}")

main()
```

## with sha256

```python
import click
import os
from hashlib import sha256

def scanner(file_path):
    for (root, dirs, files) in os.walk(file_path, topdown=True):
        for f in files:
          yield os.path.join(root, f)

@click.command()
@click.option("--fpath", help="Path to start scanning", required=True)
def main(fpath):
    for file_path in scanner(fpath):
        with open(file_path, 'rb') as f:
		      print(f"File: {file_path}, hash: {sha256(f.read()).hexdigest()}")

main()
```

## file seek

```python
import click
import os
from hashlib import sha256

def scanner(file_path: str):
    for (root, dirs, files) in os.walk(file_path, topdown=True):
        for f in files:
          yield os.path.join(root, f)

def calculate_hash(file_path: str) -> str:
    with open(file_path, "rb") as f:
        file_hash = sha256()
        chunk = f.read(8192)
        while chunk:
            file_hash.update(chunk)
            chunk = f.read(8192)

        return file_hash.hexdigest()

@click.command()
@click.option("--fpath", help="Path to start scanning", required=True)
def main(fpath):
    for file_path in scanner(fpath):
        hash_value = calculate_hash(file_path)
        print(f"File: {file_path}, hash: {hash_value}")

main()
```

another example

source: stackoverflow
```python
import sys
import hashlib

BUF_SIZE = 65536  # lets read stuff in 64kb chunks!

md5 = hashlib.md5()
sha1 = hashlib.sha1()

with open(sys.argv[1], 'rb') as f:
    while True:
        data = f.read(BUF_SIZE)
        if not data:
            break
        md5.update(data)
        sha1.update(data)

print("MD5: {0}".format(md5.hexdigest()))
print("SHA1: {0}".format(sha1.hexdigest()))
```

# virus

A computer virus is a type of computer program that, when executed, replicates itself by modifying other computer programs and inserting its own code into those programs. If this replication succeeds, the affected areas are then said to be "infected" with a computer virus, a metaphor derived from biological viruses.


# quarantine


## delete infected

```python
import os

VIRUSES_LIST = []

def is_virus(file_path, hash_value):
    status = True
    if hash_value in VIRUSES_LIST:
        status = False

    if status:
        print(f"File: {file_path}, hash: {hash_value}, status: [ok]")
    else:
        print(f"File: {file_path}, hash: {hash_value}, status: virus! removing...")
        try:
            os.remove(file_path)
        except OSError:
            print("Seem like detected file can't be remove at the moment, in use?")


@click.command()
@click.option("--virus_def", help="File with virus definition", required=True)
@click.option("--fpath", help="Path to start scanning", required=True)
def main(fpath, virus_def):
    with open(virus_def, 'rb') as f:
        VIRUSES_LIST = f.read().decode('utf-8').replace(' ', '').split('\n')

    for file_path in scanner(fpath):
        hash_value = calculate_hash(file_path)
        is_virus(hash_value, file_path)
```

```bash
$ pip install python-magic
```

# asynchronous scanning

```bash
$ pip install asyncio_pool asyncio aiofiles
```
