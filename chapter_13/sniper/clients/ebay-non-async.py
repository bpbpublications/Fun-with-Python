import os
import yaml
from pprint import pprint
from ebaysdk.finding import Connection as Finding
from ebaysdk.exception import ConnectionError
from ebaysdk.shopping import Connection as Shopping

EBAY_SANDBOX_API = "svcs.sandbox.ebay.com"
EBAY_API = "svcs.ebay.com"
SITE_ID = "EBAY-US"


class ClientEbay:
    def __init__(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.__config_file = os.path.join(dir_path, "..", "configs", "ebay.yaml")
        self.config = self.__load_config()

    def __load_config(self):
        with open(self.__config_file, "r") as file:
            return yaml.safe_load(file)

    def find_items(self, search_phrase):
        api = Finding(
            domain=EBAY_API,
            # appid=self.config["api.sandbox.ebay.com"]["appid"],
            appid=self.config["api.ebay.com"]["appid"],
            config_file=self.__config_file,
            siteid=SITE_ID,
        )
        response = api.execute(
            "findItemsAdvanced",
            {
                "keywords": search_phrase,
                "itemFilter": [
                    {"name": "Condition", "value": "New"},
                    {"name": "currency", "value": "USD"},
                    {"name": "minPrice", "value": 300},
                ],
                "sortOrder": "BestPrice",
            },
        )
        response = response.dict()
        items = []
        if int(response["searchResult"]["_count"]) > 0:
            for item in response["searchResult"]["item"]:
                if item["condition"]["conditionDisplayName"] == "New":
                    url = item["viewItemURL"]
                    print(f"Found NEW item URL: {url}")
                    items.append(
                        {
                            "price": item["itemId"],
                            "currency": item["sellingStatus"]["currentPrice"]["_currencyId"],
                            "price": item["sellingStatus"]["currentPrice"]["value"],
                            "img": item["galleryURL"],
                            "url": item["viewItemURL"],
                            "title": item["title"],
                        }
                    )

        return items

    def get_item_details(self, item_id):
        api = Shopping(
            domain=EBAY_API,
            https=True,
            appid=self.config["api.sandbox.ebay.com"]["appid"],
            config_file=self.__config_file,
            siteid=SITE_ID,
        )
        response = api.execute("GetSingleItem", {"ItemID": item_id})

    def product_details(self, product_url):
        pass
