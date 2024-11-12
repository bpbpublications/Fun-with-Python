import click
import time
import requests
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from dotenv import dotenv_values

SUPPORTED_COINS = {"eth": "ethereum", "btc": "bitcoin"}


class CoinApp:
    def __init__(self, coin_str):
        self._config = dotenv_values(".env")
        self._coin_str = coin_str
        self.connect()

    def fetch_exchange(self):
        url = f"https://price-api.crypto.com/price/v1/token-price/{self._coin_str}"
        print(f"Calling {url}")
        result = requests.get(url, headers={"User-Agent": "Firefox"})
        data = result.json()
        return data

    def seed_data(self):
        data = self.fetch_exchange()
        no_of_items = len(data["prices"])
        for i, value in enumerate(data["prices"]):
            self._save_data(value)
            print(f"Write item {i+1}/{no_of_items}")
            time.sleep(1)

    def update_db(self):
        data = self.fetch_exchange()
        value = data["usd_price"]
        self._save_data(value)

    def _save_data(self, value):
        point = Point("price").tag("coin", self._coin_str).field("value", value)
        self._write_api.write(bucket=self._config["bucket"], org=self._config["org"], record=point)

    def connect(self):
        url = "http://localhost:8086"
        client = InfluxDBClient(url=url, token=self._config["API_KEY"], org=self._config["org"])
        self._write_api = client.write_api(write_options=SYNCHRONOUS)


@click.command()
@click.option("--seed", help="Seed example data", required=False, default=False, is_flag=True)
@click.option(
    "--coin", type=click.Choice(SUPPORTED_COINS.keys()), help="Coin symbol to fetch details about", required=True
)
def main(seed, coin):
    if coin not in SUPPORTED_COINS:
        raise Exception("Invalid coin")
    c = CoinApp(SUPPORTED_COINS[coin])
    if seed:
        c.seed_data()
    else:
        c.update_db()


if __name__ == "__main__":
    main()
