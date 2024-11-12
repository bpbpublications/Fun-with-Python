import click
import asyncio
import httpx
import os
from urllib.parse import urlparse


async def main(url):
    async with httpx.AsyncClient() as client:
        response = await client.get(url, follow_redirects=True)

        if response.status_code == 200:
            u = urlparse(url)
            file_name = os.path.basename(u.path)
            with open(f"/tmp/{file_name}", "wb") as f:
                f.write(response.content)


@click.command()
@click.option("--url", help="File URL path to download  ", required=True)
def run(url):
    asyncio.run(main(url))


if __name__ == "__main__":
    run()
