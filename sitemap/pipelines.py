#-*- coding:utf-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from twisted.enterprise import adbapi
from scrapy.exceptions import DropItem
import MySQLdb  
import MySQLdb.cursors
class ExamplePipeline(object):
    def __init__(self):
        self.dbpool = adbapi.ConnectionPool('MySQLdb',  
            db = 'hitcircles',  
            user = 'hitc_django', 
            passwd = 'jowei*$3gj',  
            cursorclass = MySQLdb.cursors.DictCursor,  
            charset = 'utf8',  
            use_unicode = True 
            )
    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self._conditional_insert, item)  
        return item
    def _conditional_insert(self, tx, item):
        if item.get('titl'):
            tx.execute('delete from hitcircles_web')
            tx.execute('delete from hitcircles_web1')
        if item.get('title'):
                tx.execute('insert into hitcircles_web values (%s, %s, %s, %s)', ('1', item['title'],item['link'],item['content']))
        if item.get('title1'):
                tx.execute('insert into hitcircles_web1 values (%s, %s, %s, %s)', ('1', item['title1'],item['link1'],item['content1']))
#             tx.execute('insert into web values (%s, %s, %s)', ("http://today.hit.edu.cn"+item['link'], item['title'],item['content']))