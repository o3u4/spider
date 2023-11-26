import scrapy
from sele_spider.request import SeleniumRequest


class LoginSpider(scrapy.Spider):
    name = "sln"
    allowed_domains = ["baidu.com"]
    start_urls = ["http://baidu.com/"]

    def start_requests(self):  # 重写对start_urls的处理
        yield SeleniumRequest(
            url=self.start_urls[0],
            callback=self.parse
        )

    def parse(self, response, **kwargs):
        yield scrapy.Request(
            url=LoginSpider.start_urls[0]
        )
