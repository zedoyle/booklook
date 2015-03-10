# -*- coding: utf-8 -*-
import scrapy
import urllib
import re
import sys

from bookcrawl.items import BookcrawlItem
from bookcrawl.assigner import BookAssigner
from PyPDF2 import PdfFileReader
from PyPDF2.pdf import DocumentInformation
from scrapy import log, signals
from PyPDF2.utils import PdfReadError

class BookSpider(scrapy.Spider):
    tia = ["","","",""]
    name = "bookspider"
    allowed_domains = ["google.com"]
    outer_querystring = "http://www.google.com"
    
    target_type=""
    target_title=""
    target_author=""
    target_pages=-35

    def __init__(self, target_info_array=None, *args, **kwargs):
        super(BookSpider, self).__init__(*args, **kwargs)
        #sys.exit()
        self.tia = target_info_array
        self.target_type = self.tia[0]
        self.target_title = self.tia[1]
        self.target_author = self.tia[2]
        try:
            self.target_pages = int(self.tia[3])
        except ValueError:
            self.target_pages = -30
        self.outer_querystring=("http://www.google.com/search?q=filetype:"+self.target_type+"+"+self.target_title+"+"+self.target_author) 
        self.start_urls = (
            'http://www.google.com',
            self.outer_querystring
        )

    def parse(self, response):
        for result in response.xpath('//h3/a'):
            print result
            link = BookcrawlItem()
            link['title'] = ""
            link['author'] = ""
            link['pages'] = -30
            possible_title = result.xpath('text()').extract()
            xpath_url = result.xpath('@href').extract()
            link['url'] = re.search('http.*\.'+self.target_type, xpath_url[0]).group(0)
            #log.msg("Presumed URL: "+link['url']+"Expected filetype: "+self.target_type, level=log.INFO)
            urllib.urlretrieve(link['url'], "file."+self.target_type)
            if(self.target_type == "pdf"):
	        try:
                    reader = PdfFileReader(open("file."+self.target_type,"rb"))
                    fileinfo = reader.getDocumentInfo()
                    link['title'] = fileinfo.title
                    link['pages'] = reader.getNumPages()
                    link['author'] = fileinfo.author
                except PdfReadError:
                    log.msg("error reading PDF at ["+link['url']+"]",level=log.INFO)
                    yield None
            log.msg("done reading PDF at ["+link['url']+"]",level=log.INFO)
            nomatch = True
            try:
                log.msg("title: "+str(link['title']), level=log.INFO)
                if(self.target_title.replace("+"," ") in link['title']):
                    log.msg("---> title matches!", level=log.INFO)
                    nomatch = False
                    yield link
            except (TypeError, UnicodeEncodeError):
                pass
            try:
                log.msg("author: "+str(link['author']), level=log.INFO)
                if(self.target_author.replace("+"," ") in link['author']):
                    log.msg("---> author matches!", level=log.INFO)
                    nomatch = False
                    yield link
            except (TypeError, UnicodeEncodeError):
                pass
            log.msg(str(link['pages'])+" pages long")
            if(link['pages'] < self.target_pages+30 and link['pages'] > self.target_pages-30):
                log.msg("---> pagecount matches!", level=log.INFO)
                nomatch = False
                yield link
            if(nomatch):
                log.msg("---> no match.",level=log.INFO)
                yield None
