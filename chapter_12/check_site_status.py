import asyncio
import click
import httpx


async def check_status(url):
    async with httpx.AsyncClient() as client:
        response = await client.get(url, follow_redirects=True)
        status = response.status_code == 200 and len(response.text) >= 50
        print(f"Site status: {status}")


@click.command()
@click.option("--url", help="URL to scan", required=True)
def main(url):
    asyncio.run(check_status(url))


if __name__ == "__main__":
    main()
