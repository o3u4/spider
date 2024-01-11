import concurrent.futures
import asyncio
import time


# 定义一个耗时的函数，模拟I/O操作
def io_bound_task(n):
    print(f'Starting I/O bound task {n}')
    time.sleep(2)  # 模拟一个耗时的I/O操作
    print(f'Finished I/O bound task {n}')


# 定义一个CPU密集型的函数，模拟计算操作
def cpu_bound_task(n):
    print(f'Starting CPU bound task {n}')
    result = sum(i * i for i in range(10 ** 7))  # 模拟一个CPU密集型的计算操作
    print(f'Finished CPU bound task {n}')
    return result  # 返回计算结果


async def main():
    # 创建一个线程池，最多同时执行2个线程
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        # 在线程池中执行两个耗时的I/O操作
        loop = asyncio.get_event_loop()  # 获取当前的事件循环, 异步事件
        await loop.run_in_executor(executor, io_bound_task, 1)  # 在线程池中以异步的方式执行
        await loop.run_in_executor(executor, io_bound_task, 2)

    # 在异步任务中执行CPU密集型的计算操作
    cpu_task_1 = asyncio.get_event_loop().run_in_executor(None, cpu_bound_task, 1)
    cpu_task_2 = asyncio.get_event_loop().run_in_executor(None, cpu_bound_task, 2)
    results = await asyncio.gather(cpu_task_1, cpu_task_2)
    print(results)  # 打印计算结果


# 运行异步任务
asyncio.run(main())

# 无异步线程, 创建一个最多同时执行2个线程的线程池
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
    # 在线程池中执行两个耗时的I/O操作
    executor.submit(io_bound_task, 1)
    executor.submit(io_bound_task, 2)
