import asyncio
from aiohttp import ClientSession
import json, requests
from time import time

def write_list(a_list):
    with open('authKeyList.txt', 'w', encoding="utf-8") as fp:
        for i in a_list:
            fp.write(str(i) + "\n")


async def fetch(url, session):
    async with session.get(url) as response:
        return await response.read()

async def push(url, session, authkey):
    async with session.post(url, headers={"Authorization":authkey}) as response:
        return await response.text()


async def run(r):
    global masterList

    url = "https://api.dashcraft.io/auth/createAccount"
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


def genNewKeys(amount):
    global masterList

    revs = amount

    t1 = time()
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(run(revs))
    loop.run_until_complete(future)
    tTotal = time() - t1
    print(f"Generating {revs} account keys took {tTotal} seconds, at an average of {tTotal / revs} seconds per key.")

    keyList = [json.loads(i)["token"] for i in masterList]

    write_list(keyList)


def readKeys():
    with open('authKeyList.txt', 'r', encoding="utf-8") as fp:
        data = fp.readlines()
    return [i.strip("\n") for i in data]


async def likeTrack(trackID, authList):

    url = "https://api.dashcraft.io/track/vote/" + str(trackID) + "/1"
    tasks = []

    # Fetch all responses within one Client session,
    # keep connection alive for all requests.
    async with ClientSession() as session:
        for i in authList:
            task = asyncio.ensure_future(push(url, session, i))
            tasks.append(task)

        responses = await asyncio.gather(*tasks)
        # you now have all response bodies in this variable
        print(responses)


def listLike(trackID, likeCount):
    keyList = readKeys()
    keyLen = len(keyList)
    if likeCount > keyLen:
        print(f"Desired like count exceeds authKey length, reducing likes to {keyLen}.")
        likeCount = keyLen

    t1 = time()
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(likeTrack(likeCount, keyList))
    loop.run_until_complete(future)
    tTotal = time() - t1
    print(f"Liking the track {likeCount} times took {tTotal} seconds, at an average of {tTotal / likeCount} seconds per like.")

def slowListLike(trackID, likeCount):
    keyList = readKeys()
    keyLen = len(keyList)
    if likeCount > keyLen:
        print(f"Desired like count exceeds authKey length, reducing likes to {keyLen}.")
        likeCount = keyLen

    url = "https://api.dashcraft.io/track/vote/" + str(trackID) + "/1"

    t1 = time()

    for i in range(likeCount):
        requests.put(url=url, headers={"Authorization":keyList[i]})

    tTotal = time() - t1
    print(f"Liking the track {likeCount} times took {tTotal} seconds, at an average of {tTotal / likeCount} seconds per like.")

genNewKeys(100)
slowListLike("63f6f014768e3ae5658a9506", 100)