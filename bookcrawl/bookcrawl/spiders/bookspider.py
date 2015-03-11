# -*- coding: utf-8 -*-
import scrapy
import requests
import re
import sys
import os

from bookcrawl.items import BookcrawlItem
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
    target_pages=-30

    compmode="equals"

    def __init__(self, target_info_array=None, page_count_mode="equals", page_count_fuzziness=10, *args, **kwargs):
        super(BookSpider, self).__init__(*args, **kwargs)
        self.tia = target_info_array
        self.target_type = self.tia[0]
        self.target_title = self.tia[1]
        self.target_author = self.tia[2]
        try:
            self.target_pages = int(self.tia[3])
        except ValueError:
            self.target_pages = -30
        self.outer_querystring=("http://www.google.com/search?q=filetype:"+self.target_type+"+\""+self.target_title+"\"+\""+self.target_author+"\"") 
        self.start_urls = (
            'http://www.google.com',
            self.outer_querystring
        )
        self.compmode=page_count_mode

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
            filename = link['url'].split('/')[-1]
            req = requests.get(link['url'])
            with open(filename, 'wb') as handle:
                if not req.ok:
                    log.msg("error requesting PDF")
                    yield None
                else:
                    for block in req.iter_content(1024):
                        if not block:
                            break
                        print "writing block..."
                        handle.write(block) 
            if(self.target_type == "pdf"):
	        try:
                    reader = PdfFileReader(open(filename,"rb"))
                    fileinfo = reader.getDocumentInfo()
                    link['title'] = fileinfo.title
                    link['pages'] = reader.getNumPages()
                    link['author'] = fileinfo.author
                except PdfReadError as pdferror:
                    if(str(pdferror)=="EOF marker not found"):
                        log.msg("PDF too long for parser, likely textbook.")
                        nomatch = False
                        yield link
                    else:
                        log.msg("error reading PDF: "+str(pdferror),level=log.INFO)
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
            gotpages = True
            if(link['pages'] != -30):
                log.msg(str(link['pages'])+" pages long")
            else:
                log.msg("Unable to get page count")
            log.msg("filesize: "+str(os.stat(filename).st_size/1024) + "K")
            if(self.target_pages == -30):
                log.msg("---> no desired pagecount specified; grabbing all results")
                nomatch = False
                yield link
            if(self.compmode == "equals"):
                if(link['pages'] < self.target_pages+30 and link['pages'] > self.target_pages-30):
                    log.msg("---> pagecount matches!", level=log.INFO)
                    nomatch = False
                    yield link
            if(nomatch):
                log.msg("---> no match.",level=log.INFO)
                yield None
