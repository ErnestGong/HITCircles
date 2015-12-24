#-*- coding:utf-8 -*-
import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector
from sitemap.items import SitemapItem,SitemapItem1

class MySpider(CrawlSpider):
    name = 'delete'
    allowed_domains = ['today.hit.edu.cn']
    start_urls = ['http://today.hit.edu.cn/depart/14.htm']
    rules = (
        # 提取匹配 'category.php' (但不匹配 'subsection.php') 的链接并跟进链接(没有callback意味着follow默认为True)
        # Rule(LinkExtractor(allow=('news/2015/.*\.htm', 'news/2016/.*\.htm')), callback = 'parse_news', follow = False),
        Rule(LinkExtractor(allow=('depart/\d+\.htm')), callback = 'parse_news',follow=False),
        # 提取匹配 'item.php' 的链接并使用spider的parse_item方法进行分析
        #Rule(LinkExtractor(allow=('item\.php', )), callback='parse_item'),
    )
    def parse_news(self, response):
        sel = Selector(response)
        site = SitemapItem1()
        site["titl"] = 'title'
        site["conten"] = "utf-8"
        site["lin"] = response.url
        return site