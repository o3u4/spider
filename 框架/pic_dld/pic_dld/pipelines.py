# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline


class PicDldPipeline:
    def process_item(self, item, spider):
        # 存数据
        return item


# 用ImagesPipeline需要单独配置, 用来保存文件的文件夹
class SavePipeline(ImagesPipeline):     # 图片管道完成下载

    def get_media_requests(self, item, info):   # 负责下载
        return scrapy.Request(item['src'])      # 返回请求

    def file_path(self, request, response=None, info=None, *, item=None):   # 准备路径
        file_name = request.url.split('/')[-1]      # request.url获取到刚请求的url
        return f'img{file_name}'    # 返回路径

    def item_completed(self, results, item, info):  # 返回详细信息
        ok, pic_info = results[0]
        path = pic_info['path']
        print(results)
        print(path)
