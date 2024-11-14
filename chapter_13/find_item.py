import click
import yaml
from pprint import pprint
from ebaysdk.shopping import Connection as Shopping
from ebaysdk.exception import ConnectionError


@click.command()
@click.option("--item", type=str, help="Item id to get information about", required=True)
def main(item):
    with open("ebay.yaml", "r") as file:
        data = yaml.safe_load(file)

    api = Shopping(
        domain="svcs.sandbox.ebay.com",
        https=True,
        appid=data["api.sandbox.ebay.com"]["appid"],
        config_file="ebay.yaml",
        siteid="EBAY-GB",
        # version="1.18.2",
        debug=True,
    )
    response = api.execute("GetSingleItem", {"ItemID": item})
    pprint(response.dict())


if __name__ == "__main__":
    main()
