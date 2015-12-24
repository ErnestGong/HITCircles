#-*- coding:utf-8 -*-
import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector
from sitemap.items import SitemapItem

class MySpider(CrawlSpider):
    name = 'bs'
    allowed_domains = ['today.hit.edu.cn']
    start_urls = ['http://today.hit.edu.cn/depart/26.htm']
    rules = (
        # 提取匹配 'category.php' (但不匹配 'subsection.php') 的链接并跟进链接(没有callback意味着follow默认为True)
        Rule(LinkExtractor(allow=('news/2015/.*\.htm', 'news/2016/.*\.htm')), callback = 'parse_news', follow = False),
        Rule(LinkExtractor(allow=('depart/\d+\.htm')), callback = 'parse_1',follow=False),
        # 提取匹配 'item.php' 的链接并使用spider的parse_item方法进行分析
        #Rule(LinkExtractor(allow=('item\.php', )), callback='parse_item'),
    )
    def parse_news(self, response):
        sel = Selector(response)
        title = sel.xpath("//div[@class='articleTitle']/text()").extract()
        content = sel.xpath("//div[@class='articletext']").extract()
        site = SitemapItem()
        site["title"] = title
        site["content"] = content[0].encode("utf-8")
        site["link"] = response.url
        return site
        
    def parse_1(self, response):
        pass