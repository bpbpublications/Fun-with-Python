import click
import os
import magic
import sqlite3
import uuid
import zipfile
from hashlib import sha256

DB_FILENAME = "virus.db"


class VirusScanner:
    def __init__(self):
        self.conn = sqlite3.connect(DB_FILENAME)

    def _execute(self, sql):
        cursor = self.conn.cursor()
        cursor.execute(sql)
        return cursor.fetchall()

    def check_hash(self, has_value) -> bool:
        sql = f"SELECT * FROM virus_db WHERE virus_hash='{has_value}' LIMIT 1"
        cursor = self.conn.cursor()
        cursor.execute(sql)
        return True if cursor.fetchall() else False

    def is_virus(self, file_path, hash_value):
        if not hash_value:
            return
        if self.check_hash(hash_value):
            print(f"File: {file_path}, hash: {hash_value}, status: virus! removing...")
            try:
                # os.remove(file_path)
                print("r" * 20)
            except OSError:
                print("Seem like detected file can't be remove at the moment, in use?")
        else:
            print(f"File: {file_path}, hash: {hash_value}, status: [ok]")

    def scanner(self, file_path: str):
        for (root, dirs, files) in os.walk(file_path, topdown=True):
            for f in files:
                yield os.path.join(root, f)

    def calculate_hash(self, file_path: str) -> str:
        if not file_path:
            return
        try:
            with open(file_path, "rb") as f:
                file_hash = sha256()
                chunk = f.read(8192)
                while chunk:
                    file_hash.update(chunk)
                    chunk = f.read(8192)

                return file_hash.hexdigest()
        except OSError:
            print(f"File {file_path} can not be opened at the moment, skipping")

    def analyze_zip(self, fpath):
        extract_dir = "/tmp/{tmp_id}/".format(tmp_id=str(uuid.uuid4()))
        with zipfile.ZipFile(fpath, "r") as zip_ref:
            zip_ref.extractall(extract_dir)
        self.analyze(extract_dir)
        os.remove(extract_dir)

    def analyze(self, fpath):
        for file_path in self.scanner(fpath):
            try:
                hash_value = self.calculate_hash(file_path)
                self.is_virus(hash_value, file_path)
                if "zip" in magic.from_file(file_path).lower():
                    self.analyze_zip(file_path)
            except OSError:
                print(f"File {file_path} can not be opened at the moment, skipping")


@click.command()
@click.option("--fpath", help="Path to start scanning", required=True)
def main(fpath):
    v = VirusScanner()
    v.analyze(fpath)


if __name__ == "__main__":
    main()
