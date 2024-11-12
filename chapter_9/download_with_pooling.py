import click
import asyncio
import httpx
import os
from asyncio_pool import AioPool
from urllib.parse import urlparse
from tenacity import AsyncRetrying, RetryError, stop_after_attempt

RETRIES = 3
CONCURRENCY_SIZE = 2


async def download(url):
    """Fetch URL resource with retry"""
    try:
        async for attempt in AsyncRetrying(stop=stop_after_attempt(RETRIES)):
            with attempt:
                click.echo(f"Fetching: {url}")
                async with httpx.AsyncClient() as client:
                    response = await client.get(url, follow_redirects=True)
                    if response.status_code == 200:
                        u = urlparse(url)
                        file_name = os.path.basename(u.path)
                        with open(f"/tmp/{file_name}", "wb") as f:
                            f.write(response.content)
    except RetryError:
        click.echo(f"Failed to fetch {url} after {RETRIES} tries")


async def download_list(urls_file):
    calls = []
    with open(urls_file, "r") as f:
        async with AioPool(size=CONCURRENCY_SIZE) as pool:
            for item in f:
                if item and "http" in item:
                    result = await pool.spawn(download(item.strip()))
                    calls.append(result)


async def main(url=None, url_list=None):
    if url:
        return await download(url)
    if url_list:
        click.echo("Running downloader for given list of URLs")
        return await download_list(url_list)


@click.command()
@click.option("--url", help="File URL path to download")
@click.option("--url-list", help="File with URLs to download")
def run(url, url_list):
    asyncio.run(main(url, url_list))


if __name__ == "__main__":
    ru
