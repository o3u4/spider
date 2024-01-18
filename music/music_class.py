import requests
import json
from lxml import etree
from csv import writer
import aiohttp
import asyncio


class Music:
    ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' \
         'AppleWebKit/537.36 (KHTML, like Gecko) ''Chrome/58.0.3029.110 Safari/537.3'
    fetch_url = 'http://www.2t58.com/js/play.php'

    def page_search(self, key, page=None, current_url=None):  # 当前页搜索歌曲, 返回歌曲编号
        url = ''
        if page and not current_url:  # 指定页数搜索
            url = f'http://www.2t58.com/so/{key}/{page}.html'
        elif current_url and not page:  # 根据下一页网址搜索
            url = current_url
        headers = {'User-Agent': self.ua}
        resp = requests.get(url, headers=headers)
        data = resp.text
        html = etree.HTML(data)

        search_list_name = html.xpath("/html/body/div[1]/div/div[2]/ul/li/div[1]/a/text()")  # 搜索结果名称
        search_list_url = html.xpath("/html/body/div[1]/div/div[2]/ul/li/div[1]/a/@href")  # 搜索结果url
        search_list_order = [item.split('/')[-1].split('.')[0] for item in search_list_url]  # 搜索结果编号
        next_href_list = html.xpath('/html/body/div[1]/div/div[2]/div[2]/a[3]/@href')
        while len(next_href_list) == 0:  # 重新访问, 防止访问过快
            next_href_list = html.xpath('/html/body/div[1]/div/div[2]/div[2]/a[3]/@href')
        next_href = ('http://www.2t58.com' + next_href_list[0])
        # print(search_list_name)
        # print(search_list_url)
        # print(search_list_order)
        return search_list_name, search_list_order, next_href

    def search(self, key):  # 启动搜索
        search_list_name, search_list_order, next_href = self.page_search(key, 1)
        print('搜索结果为:')
        print('-----------------------------------------------')
        self.prt(search_list_name)
        flag = input("是否下一页(是y, 否回车)")

        while flag:
            name_lst, order_lst, next_href = self.page_search(key, current_url=next_href)
            self.prt(name_lst, len(search_list_name))
            search_list_name += name_lst
            search_list_order += order_lst
            flag = input("是否下一页(是y, 否回车)")
        return search_list_name, search_list_order

    @staticmethod
    def choose(lst1, lst2):
        lst = []
        order = int(input("选择序号"))
        lst.append(order)
        print(lst1[order], lst2[order])
        flg = input('继续下载(y或回车)')
        while flg:
            order = int(input("选择序号"))
            lst.append(order)
            print(lst1[order], lst2[order])
            flg = input('继续下载(y或回车)')
        with open("./歌曲编号.csv", mode='a', newline='') as f:
            wt = writer(f)
            wt.writerows([[lst1[num], lst2[num]] for num in lst])
        lst = [lst2[num] for num in lst]
        return lst

    @staticmethod
    def prt(lst1, ori_num=0):
        # print(lst1)
        # print(lst2)   # lst2为删除参数, 输出编号
        for i in range(0, len(lst1)):
            print(ori_num + i, lst1[i])

    async def mp3_async_download(self, order):
        url = self.fetch_url  # 接口获取mp3网址
        code = order  # 歌曲独特编号
        payload = {'id': code, 'type': 'music'}
        refer = f'http://www.2t58.com/song/{code}.html'  # 防盗链
        headers = {'Referer': refer, 'User-Agent': self.ua}

        async with aiohttp.ClientSession() as session:  # 异步发送请求, 获取mp3网址
            async with session.post(url, data=payload, headers=headers) as response:
                await asyncio.sleep(0.5)  # 延迟0.5秒
                data = await response.text()  # 等待返回值

                # 解析 JSON 数据
                parsed_data = json.loads(data)
                # 提取 title 和 url 元素放入字典
                result = [parsed_data["title"], parsed_data["url"]]
                print(result)
                name = parsed_data["title"]
                mp3_url = result[1]

                async with session.get(mp3_url) as mp3_response:  # 请求mp3网址, 下载
                    mp3_content = await mp3_response.read()

                    # 写歌
                    with open(f"./mp3/{name}.mp3", mode="wb") as f:
                        f.write(mp3_content)
                    print(f"成功下载", name)

    def lrc_download(self, name, order):
        # 下载LRC歌词
        url = f'http://www.2t58.com/song/{order}.html'
        headers = {'User-Agent': self.ua}
        resp = requests.get(url, headers=headers)

        html = etree.HTML(resp.text)

        lrc_libretto_url_list = html.xpath("/html/body/div[1]/div/div[2]/div[4]/a[2]/@href")
        lrc_libretto_url = 'http://www.2t58.com/' + lrc_libretto_url_list[0]
        # print(lrc_libretto_url)
        resp = requests.get(lrc_libretto_url, headers=headers)
        with open(f"./{name.lrc}", mode='wb') as f:
            f.write(resp.content)

    async def main(self, lst):  # 运行异步
        tasks = [self.mp3_async_download(code) for code in lst]  # 创建一个任务列表
        await asyncio.gather(*tasks)  # 使用 gather 来并发运行任务

    def run(self):  # 启动流程
        key_word = input("输入关键词:")
        name_list, order_list = self.search(key_word)
        r_code_list = self.choose(name_list, order_list)
        asyncio.run(self.main(r_code_list))


if __name__ == '__main__':
    msc = Music()
    msc.run()
