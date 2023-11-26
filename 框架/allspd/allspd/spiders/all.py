import scrapy
from scrapy.linkextractors import LinkExtractor


class AllSpider(scrapy.Spider):
    name = "all"
    allowed_domains = ["baidu.com"]
    start_urls = ["http://baidu.com/"]

    def parse(self, response, **kwargs):
        le = LinkExtractor(restrict_xpaths=('example_xpath',))  # 参数给元组
        links = le.extract_links(response)  # 提取链接
        for link in links:
            print(link.text.replace(' ', ''), link.url)  # link.url不用拼接
            yield scrapy.Request(
                url=link.url,
                callback=self.parse_detail
            )
        # 开始翻页
        page_le = LinkExtractor(restrict_xpaths=('example_xpath',))
        page_links = page_le.extract_links(response)     # 分页url
        for page in page_links:
            yield scrapy.Request(
                url=page.url,
                # dont_filter=True,   # 不过滤
                callback=self.parse
            )

    def parse_detail(self, response, **kwargs):
        pass
