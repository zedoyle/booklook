# -*- coding: utf-8 -*-
import scrapy

from scrapy import log, signals
from bookcrawl.items import AmazonSearchItem

amazon_book_search_base_string = "http://www.amazon.com/s/ref=nb_sb_noss_2?url=search-alias%3Dstripbooks&field-keywords="

class AmazonSpider(scrapy.Spider):
    name = "amazonspider"
    target_title = ""
    target_author = ""
    
    allowed_domains = ["amazon.com"]

    def __init__(self, title="computer networks", author="andrew tanenbaum",*args, **kwargs):
        super(AmazonSpider, self).__init__(*args, **kwargs)
        self.target_title = title.replace(" ","+")
        if(author != None):
            self.target_author = str(author).replace(" ","+")
        
        self.query_string = amazon_book_search_base_string+self.target_title
        if(author != ""):
            self.query_string = self.query_string+"+"+self.target_author
        log.msg("query string: "+self.query_string)
        self.start_urls = (
            'http://www.amazon.com',
            self.query_string
        )

    def parse(self, response):
        results = response.xpath('//li/div/div/div/div/div/a') 
        try:
            result = results[0]
        except IndexError:
            return None
        log.msg("found result: "+str(result),level=log.INFO)
        link = AmazonSearchItem()
        link['s_title'] = result.xpath('//h2/text()').extract()[1]
        link['s_url'] = result.xpath('@href').extract()[0]
        return link
