import click
import sqlite3

DB_FILENAME = "crypto.db"


class DB:
    def __init__(self):
        click.echo(f"Database: {DB_FILENAME}")
        self.conn = sqlite3.connect(DB_FILENAME)
        self.conn.row_factory = sqlite3.Row

    def execute(self, sql):
        print(f"Executing: {sql}")
        cursor = self.conn.cursor()
        cursor.execute(sql)
        return cursor.fetchall()

    def commit(self, sql):
        print(f"Insert/update: {sql}")
        cursor = self.conn.cursor()
        cursor.execute(sql)
        return self.conn.commit()

    def init_table(self, table_name):
        with open(f"{table_name}.sql") as f:
            print(self.execute(f.read()))
