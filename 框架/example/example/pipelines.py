# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class ExamplePipeline:      # settings启动管道

    def open_spider(self, spider):
        self.f = open('./exp.csv', mode='a', encoding='utf-8')  # 模式为a追加, 不能w
        print('开始爬虫')

    def close_spider(self, spider):
        if self.f:
            self.f.close()
        print('结束')

    def process_item(self, item, spider):   # 处理数据
        print(item)
        self.f.write('....')
        return item     # return到下一个管道
