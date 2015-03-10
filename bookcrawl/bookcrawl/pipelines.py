# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy import log,signals
from scrapy.contrib.exporter import JsonItemExporter
from scrapy.xlib.pydispatch import dispatcher

class BookcrawlPipeline(object):

    def __init__(self):
        self.files = {}
        dispatcher.connect(self.spider_opened , signals.spider_opened)
        dispatcher.connect(self.spider_closed , signals.spider_closed)

    def spider_opened(self,spider):
        file = open('links_pipelines.json' ,'wb')
        self.files[spider] = file
        self.exporter = JsonItemExporter(file)
        self.exporter.start_exporting()

    def spider_closed(self,spider):
       self.exporter.finish_exporting()
       file = self.files.pop(spider)
       file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        log.msg('It reached here')
        return item
