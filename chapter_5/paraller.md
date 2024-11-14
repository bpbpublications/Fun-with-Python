# basics

```python
import random
import asyncio


async def func(func_number: int) -> None:
    for i in range(1, 6):
        sleep_time = random.randint(1, 5)
        print(f"Func {func_number} go {i}/5, taking nap {sleep_time}s")
        await asyncio.sleep(sleep_time)


async def call_tests():
    await asyncio.gather(func(1), func(2), func(3))

asyncio.run(call_tests())
```

# full parallel

```python
async def process_item(self, item: str, number_of_retries: int):
    base_url = urlparse(url)
    content = await self.fetch_url(url, number_of_retries)
    results = LINK.findall(content)
    click.echo(f"Found {len(results)} links")
    calls = []
    for parsed_url in results:
        if parsed_url.startswith('/'):
            parsed_url = f"{base_url.scheme}://{base_url.netloc}{parsed_url}"
        if not parsed_url.startswith('http'):
            continue
        calls.append(self.fetch_url(parsed_url, number_of_retries))
    return await asyncio.gather(*calls)

async def process(self):
    """Main method to start crawler and process"""
    calls = []
    while True:
        url, number_of_retries = await self.urls_queue.get()
        calls.append(process_item(item, number_of_retries))
        if self.urls_queue.empty():
            break
    await asyncio.gather(*calls)
    click.echo("Processing finished, exiting...")
```

# with tasks pool

```python

from asyncio_pool import AioPool


async with AioPool(size=settings.RESTPACK_CONCURRENCY) as pool:
    for index, (item, client_timezone) in enumerate(query):
        item_service = Service(item.service)
        result = await pool.spawn(process_screenshot(item, client_timezone, None, None, index))
        futures.append(result)

```
