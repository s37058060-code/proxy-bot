import asyncio
import aiohttp
import time

async def check_proxy(session, proxy):
    try:
        start = time.time()
        async with session.get("http://httpbin.org/ip", proxy="http://" + proxy, timeout=5) as r:
            if r.status == 200:
                speed = round(time.time() - start, 2)
                return (proxy, speed)
    except:
        return None

async def check_all(proxies):
    async with aiohttp.ClientSession() as session:
        tasks = [check_proxy(session, p) for p in proxies]
        results = await asyncio.gather(*tasks)

        working = [r for r in results if r]
        working.sort(key=lambda x: x[1])
        
        return working
