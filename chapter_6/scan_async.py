import os
import asyncio
from aiofiles import os as asyncio_os


async def async_scan_dir(dir_path):
    dirs = []
    dir_list = await asyncio_os.listdir(dir_path)
    for check_path in dir_list:
        v_path = os.path.join(dir_path, check_path)
        is_dir = await asyncio_os.path.isdir(v_path)
        if is_dir:
            dirs += await async_scan_dir(v_path)
        else:
            dirs.append(v_path)
    return dirs


async def get_result(dir_path="/tmp"):
    result = await async_scan_dir(dir_path)
    print(f"result: {result}")


asyncio.run(get_result())
