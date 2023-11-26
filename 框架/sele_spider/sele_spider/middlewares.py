# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
from sele_spider.request import SeleniumRequest
from selenium.webdriver import Chrome
from scrapy.http.response.html import HtmlResponse


class SeleSpiderSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class SeleSpiderDownloaderMiddleware:

    @classmethod
    def from_crawler(cls, crawler):     # 核心

        s = cls()
        # 在xxx时间, 执行xxx功能   有很多功能可实现
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)      # 开启
        crawler.signals.connect(s.spider_opened, signal=signals.spider_closed)      # 关闭

        return s

    def process_request(self, request, spider):  # ua写在这里   可用selenium返回响应
        """
        在引擎将请求交给下载器前, 自动调用方法
        :param request: 当前请求
        :param spider: 发出该请求的spider
        :return:
            1.返回None, 不做拦截, 继续向后的中间件执行
            2.返回Request, 后续不进行, 重新交请求给引擎, 引擎扔给调度器
            3.返回Response, 后续不进行, 把响应交给引擎, 引擎扔给spider, 处理数据
        """
        ua = 'example'
        request.headers['User-Agent'] = ua
        # 所有请求都到这里
        # 需要进行判断, 是否需要用selenium进行处理
        # 开始selenium的操作, 返回页面源代码组装的response
        if isinstance(request, SeleniumRequest):    # 判断是否用selenium操作
            self.web.get(request.url)   # 请求
            page_source = self.web.page_source
            # 要封装响应对象
            return HtmlResponse(url=request.url, status=200,
                                body=page_source, request=request,
                                encoding='utf-8')
        else:
            return None

    def process_response(self, request, response, spider):
        """
        在下载器返回响应准备交给引擎前, 自动调用方法
        :param request: 当前请求
        :param response: 响应内容
        :param spider: 发出该请求的spider
        :return:
            1.request 直接把请求给引擎, 丢给调度器
            2.response 不做拦截, 继续向前进行提交返回
        """
        return response

    def spider_opened(self, spider):    # 在这里提前建好浏览器, 完成登录等操作
        self.web = Chrome()

    def spider_closed(self, spider):    # 在这里提前建好浏览器
        self.web.close()    # 关闭浏览器
