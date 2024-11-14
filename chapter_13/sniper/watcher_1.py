import click
import pycron
from datetime import datetime
from clients import __all__

product_url = None
provider_name = None
choices = [x.__name__.lower()[6:] for x in __all__]


@pycron.cron("*/1 * * * *")
async def check_product_availability(timestamp: datetime):
    print(f"started checking price for: {provider_name}")
    client = provider_name()
    client.product_details(product_url)


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
