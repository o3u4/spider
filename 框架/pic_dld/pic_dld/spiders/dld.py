import scrapy
from pic_dld.items import PicDldItem


class DldSpider(scrapy.Spider):
    name = "dld"
    allowed_domains = ["baidu.com"]
    start_urls = ["https://www.baidu.com/"]

    def parse(self, resp, **kwargs):
        li_lst = resp.xpath('example')
        for li in li_lst:
            href = li.xpath('example').extract_first()
            scrapy.Request(
                url=resp.urljoin(href),      # 拼接url
                method='get',
                callback=self.parse_detail
            )
        # 考虑下一页
        button_href = resp.xpath('example/@href').extract_first()
        if button_href:
            yield scrapy.Request(
                url=resp.urljoin(button_href),
                callback=self.parse     # 循环调用
            )

    def parse_detail(self, resp, **kwargs):
        name = resp.xpath('example').extract_first()
        img_src = resp.xpath('example').extract_first()
        item = PicDldItem()
        item['name'] = name
        item['img_src'] = img_src

        yield item
