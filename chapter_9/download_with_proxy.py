import click
import asyncio
import httpx
import os
import random
from asyncio_pool import AioPool
from hashlib import sha256
from urllib.parse import urlparse
from tenacity import AsyncRetrying, RetryError, stop_after_attempt

RETRIES = 3
CONCURRENCY_SIZE = 2


class Downloader:
    def __init__(self, proxies=None):
        self.proxies = proxies

    async def download(self, url):
        """Fetch URL resource with retry"""
        try:
            async for attempt in AsyncRetrying(stop=stop_after_attempt(RETRIES)):
                with attempt:
                    proxy_server = None
                    if self.proxies:
                        proxy_server = {
                            "all://": random.choice(self.proxies),
                        }
                    click.echo(f"Fetching: {url}, proxy: {proxy_server}")
                    async with httpx.AsyncClient(proxies=proxy_server) as client:
                        response = await client.get(url, follow_redirects=True)
                        if response.status_code == 200:
                            u = urlparse(url)
                            file_hash = sha256(url.encode("utf8")).hexdigest()
                            file_name = f"{os.path.basename(u.path)}_{file_hash}"
                            with open(f"/tmp/{file_name}", "wb") as f:
                                f.write(response.content)
        except RetryError:
            click.echo(f"Failed to fetch {url} after {RETRIES} tries")

    async def download_list(self, urls_file):
        calls = []
        with open(urls_file, "r") as f:
            async with AioPool(size=CONCURRENCY_SIZE) as pool:
                for item in f:
                    if item and "http" in item:
                        result = await pool.spawn(self.download(item.strip()))
                        calls.append(result)


@click.command()
@click.option("--url", help="File URL path to download")
@click.option("--url-list", help="File with URLs to download")
@click.option("--proxy", help="List of proxy servers", multiple=True)
def run(url, url_list, proxy):
    d = Downloader(proxy)
    if url:
        run_app = d.download(url)
    elif url_list:
        run_app = d.download_list(url_list)
    if run_app:
        asyncio.run(run_app)
    else:
        click.echo("No option selected")


if __name__ == "__main__":
    run()
