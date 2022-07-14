#!/usr/bin/env python
import asyncio
from locks import Semaphore

# test case taken from 
# https://github.com/python/cpython/pull/93222
async def main():
    sem = Semaphore(1)

    async def c1(tasks):
        async with sem:
            await asyncio.sleep(0)
        tasks[1].cancel()

    async def c2(tasks):
        async with sem:
            await asyncio.sleep(0)

    tasks = []
    tasks.append(asyncio.create_task(c1(tasks)))
    tasks.append(asyncio.create_task(c2(tasks)))

    await asyncio.gather(*tasks, return_exceptions=True)

    while True:
        try:
            await asyncio.wait_for(sem.acquire(), timeout=0.1)
            break
        except asyncio.exceptions.TimeoutError:
            print(f"waiters: {len(sem._waiters)} - _wakeup_scheduled: {sem._wakeup_scheduled}")
    print("succeeded")

asyncio.run(main())
