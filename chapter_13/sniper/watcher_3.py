import click
import os
import pycron
import pickle
from clients import __all__
from datetime import datetime
from hashlib import sha256
from plyer import notification

product_url = None
provider_name = None
choices = [x.__name__.lower()[6:] for x in __all__]


class Cron:
    def __init__(self, product_url):
        self._product_url = product_url
        self._file_hash = sha256(product_url.encode("utf-8")).hexdigest()
        self._file_path = f"/tmp/{self._file_hash}"

    def load_price(self):
        if os.path.exists(self._file_path):
            with open(self._file_path, "rb") as f:
                return pickle.load(f)["price"]

    def save_price(self, price):
        with open(self._file_path, "wb") as f:
            return pickle.dump({"price": price}, f)

    def is_price_drop(self, current_price: float) -> bool:
        return self.load_price() and current_price < self.load_price()


def send_alert(old_price: str, new_price: str):
    notification.notify(
        title="Price alert",
        message=f"Price is dropped! It was {old_price} and it is now {new_price}",
        app_icon=None,
        timeout=10,
    )


@pycron.cron("*/1 * * * *")
async def check_product_availability(timestamp: datetime):
    print(f"started checking price for: {provider_name}")
    client = provider_name()
    new_price = client.product_details(product_url)
    c = Cron(product_url)
    if c.is_price_drop(new_price):
        send_alert(c.load_price(), new_price)
    c.save_price(new_price)


@click.command()
@click.option("--url", help="Product URL to observe", type=str, required=True)
@click.option("--provider", help="Provider", type=click.Choice(choices, case_sensitive=False), required=True)
def main(url, provider):
    global provider_name, product_url
    product_url = url
    provider_name = [x for x in __all__ if f"Client{provider.capitalize()}" == x.__name__].pop()
    print(f"Provider class: {provider_name}")
    pycron.start()


if __name__ == "__main__":
    main()
