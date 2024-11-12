import click
import time
import requests
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from dotenv import dotenv_values

SUPPORTED_COINS = {"eth": "ethereum", "btc": "bitcoin"}
URL = "http://localhost:8086"


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

    def update_db(self, alarm):
        data = self.fetch_exchange()
        value = data["usd_price"]
        self._save_data(value)
        self.check_value(alarm)

    def check_value(self, alarm):
        query = """
        from(bucket: "coins")
        |> range(start: -1000m)
        |> filter(fn: (r) => r._measurement == "price")
        |> sort(columns: ["_time"], desc: true)
        |> limit(n:2)
        """
        client = InfluxDBClient(url=URL, token=self._config["API_KEY"], org=self._config["org"])
        query_api = client.query_api()
        result = query_api.query(org=self._config["org"], query=query)
        results = []
        for table in result:
            for record in table.records:
                results.append(record.get_value())
        print(results)
        ratio = results[1] / results[0]
        trend_percentage = (ratio * 100) - 100
        print(f"Trends change: {trend_percentage}%")
        if abs(trend_percentage) > alarm:
            print(f"WARNING: Critical change since last time we fetched data, change: {trend_percentage}%")

    def _save_data(self, value):
        point = Point("price").tag("coin", self._coin_str).field("value", value)
        self._write_api.write(bucket=self._config["bucket"], org=self._config["org"], record=point)

    def connect(self):
        client = InfluxDBClient(url=URL, token=self._config["API_KEY"], org=self._config["org"])
        self._write_api = client.write_api(write_options=SYNCHRONOUS)


@click.command()
@click.option("--alarm", help="Alarm level - percentage", required=False, default=False, type=int)
@click.option("--seed", help="Seed example data", required=False, default=False, is_flag=True)
@click.option(
    "--coin", type=click.Choice(SUPPORTED_COINS.keys()), help="Coin symbol to fetch details about", required=True
)
def main(alarm, seed, coin):
    if coin not in SUPPORTED_COINS:
        raise Exception("Invalid coin")
    c = CoinApp(SUPPORTED_COINS[coin])
    if seed:
        c.seed_data()
    else:
        c.update_db(alarm)


if __name__ == "__main__":
    main()
