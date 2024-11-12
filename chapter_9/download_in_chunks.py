import asyncio
import httpx
import os
from asyncio_pool import AioPool
from urllib.parse import urlparse

URL = "https://www.python.org/ftp/python/3.12.0/Python-3.12.0.tgz"


async def get_size(url):
    async with httpx.AsyncClient() as client:
        response = await client.head(url)
        size = int(response.headers["Content-Length"])
        return size


async def download_range(url, start, end, output):
    headers = {"Range": f"bytes={start}-{end}"}
    async with httpx.AsyncClient() as client:
        response = await client.get(url, follow_redirects=True, headers=headers)

    with open(output, "wb") as f:
        for part in response.iter_bytes():
            f.write(part)
    print(f"Finished: {output}")


async def download(url, output, chunk_size=1000000):
    file_size = await get_size(url)
    chunks = range(0, file_size, chunk_size)
    print(f"Planned number of chunks: {len(chunks)}")
    calls = []
    async with AioPool(size=int(len(chunks) / 3)) as pool:
        for i, start in enumerate(chunks):
            partial_output = f"{output}.part{i}"
            result = await pool.spawn(download_range(url, start, start + chunk_size - 1, partial_output))
            calls.append(result)

    with open(output, "wb") as o:
        for i in range(len(chunks)):
            chunk_path = f"{output}.part{i}"

            with open(chunk_path, "rb") as s:
                o.write(s.read())
            os.remove(chunk_path)


if __name__ == "__main__":
    _url = urlparse(URL)
    file_name = _url.path.split("/")[-1].strip()
    output_path = f"/tmp/{file_name}"
    asyncio.run(download(URL, output_path))
