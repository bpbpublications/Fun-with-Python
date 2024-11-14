import asyncio
import os
import httpx
import yaml
from bs4 import BeautifulSoup
from pprint import pprint
from ebaysdk.finding import Connection as Finding
from ebaysdk.exception import ConnectionError
from ebaysdk.shopping import Connection as Shopping

EBAY_SANDBOX_API = "svcs.sandbox.ebay.com"
EBAY_API = "svcs.ebay.com"
SITE_ID = "EBAY-US"


class ClientEbay:
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
    }

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

    async def product_details(self, product_url):
        async with httpx.AsyncClient(headers=self.HEADERS, http2=True, follow_redirects=True) as client:
            r = await client.get(product_url)
            s = BeautifulSoup(r.content, "html.parser")
            divs = s.find_all(
                "div",
                {
                    "class": [
                        "x-bin-price",
                    ]
                },
            )
            spans = divs[0].find_all(
                "span",
                {
                    "class": [
                        "ux-textspans",
                    ]
                },
            )
            price = spans[0].text.replace("$", "").replace(",", "").replace("US", "").strip()
            return price
