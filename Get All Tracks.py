import asyncio
from aiohttp import ClientSession
import json

def write_list(a_list):
    with open('masterList.txt', 'w', encoding="utf-8") as fp:
        for i in a_list:
            fp.write(str(i) + "\n")


async def fetch(url, session):
    async with session.get(url) as response:
        return await response.read()

async def run(r):
    global masterList

    url = "https://api.dashcraft.io/track/global/{}/50?sort=2"
    tasks = []

    # Fetch all responses within one Client session,
    # keep connection alive for all requests.
    async with ClientSession() as session:
        for i in range(r):
            task = asyncio.ensure_future(fetch(url.format(i), session))
            tasks.append(task)

        responses = await asyncio.gather(*tasks)
        # you now have all response bodies in this variable
        masterList = responses

masterList = []

revs = 1600

loop = asyncio.get_event_loop()
future = asyncio.ensure_future(run(revs))
loop.run_until_complete(future)

finalList = []

masterList = [json.loads(i) for i in masterList if i != '']

for a in masterList:
    for b in a:
        finalList.append(b)

write_list(finalList)