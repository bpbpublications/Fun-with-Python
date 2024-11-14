import click
import os
import sqlite3

DB_FILENAME = "virus.db"


class VirusDB:
    def __init__(self):
        self.conn = sqlite3.connect(DB_FILENAME)

    def _execute(self, sql):
        print(f"Executing: {sql}")
        cursor = self.conn.cursor()
        cursor.execute(sql)
        return cursor.fetchall()

    def _commit(self, sql):
        print(f"Insert/update: {sql}")
        cursor = self.conn.cursor()
        cursor.execute(sql)
        return self.conn.commit()

    def init_table(self):
        sql = """CREATE TABLE IF NOT EXISTS virus_db (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            virus_hash TEXT UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )"""
        print(self._execute(sql))

    def import_data(self, sources):
        print(f"Importing: {sources}")
        for source in sources:
            assert os.path.exists(source), f"File {source} does not exist"
            with open(source, "r", encoding="utf-8") as f:
                for line in f:
                    data = line.strip().strip("\n")
                    sql = f"INSERT OR IGNORE INTO virus_db (virus_hash) values ('{data}')"
                    self._commit(sql)


@click.command()
@click.option("--source", help="File with virus definition", multiple=True, type=str)
@click.option("--operation", help="Operation type", required=True, type=click.Choice(["init", "import"]))
def main(operation, source):
    v = VirusDB()
    if operation == "init":
        v.init_table()
    elif operation == "import":
        assert source, "We need source value"
        v.import_data(source)


if __name__ == "__main__":
    main()
