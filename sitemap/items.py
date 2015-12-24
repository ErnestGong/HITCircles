#-*- coding:utf-8 -*-
# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class SitemapItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    link = scrapy.Field()
    content = scrapy.Field()
class SitemapItem1(scrapy.Item):
    titl = scrapy.Field()
    lin = scrapy.Field()
    conten = scrapy.Field()
class SitemapItem2(scrapy.Item):
    title1 = scrapy.Field()
    link1 = scrapy.Field()
    content1 = scrapy.Field()
