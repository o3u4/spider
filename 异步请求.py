import aiohttp
import asyncio
import json


async def fetch_url(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()


async def main1():
    url1 = "https://example.com/api1"
    url2 = "https://example.com/api2"
    url3 = "https://example.com/api3"

    results = await asyncio.gather(
        fetch_url(url1),
        fetch_url(url2),
        fetch_url(url3)
    )

    for result in results:
        print(result)


ua = ''


async def mp3_download_async(order):
    url = 'http://www.2t58.com/js/play.php'  # 接口获取mp3网址
    code = order  # 歌曲独特编号
    payload = {'id': code, 'type': 'music'}
    refer = f'http://www.2t58.com/song/{code}.html'  # 防盗链
    headers = {'Referer': refer, 'User-Agent': ua}

    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload, headers=headers) as response:
            data = await response.text()

            # 解析 JSON 数据
            parsed_data = json.loads(data)
            # 提取 title 和 url 元素放入字典
            result = [parsed_data["title"], parsed_data["url"]]
            print(result)
            name = parsed_data["title"]
            mp3_url = result[1]

            async with session.get(mp3_url) as mp3_response:
                mp3_content = await mp3_response.read()

                # 写歌
                with open(f"./{name}.mp3", mode="wb") as f:
                    f.write(mp3_content)
                print(f"成功下载", name)


async def main2():
    await asyncio.gather(  # 调用异步下载函数
        mp3_download_async("code1"),
        mp3_download_async("code2"),
        mp3_download_async("code3")
    )


if __name__ == "__main__":
    asyncio.run(main2())
