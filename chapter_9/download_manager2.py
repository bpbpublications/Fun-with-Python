import click
import asyncio
import httpx
import os
from urllib.parse import urlparse


async def download(url):
    async with httpx.AsyncClient() as client:
        print(f"Fetching: {url}")
        response = await client.get(url, follow_redirects=True)
        if response.status_code == 200:
            u = urlparse(url)
            file_name = os.path.basename(u.path)
            with open(f"/tmp/{file_name}", "wb") as f:
                f.write(response.content)


async def download_list(urls_file):
    with open(urls_file, "r") as f:
        for item in f:
            await download(item.strip())


async def main(url=None, url_list=None):
    if url:
        return await download(url)
    if url_list:
        print("Running downloader for given list of URLs")
        return await download_list(url_list)


@click.command()
@click.option("--url", help="File URL path to download")
@click.option("--url-list", help="File with URLs to download")
def run(url, url_list):
    asyncio.run(main(url, url_list))


if __name__ == "__main__":
    run()
