import asyncio
from concurrent.futures import ThreadPoolExecutor

async def task1():
    try:
        for i in range(100):
            print(f"Task 1: hi {i}")
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        print("Task 1 was cancelled")

async def task2():
    try:
        for i in range(100):
            print(f"Task 2: hi {i}")
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        print("Task 2 was cancelled")

async def run():
    loop = asyncio.get_running_loop()
    executor = ThreadPoolExecutor()
    
    t1 = loop.run_in_executor(executor, asyncio.run, task1())
    t2 = loop.run_in_executor(executor, asyncio.run, task2())

    await asyncio.sleep(10)
    t1.cancel()
    await asyncio.sleep(10)
    t2.cancel()

    # Ensure all tasks are completed
    await asyncio.gather(t1, t2, return_exceptions=True)