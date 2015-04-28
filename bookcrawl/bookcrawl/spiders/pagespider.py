# -*- coding: utf-8 -*-
import scrapy
from bookcrawl.items import AmazonPageItem
from scrapy import log, signals

class PageSpider(scrapy.Spider):
    """
       The simplest of the three spiders, PageSpider exists only to parse information from
       an Amazon.com product page- specifically, page count. As it turns out, Amazon.com is
       by far the easiest-to-access authoritative source on the page counts of different
       editions of books- especially textbooks.
    """
    name = "pagespider"
    allowed_domains = ["amazon.com"]
    start_urls = ()

    def __init__(self, passed_urls=(), *args, **kwargs):
        """
	   Calls the generic spider constructor and passes the only parameter, a list
	   of Amazon.com product page URLs, to the spider itself.
        """
	super(PageSpider, self).__init__(*args, **kwargs)
	self.start_urls = passed_urls

    def parse(self, response):
	"""
	   Looks for a list item inside an unordered list inside a table whose text
	   mentions the word 'page'; the first occurance of which always contains
	   the page count. 
	"""	
	pageinfo = AmazonPageItem()
	try:
		result = response.xpath('//td/div/ul/li')
	except IndexError:
		log.msg("NO RESULTS FOUND")
		return None
	for res in result:
		text = res.xpath('text()').extract()[0]
		if "pages" in text:
			pageinfo['p_pages'] = text
	return pageinfo
		
