import asyncio
import click
import os
import magic
import sqlite3
import uuid
import zipfile
from enrypt_files import FilesEncoder
from aiofiles import os as asyncio_os
from hashlib import sha256

DB_FILENAME = "virus.db"


class VirusScanner:
    def __init__(self):
        self.conn = sqlite3.connect(DB_FILENAME)
        self.encryptor = FilesEncoder()
        self.locks = {}
        self.files_to_lock = []
        self.files_to_remove_lock = []

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
                self.encryptor.encrypt_file(file_path)
                os.remove(file_path)
            except OSError:
                print("Seem like detected file can't be remove at the moment, in use?")
        else:
            print(f"File: {file_path}, hash: {hash_value}, status: [ok]")

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

    async def analyze_zip(self, fpath):
        extract_dir = "/tmp/{tmp_id}/".format(tmp_id=str(uuid.uuid4()))
        with zipfile.ZipFile(fpath, "r") as zip_ref:
            zip_ref.extractall(extract_dir)
        await self.analyze(extract_dir)
        os.remove(extract_dir)

    async def async_scan_dir(self, dir_path):
        dirs = []
        dir_list = await asyncio_os.listdir(dir_path)
        for check_path in dir_list:
            v_path = os.path.join(dir_path, check_path)
            is_dir = await asyncio_os.path.isdir(v_path)
            if is_dir:
                dirs += await self.async_scan_dir(v_path)
            else:
                dirs.append(v_path)
        return dirs

    async def analyze(self, fpath):
        for file_path in await self.async_scan_dir(fpath):
            try:
                hash_value = self.calculate_hash(file_path)
                self.is_virus(hash_value, file_path)
                if "zip" in magic.from_file(file_path).lower():
                    await self.analyze_zip(file_path)
            except OSError:
                print(f"File {file_path} can not be opened at the moment, skipping")


@click.command()
@click.option("--fpath", help="Path to start scanning", required=True)
def main(fpath):
    v = VirusScanner()
    asyncio.run(v.analyze(fpath))


if __name__ == "__main__":
    main()
