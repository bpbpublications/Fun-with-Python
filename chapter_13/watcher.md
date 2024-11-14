# watchewr

## example params

```python
python watcher.py --help

Usage: watcher.py [OPTIONS]

Options:
  --url TEXT                Product URL to observe  [required]
  --provider [ebay|amazon]  Provider  [required]
  --help                    Show this message and exit.
```


# alerts

```bash
$ pip install plyer pyobjus
```


# run watcher

```bash
$ python watcher.py --watch

Exception in thread Thread-1:
Traceback (most recent call last):
  (..)
    asyncio.run(self.check_prices())
    raise RuntimeError(
RuntimeError: asyncio.run() cannot be called from a running event loop
^C
Aborted!
sys:1: RuntimeWarning: coroutine 'PriceChecker.check_prices' was never awaited
RuntimeWarning: Enable tracemalloc to get the object allocation traceback
```

## fix

```bash
$ python watcher_6.py --price

Checking for prices: <class 'clients.amazon.ClientAmazon'>
Current price: 349.99
Current price: 389.99
Checking for prices: <class 'clients.ebay.ClientEbay'>
Current price: 289.99
```
