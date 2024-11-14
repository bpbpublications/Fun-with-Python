# proxy


```Python
PROXIES = {
    "http://": "http://proxy.foo.com:8030",
    "https://": "http://proxy.foo.com:8031",
}
```

in the call

```Python
async def fetch_url(self, url: str, number_of_retries: int) -> Optional[str]:
    click.echo(f"Fetching {url}")
    for try_item in range(int(number_of_retries)):
        try:
            async with httpx.AsyncClient(proxies=PROXIES) as client:
                response = await client.get(url, follow_redirects=True)
            content_type = response.headers.get('Content-Type').split(';')[0]
            extension = content_type.split('/')[-1].lower()
            if response.status_code == 200:
                f_name = sha256(url.encode('utf-8')).hexdigest()
                output_file = f"/tmp/{f_name}.{extension}"
                with open(output_file, "wb") as f:
                    data = response.content
                    f.write(data)
                    click.echo(f"URL: {url} [saved] under {output_file}")
                    return data.decode('utf-8')
        except Exception as e:
            click.echo(f"We failed to fetch URL {url} with exeception: {e}")

        click.echo(f"Fetching resource failed with status code {response.status_code} sleeping {SLEEP_TIME}s before retry")
        if response.status_code != 404:
            await asyncio.sleep(SLEEP_TIME)
````

random proxies

```python
import random

_PROXIES_HTTP = ("http://proxy.foo.com:8030", "http://proxy2.foo.com", "http://proxy3.foo.com")
_PROXIES_HTTPS = ("https://http-proxy1.foo.com", "https://http-proxy2.foo.com","https://http-proxy3.foo.com")

async def fetch_url(self, url: str, number_of_retries: int) -> Optional[str]:
    random.choice(proxies)
    my_proxies = {
        "http://": random.choice(_PROXIES_HTTP),
        "https://": random.choice(_PROXIES_HTTPS),
    }
    click.echo(f"Fetching {url}")
    for try_item in range(int(number_of_retries)):
        try:
            async with httpx.AsyncClient(proxies=my_proxies) as client:
                ...
```
