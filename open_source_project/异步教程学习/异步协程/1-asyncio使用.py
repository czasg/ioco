import asyncio
import aiohttp
import time

loop = asyncio.get_event_loop()


async def fetch():
    async with aiohttp.ClientSession(loop=loop) as session:
        async with session.get('http://www.baidu.com') as response:
            print(await response.read())


async def multi_fetch():
    await asyncio.gather(*[asyncio.create_task(fetch()) for _ in range(10)])


if __name__ == '__main__':
    start = time.time()
    loop.run_until_complete(fetch())  # 执行一次
    # loop.run_until_complete(multi_fetch())  # 执行十次
    print(time.time() - start)
