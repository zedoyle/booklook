# -*- coding: utf-8 -*-
import scrapy
from bookcrawl.items import AmazonPageItem
from scrapy import log, signals

class PageSpider(scrapy.Spider):
    name = "pagespider"
    allowed_domains = ["amazon.com"]
    start_urls = ()

    def __init__(self, passed_urls=(), *args, **kwargs):
		super(PageSpider, self).__init__(*args, **kwargs)
		self.start_urls = passed_urls

    def parse(self, response):
		pageinfo = AmazonPageItem()
		try:
			result = response.xpath('//td/div/ul/li')
		except IndexError:
			log.msg("NO RESULTS FOUND")
			return None
		log.msg("Length of the thing: "+str(len(result)))
		for res in result:
			text = res.xpath('text()').extract()[0]
			log.msg(text)
			if "pages" in text:
				pageinfo['p_pages'] = text
		return pageinfo
		
