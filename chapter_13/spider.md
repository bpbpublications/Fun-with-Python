# find item

```
$ python main_app.py --phrase "iphone 14"
```

# no sorting

```python
import click
from clients.main import Main


@click.command()
@click.option("--phrase", type=str, help="Item name to look for", required=True)
def main(phrase):
     m = Main()
     print(m.collect_results(phrase))


if __name__ == "__main__":
    main()
```

# call with limit

```bash
$ python main_app.py --phrase "iphone 14" --limit 1
```

## descengin order

```bash
$ python main_app.py --phrase "iphone 14" --limit 1 --order desc
```

# install

```bash
$ pip install python-cron
```

# asyncio

```bash
$ pip install asyncio-pool
```

http client

```bash
$ pip install httpx
```

## HTTP2

```bash
$ pip install httpx[http2]
```
