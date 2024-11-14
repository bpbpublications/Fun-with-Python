import yaml
from pprint import pprint
from ebaysdk.finding import Connection as Finding
from ebaysdk.exception import ConnectionError
from ebaysdk.shopping import Connection as Shopping

try:
    with open("ebay.yaml", "r") as file:
        data = yaml.safe_load(file)

    api = Finding(
        domain="svcs.sandbox.ebay.com",
        appid=data["api.sandbox.ebay.com"]["appid"],
        config_file="ebay.yaml",
        siteid="EBAY-GB",
        version="1.18.2",
    )
    response = api.execute("findItemsAdvanced", {"keywords": "iphone"})
    pprint(response.dict())

    api = Shopping(
        domain="svcs.sandbox.ebay.com",
        appid=data["api.sandbox.ebay.com"]["appid"],
        config_file="ebay.yaml",
        siteid="EBAY-GB",
        version="1.18.2",
    )

    # response = api.execute('FindProducts', {
    #     "ProductID": {
    #         # '@attrs': {'type': 'ISBN'},
    #         '#text': 'iphone'
    #     }})
    response = api.execute(
        "findItemsByProduct",
        """<productId type="ReferenceID">110555342335</productId>
                   <itemFilter><name>MinQuantity</name><value>1</value></itemFilter>""",
    )

    pprint(response.dict())
except ConnectionError as e:
    print(e)
    print(e.response.dict())
