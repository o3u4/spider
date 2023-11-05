import scrapy
from scrapy.crawler import CrawlerProcess
import os
from gather import file_gather
from mytq import progress_bar

# https://cdn.1080pzy.co/20210629/EZPo3U2F/1200kb/hls/index.m3u8

m3u8_url = [input("输入m3u8文件网址:")]
video_name = input("输入视频名称:")  # 保存m3u8文件
ts_path = input("输入ts文件保存地址(文件夹绝对地址):")

# 建文件夹保存ts
try:
    os.listdir(ts_path)
    print('已存在此目录,将在此保存ts文件')
except FileNotFoundError:
    os.mkdir(ts_path)
    print('无所指目录,已新建用于保存ts文件')

pre_num = len(os.listdir(ts_path))  # 已下载文件数量
add_var = pre_num
order_list = []     # 后面获取ts顺序
total = 0


def m3u8_parse(path):  # 获取ts的url
    with open(path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            if line.startswith('#'):
                continue
            else:
                ts_url = line.strip()
                yield ts_url


def save_ts(resp):     # 保存ts
    global add_var
    ts_name = resp.url.split('/')[-1]
    with open(f'{ts_path}/{ts_name}', 'wb') as f:
        f.write(resp.body)
    add_var += 1
    progress_bar(total, add_var)      # 显示进度条


class M3u8Spider(scrapy.Spider):
    name = 'm3u8_spider'
    start_urls = m3u8_url

    def parse(self, response, **kwargs):
        # with open(f'{video_name}.m3u8', 'wb') as f:
        #     f.write(response.body)
        print(f'm3u8文件保存在{os.getcwd()}/{video_name}.m3u8')
        # 解析m3u8文件
        global order_list, total
        ts_url_lst = m3u8_parse(f'{video_name}.m3u8')
        order_list = list(ts_url_lst)  # 获取ts的顺序,用于合并
        total = len(order_list)  # ts总数
        print(f'已下载{pre_num}个文件')
        print(f'共{total}个文件')
        for ts_url in ts_url_lst:
            if ts_url.split('/')[-1] in os.listdir(ts_path):  # 去重
                continue
            else:
                yield scrapy.Request(url=ts_url,
                                     method='get',
                                     callback=save_ts
                                     )


def run_spider():
    process = CrawlerProcess(settings={
        'USER_AGENT': 'Mozilla/5.0',
        'ROBOTSTXT_OBEY': False,
        'REQUEST_FINGERPRINTER_IMPLEMENTATION': "2.7",
        'TWISTED_REACTOR': "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
        'FEED_EXPORT_ENCODING': "utf-8",
        'LOG_LEVEL': 'WARNING'
    })
    process.crawl(M3u8Spider)
    process.start()


def save_movie(target_path, method):
    # 合并文件
    if method:      # 是否绝对地址
        os.makedirs('/'.join(target_path.split('/')[:-1]))      # 新建文件夹
        file_gather(ts_path, target_path, order_list)
        print(f'视频保存至{target_path}')
    else:
        file_gather(ts_path, f'D:/movie/{target_path}', order_list)
        print(f'视频保存至默认文件夹 D:/movie/{target_path}')


if __name__ == "__main__":
    run_spider()
    print('下载完成')
    movie_path = input('输入视频保存位置(.mp4):')
    mtd = input('是否为绝对地址(否直接按回车):')
    save_movie(movie_path, mtd)
