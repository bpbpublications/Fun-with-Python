import click
import os
from hashlib import sha256

BUFF_SIZE = 8192


def scanner(file_path: str):
    for (root, dirs, files) in os.walk(file_path, topdown=True):
        for f in files:
            yield os.path.join(root, f)


def calculate_hash(file_path: str) -> str:
    with open(file_path, "rb") as f:
        file_hash = sha256()
        chunk = f.read(BUFF_SIZE)
        while chunk:
            file_hash.update(chunk)
            chunk = f.read(BUFF_SIZE)

        return file_hash.hexdigest()


@click.command()
@click.option("--virus_def", help="File with virus definition", required=True)
@click.option("--fpath", help="Path to start scanning", required=True)
def main(fpath, virus_def):
    with open(virus_def, "rb") as f:
        viruses_list = f.read().decode("utf-8").replace(" ", "").split("\n")

    for file_path in scanner(fpath):
        hash_value = calculate_hash(file_path)
        status = "ok"
        if hash_value in viruses_list:
            status = "virus!"

        print(f"File: {file_path}, hash: {hash_value}, status: {status}")


main()
