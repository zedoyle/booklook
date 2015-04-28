# -*- coding: utf-8 -*-
import scrapy

from scrapy import log, signals
from bookcrawl.items import AmazonSearchItem

amazon_book_search_base_string = "http://www.amazon.com/s/ref=nb_sb_noss_2?url=search-alias%3Dstripbooks&field-keywords="

class AmazonSpider(scrapy.Spider):
    """
       A relatively simple spider that searches Amazon.com for a product page matching the supplied
       initialization parameters (see below). Intended to be run first in a pseudopipeline to get
       more accurate information on a book where the page count is not known.
    """
    name = "amazonspider"
    target_title = ""
    target_author = ""
    
    allowed_domains = ["amazon.com"]

    def __init__(self, title=None, author=None,*args, **kwargs):
        """
        In addition to the standard command line arguments, initializing an AmazonSpider permits passing
        a title and author to the spider; functionally these arguments are treated the same and are both
        passed to the amazon.com search query string. Because this is intended to GET the page number, 
        it cannot be passed as a parameter.
        """
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
        """
        AmazonSpider's parse function is fairly simple; from a response body (which should always be
        an amazon.com search response page), it pulls out the first apparently list item that seems
        to be a link to an amazon.com product page. It then spits this out in amazon_result.json.
        """
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
