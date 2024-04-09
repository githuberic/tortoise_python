import asyncio
import time


async def worker():
    print('Worker task started')
    # do some work here
    print('Worker task finished')


def start_worker():
    print('Main task started')
    loop = asyncio.get_event_loop()
    # run the worker coroutine
    loop.run_until_complete(worker())
    # close the event loop
    loop.close()
    print('Main task finished')


async def say_after():
    print('hello')
    await asyncio.sleep(1)
    print('world')


def say_after_main():
    coroutine_obj = say_after()
    asyncio.run(coroutine_obj)


async def say_after_v2(delay, say_what):
    await asyncio.sleep(delay)
    print(say_what)


async def say_after_v2_main():
    print(f"Start at {time.strftime('%X')}")
    await say_after_v2(1, 'Hello')
    await say_after_v2(2, 'World')
    print(f"End at {time.strftime('%X')}")


async def say_after_v3_main():
    task_1 = asyncio.create_task(say_after_v2(1, 'Hello'))
    task_2 = asyncio.create_task(say_after_v2(2, 'World'))

    print(f"Start at {time.strftime('%X')}")
    await task_1
    await  task_2
    print(f"End at {time.strftime('%X')}")


# say_after_main()
#asyncio.run(say_after_v2_main())
if __name__ == "__main__":
    asyncio.run(say_after_v3_main())

