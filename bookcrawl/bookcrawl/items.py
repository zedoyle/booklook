# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
class BookcrawlItem(scrapy.Item):
    """
    Part of a trio of objects designed to have data passed to
    by the appropriate spider. Their fields are flushed to
    a JSON-formatted file when their jobs are complete.

    This item is associated with the BookSpider.
    """
    title = scrapy.Field()
    url = scrapy.Field()
    pages = scrapy.Field()
    author = scrapy.Field()

class AmazonSearchItem(scrapy.Item):
    """
    Part of a trio of objects designed to have data passed to
    by the appropriate spider. Their fields are flushed to
    a JSON-formatted file when their jobs are complete.

    This item is associated with the AmazonSpider.
    """
    s_title = scrapy.Field()
    s_url = scrapy.Field()

class AmazonPageItem(scrapy.Item):
    """
    Part of a trio of objects designed to have data passed to
    by the appropriate spider. Their fields are flushed to
    a JSON-formatted file when their jobs are complete.

    This item is associated with the BookSpider.
    """ 
    p_title = scrapy.Field()
    p_author = scrapy.Field()
    p_pages = scrapy.Field()
