# install package

requirements

```bash
$ pip install pycryptodome==3.17 web3==6.0.0
$ git clone git@github.com:bpbpublications/Fun-with-Python.git
$ cd fun-with-Python/chapter_7/eth-keyfile/
$ python setup.py install
```

install

```bash
$ pip install -r requirements.txt
```

# generate

```python
from web3 import Web3

acc = w3.eth.account.create()
print(f"Public address of wallet: {acc.address}")
print(f"Private key: {acc.key.hex()}")
```

# recover

Recover from private key

```python
from web3 import Web3

acc = w3.eth.account.create()
private_key = acc.key.hex()

recovered_account = w3.eth.account.from_key(private_key)
is_same = recovered_account.address == acc.address
print(f"Is adresss the same: {is_same}")
```

# get value

```python
from web3 import Web3

w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))
print("Are we connected", w3.is_connected())

wallet_address = "0x8b5105D3c66617D3D3Bc45c1d9714138E4b228BD"
balance = w3.eth.get_balance(wallet_address)
print(f"Balance: {balance}")
```

output

```python
$ python eth_client.py

Are we connected True
100000000000000000000
```

# convert from wei

```python
from web3 import Web3

w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))
print("Are we connected", w3.is_connected())

wallet_address = "0x8b5105D3c66617D3D3Bc45c1d9714138E4b228BD"
balance = w3.eth.get_balance(wallet_address)
human_blance = w3.from_wei(balance, "ether")
print(f"balance: {human_blance:.2f}")
```


# config

https://docs.python.org/3/library/configparser.html

# main

```ini
[network]
server=http://127.0.0.1:7545

[wallet]
main=0x6D4a84a4E7b7A0D1c1b68D8c18D88e4d21D67484
trade=0x43319A04776dc250559eB752584FD0791Cf5688f
```

```python
import configparser

config = configparser.ConfigParser()
config.sections()
config.read('config.ini')
````

# check balance

```sh
$ python eth_client_with_sending.py --balance

Are we connected True
balance: 100.00
balance: 100.00
```

# send coins

```sh
$ python eth_client_with_sending.py --send --amount 0.5

Are we connected True
Sending result: 0x55f6e2ba7da3d8751bddce4fb8f8fef32fd82b9db35d873fe952f3e94c4f94d8
```

# numpy

```sh
$ pip install numpy==1.21.6
```
## tends

* raising

```python
import numpy as np

def growing_avg(a, n=3)
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n

rates_1 = [3.0, 6.0, 10.0, 4.2, 11.0]
rates_2 = [6.0, 5.5, 9.1, 3.9, 9.8]

print("Is growing trend: ", growing_avg(rates_1))
print("Is growing trend: ", growing_avg(rates_2))
```

# calculate

```python
import numpy as np
from db import DB


class AnalyzeRates:

    def __init__(self, currency):
        self.currency = currency
        self._db = DB()

    def growing_avg(self, a, n=3):
        ret = np.cumsum(a, dtype=float)
        ret[n:] = ret[n:] - ret[:-n]
        return ret[n - 1:] / n

    def is_growing(self, data):
        return np.all(np.diff(self.growing_avg(np.array(data), n=4))>0)

    def _get_last_rates(self, limit=7):
        sql = f"SELECT last_price FROM currency_exchange_history WHERE currency_code='{self.currency}' ORDER BY updated_at DESC LIMIT {limit}"
        return [x['last_price'] for x in self._db.execute(sql)]

    def check_currency_growing(self):
        currency_values = self._get_last_rates()
        return self.is_growing(currency_values)

if __name__ == "__main__":
    checker = AnalyzeRates('ETH')
    result = checker.check_currency_growing()
    tendency = 'growing' if result else 'falling'
    print(f'Currency ETH has tendency to {tendency}')
```
