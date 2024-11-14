import click
import os
from db import DB


@click.command()
@click.option("--table", help="File with virus definition", multiple=True, type=str)
@click.option("--source", help="File with virus definition", multiple=True, type=str)
def main(operation, source):
    v = DB()
    if operation == "init":
        v.init_table()
    elif operation == "import":
        assert source, "We need source value"
        v.import_data(source)


if __name__ == "__main__":
    main()
