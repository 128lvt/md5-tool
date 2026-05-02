import asyncio
import aiohttp

url = "http://localhost:8000/login"

payload = {
    "username": "test",
    "password": "123456"
}

TOTAL = 1_000_000
CONCURRENCY = 500   # test dần: 100 → 500 → 1000

connector = aiohttp.TCPConnector(limit=CONCURRENCY)

async def send_request(session, i):
    try:
        async with session.post(url, json=payload) as resp:
            return resp.status
    except:
        return 0

async def main():
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = [send_request(session, i) for i in range(TOTAL)]
        results = await asyncio.gather(*tasks)
        print("Done:", len(results))

asyncio.run(main())
