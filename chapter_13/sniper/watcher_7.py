import asyncio
import click
import os
import pycron
import pickle
import yaml
from asyncio_pool import AioPool
from clients import __all__
from datetime import datetime
from hashlib import sha256
from plyer import notification
from concurrent.futures import ThreadPoolExecutor
from payments import PaymentCreditCard

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


class PriceChecker:
    def __init__(self):
        with open("watcher.yaml", "rb") as f:
            config = yaml.safe_load(f)
        self._providers = {}
        for provider in config:
            provider_cls = [x for x in __all__ if f"Client{provider.capitalize()}" == x.__name__].pop()
            self._providers[provider_cls] = config.get(provider)
        self.__lock_file = "/tmp/price_check.lock"

    def load_key(self):
        with open("/tmp/key", "rb") as f:
            return f.read()

    def __create_lock(self):
        with open(self.__lock_file, "w") as f:
            f.write("locked")

    def remove_lock(self):
        if os.path.exists(self.__lock_file):
            os.remove(self.__lock_file)

    def __is_purchase_is_locked(self):
        return os.path.exists(self.__lock_file)

    async def get_single_product_details(self, provider, product_url):
        client = provider()
        print(f"Check product details: {product_url}")
        new_price = await client.product_details(product_url)
        c = Cron(product_url)
        if c.is_price_drop(new_price):
            send_alert(c.load_price(), new_price)
            cc = PaymentCreditCard(self.load_key())
            client.buy(cc.pay())
            self.__create_lock()
        c.save_price(new_price)

    async def check_prices(self):
        calls = []
        print("Calling check process...")
        async with AioPool(size=5) as pool:
            for provider in self._providers:
                for product_url in self._providers.get(provider):
                    calls.append(await pool.spawn(self.get_single_product_details(provider, product_url)))

    def show_prices(self):
        for provider, urls in self._providers.items():
            print(f"Checking for prices: {provider}")
            for product_url in urls:
                c = Cron(product_url)
                if c.load_price():
                    print(f"Current price: {c.load_price()}")
                else:
                    print("Price data not found.")

    def start_processing(self):
        if self.__is_purchase_is_locked():
            print("We already purchased product, canceling processing...")
            return
        try:
            asyncio.get_running_loop()
            # Create a separate thread
            with ThreadPoolExecutor(1) as pool:
                result = pool.submit(lambda: asyncio.run(self.check_prices())).result()
        except RuntimeError:
            result = asyncio.run(self.check_prices())


def send_alert(old_price: str, new_price: str):
    notification.notify(
        title="Price alert",
        message=f"Price is dropped! It was {old_price} and it is now {new_price}",
        app_icon=None,
        timeout=10,
    )


@pycron.cron("*/5 * * * *")
async def check_product_availability(timestamp: datetime):
    p = PriceChecker()
    p.start_processing()


@click.command()
@click.option("--price", help="Show prices", required=False, default=False, is_flag=True)
@click.option("--watch", help="Watch prices", required=False, default=False, is_flag=True)
def main(price, watch):
    if watch:
        pycron.start()
    elif price:
        p = PriceChecker()
        p.show_prices()


if __name__ == "__main__":
    main()
