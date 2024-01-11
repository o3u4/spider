import aiofiles
import asyncio


async def write_to_file_async(file_name, content, time):
    async with aiofiles.open(file_name, mode='a') as file:  # 使用追加模式打开文件
        await asyncio.sleep(time)
        await file.write(content)
        print(file_name + 'finished')


async def main():
    file_names = ["file1.txt", "file2.txt", "file3.txt"]
    content = "Hello, this is asynchronous file operation!\n"

    await asyncio.gather(
        write_to_file_async(file_names[2], content, 2),
        write_to_file_async(file_names[1], content, 3),
        write_to_file_async(file_names[0], content, 1)
    )


if __name__ == "__main__":
    asyncio.run(main())
