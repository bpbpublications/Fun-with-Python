import asyncio
from asyncio_pool import AioPool

HOST = "wikipedia.org"
PORTS = [443, 80, 25]


async def tcp_port_check(port) -> bool:
    try:
        reader, writer = await asyncio.open_connection(HOST, port)
        return [port, True]
    except Exception as e:
        print(e)
        return [port, False]


async def main():
    async with AioPool(size=5) as pool:
        result = await pool.map(tcp_port_check, PORTS)
        print(dict(result))


if __name__ == "__main__":
    asyncio.run(main())
