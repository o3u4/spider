# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ExampleItem(scrapy.Item):

    elm1 = scrapy.Field()   # 相当于字典的key
    elm2 = scrapy.Field()
    elm3 = scrapy.Field()

    pass
