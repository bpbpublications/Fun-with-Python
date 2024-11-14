# install

```bash
$ pip install ebaysdk pyyaml
```

## token

```yaml
name: ebay_api_config
api.sandbox.ebay.com:
    compatibility: 719
    appid: <your app ID>
    certid: <generated cert ID>
    devid: <dev ID>
    token: <generated auth'n'auth token>
```

## API serch reponse

```python
{'ack': 'Success',
 'itemSearchURL': 'https://shop.sandbox.ebay.com/i.html?_nkw=watch&_ddo=1&_ipg=100&_pgn=1',
 'paginationOutput': {'entriesPerPage': '100', 'pageNumber': '1',
                      'totalEntries': '148', 'totalPages': '2'},
 'searchResult': {
    '_count': '82',
    'item': [{'autoPay': 'false',
            'condition': {'conditionDisplayName': 'New',
                            'conditionId': '1000'},
            'country': 'US',
            'galleryURL': None,
            'globalId': 'EBAY-US',
            'isMultiVariationListing': 'false',
            'itemId': '110555269430',
            'listingInfo': {
                'bestOfferEnabled': 'false',
                'buyItNowAvailable': 'false',
                'endTime': '2024-07-20T06:08:34.000Z',
                'gift': 'false',
                'listingType': 'FixedPrice',
                'startTime': '2024-06-20T06:08:34.000Z'},
            'location': 'USA',
            'primaryCategory': {
                'categoryId': '69527',
                'categoryName': 'Other Marine '
                                'Life '
                                'Collectibles'},
            'returnsAccepted': 'true',
            'sellingStatus': {
                'convertedCurrentPrice': {'_currencyId': 'USD',
                                        'value': '43.0'},
                'currentPrice': {'_currencyId': 'USD',
                                'value': '43.0'},
                'sellingState': 'Active',
                'timeLeft': 'P26DT14H45M37S'},
            'shippingInfo': {
                'expeditedShipping': 'false',
                'handlingTime': '5',
                'oneDayShippingAvailable': 'false',
                'shipToLocations': 'Worldwide',
                'shippingServiceCost': {'_currencyId': 'USD',
                                        'value': '10.0'},
                'shippingType': 'Flat'},
            'title': 'Summit Watch',
            'topRatedListing': 'false',
            'viewItemURL': 'https://cgi.sandbox.ebay.com/Summit-Watch-/110555269430'},
            #<... more result .>
            ]},
 'timestamp': '2024-03-23T15:22:57.941Z',
 'version': '1.13.0'}
 ```

# API endpoint

```python
from ebaysdk.finding import Connection as Finding
api = Finding(
    domain="svcs.sandbox.ebay.com",
    appid=data['api.sandbox.ebay.com']['appid'],
    config_file="ebay.yaml",
    siteid="EBAY-GB",
    version="1.18.2",
)
```


# snipppet

## run

```bash
$ python main_app.py --phrase "iphone"

Found NEW item URL: https://cgi.sandbox.ebay.com/30W-Wireless-Fast-Charger-Mat-Pad-Apple-Air-Pods-iPhone-13-Pro-Max-12-14-15-/110555545034
{'price': '13.0', 'currency': 'USD', 'img': 'https://i.ebayimg.sandbox.ebay.com/images/g/GPkAAOSwzttf~qBC/s-l140.jpg', 'url': 'https://cgi.sandbox.ebay.com/30W-Wireless-Fast-Charger-Mat-Pad-Apple-Air-Pods-iPhone-13-Pro-Max-12-14-15-/110555545034', 'title': '30W Wireless Fast Charger Mat Pad For Apple Air Pods iPhone 13 Pro Max 12 14 15'}
```
