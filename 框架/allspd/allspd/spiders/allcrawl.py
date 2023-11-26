import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class AllcrawlSpider(CrawlSpider):
    name = "allcrawl"
    allowed_domains = ["baidu.com"]
    start_urls = ["http://baidu.com/"]

    rules = (   # 定义规则, 元组或列表
        Rule(LinkExtractor(restrict_xpaths=('example',)), callback="parse_item", follow=False),
        # follow是否在下一层链接继续执行该操作
        Rule(LinkExtractor(restrict_xpaths=('example2',)), follow=True)     # callback可没有
    )
    # 不能写parse, 由CrawlSpider提供

    def parse_item(self, response):
        # 处理数据
        pass
