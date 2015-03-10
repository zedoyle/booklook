# -*- coding: utf-8 -*-
import scrapy

from bookcrawl.items import BookcrawlItem

class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["google.com"]

    def grab_urls(self, filepath):
        urlfile = open('filepath','r')
	for line in urlfile:
        

    start_urls = (
        'http://www.google.com',
        'http://www.google.com/search?q=filetype:pdf+isaac+asimov+foundation',
    )

    def parse(self, response):
        for result in response.xpath('//h3/a'):
            print result
            link = BookcrawlItem()
            link['title'] = result.xpath('text()').extract()
            link['url'] = result.xpath('@href').extract()
            yield link
