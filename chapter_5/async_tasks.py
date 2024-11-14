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
