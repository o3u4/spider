import scrapy


class LogSpider(scrapy.Spider):
    name = "log"
    allowed_domains = ["baidu.com"]
    start_urls = ["http://baidu.com/"]

    def start_requests(self):  # 重写对start_urls的处理
        # cookie_str = 'example'      # cookie字符串
        # lst = cookie_str.split('; ')    # 切割
        # cookie_dic = {}
        # for it in lst:
        #     k, v = it.split('=')
        #     cookie_dic[k.strip()] = v.strip()   # 用字典保存
        #
        # yield scrapy.Request(url=self.start_urls[0],
        #                      headers={'ua': 'ua'},
        #                      cookies=cookie_dic,
        #                      callback=self.parse    # 可不写, 默认为parse
        #                      )

        # 走登录流程
        url = 'url'
        username = 'name'
        password = 'word'
        yield scrapy.Request(
            url=url,
            method='post',
            body=f'loginName={username}&passworf={password}',
            callback=self.parse
        )

    def parse(self, response, **kwargs):
        yield scrapy.Request(
            url=LogSpider.start_urls[0],
            callback=self.parse_detail
        )

    def parse_detail(self, response, **kwargs):
        pass
