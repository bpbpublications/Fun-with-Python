import click
from db import DB


@click.command()
@click.option(
    "--table",
    help="Table type",
    required=True,
    type=click.Choice(["currency", "currency_exchange", "currency_exchange_history"]),
)
def main(table):
    db = DB()
    db.init_table(table)


if __name__ == "__main__":
    main()
