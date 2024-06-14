import asyncio
import time
import concurrent.futures
from threading import Event

def task1(cancel_event):
    try:
        for i in range(100):
            if cancel_event.is_set():
                print("Task 1 was cancelled")
                break
            print(f"Task 1: hi {i}")
            time.sleep(1)
    except asyncio.CancelledError:
        print("Task 1 was cancelled")

def task2(cancel_event):
    try:
        for i in range(100):
            if cancel_event.is_set():
                print("Task 2 was cancelled")
                break
            print(f"Task 2: hi {i}")
            time.sleep(1)
    except asyncio.CancelledError:
        print("Task 2 was cancelled")

async def run():
    loop = asyncio.get_event_loop()
    executor = concurrent.futures.ThreadPoolExecutor()

    cancel_event1 = Event()
    cancel_event2 = Event()

    t1 = loop.run_in_executor(executor, task1, cancel_event1)
    t2 = loop.run_in_executor(executor, task2, cancel_event2)

    await asyncio.sleep(10)
    # Cancel execution of task2
    cancel_event2.set()

    await asyncio.sleep(10)
    # Ensure all tasks are completed
    await asyncio.gather(t1, t2, return_exceptions=True)