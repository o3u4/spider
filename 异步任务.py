import asyncio


async def async_operation1():
    print("Start async operation 1")
    await asyncio.sleep(1)
    print("Async operation 1 completed")


async def async_operation2():
    print("Start async operation 2")
    await asyncio.sleep(2)
    print("Async operation 2 completed")


async def async_operation3():
    print("Start async operation 3")
    await asyncio.sleep(0.5)
    print("Async operation 3 completed")


async def main():
    print("Start main function")
    await asyncio.gather(
        async_operation1(),
        async_operation2(),
        async_operation3()
    )
    print("All async operations completed")


if __name__ == "__main__":
    asyncio.run(main())
