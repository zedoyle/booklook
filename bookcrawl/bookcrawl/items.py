# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class BookcrawlItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    pages = scrapy.Field()
    author = scrapy.Field()

class AmazonSearchItem(scrapy.Item):
    s_title = scrapy.Field()
    s_url = scrapy.Field()

class AmazonPageItem(scrapy.Item):
    p_title = scrapy.Field()
    p_author = scrapy.Field()
    p_pages = scrapy.Field()
