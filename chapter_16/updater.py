import click
import requests
from pprint import pprin

SUPPORTED_COINS = {"eth": "ethereum", "btc": "bitcoin"}


def fetch_exchange(coin_str):
    url = f"https://price-api.crypto.com/price/v1/token-price/{coin_str}"
    print(f"Calling {url}")
    result = requests.get(url, headers={"User-Agent": "Firefox"})
    pprint(result.json())


@click.command()
@click.option(
    "--coin", type=click.Choice(SUPPORTED_COINS.keys()), help="Coin symbol to fetch details about", required=True
)
def main(coin):
    if coin not in SUPPORTED_COINS:
        raise Exception("Invalid coin")
    fetch_exchange(SUPPORTED_COINS[coin])


if __name__ == "__main__":
    main()
