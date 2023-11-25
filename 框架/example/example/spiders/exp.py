import scrapy
from example.items import ExampleItem


class ExpSpider(scrapy.Spider):
    name = "exp"
    allowed_domains = ["baidu.com"]     # 允许的域名
    start_urls = ["https://www.baidu.com/"]

    def parse(self, response, **kwargs):
        txt = response.text     # 源代码
        lst = response.xpath('example')
        for item in lst:
            elm1 = item.xpath('example').extract_first()    # 提取第一项, 没有返回None
            elm2 = item.xpath('example').extract_first()    # extract()返回列表
            elm3 = item.xpath('example').extract_first()

            # 傻瓜式
            # dic = {
            #     'elm1': elm1,
            #     'elm2': elm2,
            #     'elm3': elm3
            # }

            # 聪明式
            exp_item = ExampleItem()
            exp_item['elm1'] = elm1
            exp_item['elm2'] = elm2
            exp_item['elm3'] = elm3

            #   用yield传数据给管道
            yield exp_item
