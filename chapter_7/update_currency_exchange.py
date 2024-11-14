import click
from live_coin_client import LiveCoinClient


@click.command()
@click.option("--coin", help="Coin to update", type=str, required=False)
@click.option("--days", help="Number of days to fetch", type=int, required=False)
def main(days, coin):
    click.echo("Starting import")
    l = LiveCoinClient()
    if coin:
        l.fetch_crypto(currency_code=coin, days=(days if days else 10))
    else:
        l.fetch_and_update_coins()


if __name__ == "__main__":
    main()
