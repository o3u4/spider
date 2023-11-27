from scrapy import Spider, Request
from scrapy.crawler import CrawlerProcess
from bar import Bar
import os
from adv_gather import Gather


# 电影爬虫内核,可按需更改parse逻辑
class LocalSpider(Spider):
    name = 'local_spider'

    def __init__(self, name, urls, ts_path, root=None, prt_dl_label=None, **kwargs):
        super().__init__(**kwargs)
        self.name = name  # 视频名称
        self.start_urls = urls  # 起始网址
        self.ts_path = ts_path  # ts保存路径
        self.total = 1  # 总ts数量
        self.pre_num = len(os.listdir(ts_path))  # 已下载ts数量
        self.prg = self.pre_num  # 下载进度
        self.order_list = []  # ts文件顺序
        self.name_list = []  # ts文件名字顺序
        self.bar = Bar(1)  # 下载进度条
        self.cwd = os.getcwd()  # 当前工作路径
        self.root = root
        self.prt_label = prt_dl_label  # ui界面下载进度显示标签

    @staticmethod
    def m3u8_parse(path):  # 获取ts的url
        with open(path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                if line.startswith('#'):
                    continue
                else:
                    ts_url = line.strip()
                    yield ts_url

    @classmethod
    def get_name_list(cls, name):
        order_list = cls.m3u8_parse(f'{name}.m3u8')  # 获取ts的顺序,用于合并
        n_list = []
        for url in order_list:
            n_list.append(url.split('/')[-1])
        return n_list

    def save_ts(self, resp):  # 保存ts
        ts_name = resp.url.split('/')[-1]
        with open(f'{self.ts_path}/{ts_name}', 'wb') as f:
            f.write(resp.body)
        self.prg += 1
        self.bar.prt(self.prg)  # 显示进度条
        if self.prt_label:  # 若有标签,在标签上输出进度
            self.bar.label_prt(self.prg, self.prt_label, self.root)

    def parse(self, response, **kwargs):
        with open(f'{self.name}.m3u8', 'wb') as f:
            f.write(response.body)
        print(f'm3u8文件保存在{self.cwd}/{self.name}.m3u8')
        # 解析m3u8文件
        self.name_list = self.get_name_list(self.name)
        self.total = len(self.name_list)  # ts总数

        print(f'已下载{self.pre_num}个文件')
        print(f'共{self.total}个文件')
        self.bar = Bar(self.total)
        if self.pre_num == self.total:
            print('下载完成!')
        else:
            ts_url_lst = self.m3u8_parse(f'{self.name}.m3u8')
            for ts_url in ts_url_lst:  # 发送请求
                if ts_url.split('/')[-1] in os.listdir(self.ts_path):  # 去重
                    continue
                else:
                    yield Request(url=response.urljoin(ts_url),
                                  method='get',
                                  callback=self.save_ts
                                  )

    @classmethod
    def save_movie(cls, ts_path, movie_path, name_list, root=None, label=None):
        # 合并文件
        Gather(ts_path, movie_path, name_list, root=root, label=label).file_gather()
        if root and label:
            label.config(text='合并完成')
        print(f'视频保存至{movie_path}')

    @classmethod
    def run_spider(cls, name, urls, ts_path, root=None, prt_dl_label=None):     # 运行爬虫会新建实例
        process = CrawlerProcess(settings={
            'USER_AGENT': 'Mozilla/5.0',
            'ROBOTSTXT_OBEY': False,
            'REQUEST_FINGERPRINTER_IMPLEMENTATION': "2.7",
            'TWISTED_REACTOR': "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
            'FEED_EXPORT_ENCODING': "utf-8",
            'LOG_LEVEL': 'WARNING'
        })
        process.crawl(cls, name, urls, ts_path, root,
                      prt_dl_label)
        process.start()


if __name__ == '__main__':
    LocalSpider.run_spider('s',
                           ['https://cdn.1080pzy.co/20210629/EZPo3U2F/1200kb/hls/index.m3u8'],
                           'F:/ts_list')
    nam_list = LocalSpider.get_name_list('san')
    LocalSpider.save_movie('F:/ts_list', 'F:/mv/s.mp4', nam_list)
