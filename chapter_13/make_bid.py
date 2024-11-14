import click
import yaml
from pprint import pprint
from ebaysdk.trading import Connection as Trading

from ebaysdk.exception import ConnectionError


@click.command()
@click.option("--item", type=str, help="Item id to get information about", required=True)
def main(item):
    with open("ebay.yaml", "r") as file:
        data = yaml.safe_load(file)

    api = Trading(
        domain="api.sandbox.ebay.com",  # open.api.ebay.com
        https=True,
        appid=data["api.sandbox.ebay.com"]["appid"],
        config_file="ebay.yaml",
        siteid="2",
        # version="1.18.2",
    )
    response = api.execute("proxyBidId", {"ItemID": item, "DetailLevel": "ReturnAll"})
    pprint(response.dict())


if __name__ == "__main__":
    main()
