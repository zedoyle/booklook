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
    """A spider to grab information on book PDFs from a trimmed google search using the Scrapy webcrawler API.
	
	Initialized with an array of author, title, and page info the search for, a method of page count
	comparison, and a permitted error in page count, to account for padding/omissions from some PDFs.
    """
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
        """
		Initializes the crawler by taking an untyped array of info [name,author,pagecount] 
		regarding the target book and transforming it into a google search string (and then
		appending to that until it is a valid request URL).
        """
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
        """
        	Parses an HTTP response from google. Minimal functionality is to download all valid PDFs
		that were returned in the first page of search results. Optimal functionality (currently
		functional, but disabled for time/space reasons) is to examine the PDF after downloading
		it, extract header info detailing whether or not the thing has the correct author/page count,
		and then return it. In either case, successes are returned in json format in 'google_results.json'.
        """
        for result in response.xpath('//h3/a'):
            link = BookcrawlItem()
            link['title'] = ""
            link['author'] = ""
            link['pages'] = 0
            possible_title = result.xpath('text()').extract()
            link['title'] = possible_title
            xpath_url = result.xpath('@href').extract()
            try:
                    link['url'] = re.search('http.*\.'+self.target_type, xpath_url[0]).group(0)
                    filename = link['url'].split('/')[-1]
                    req = requests.get(link['url'])
                    yield link
            except AttributeError:
                    yield None
            #with open(filename, 'wb') as handle:
            #    if not req.ok:
            #        log.msg("error requesting PDF")
            #        yield None
            #    else:
            #        for block in req.iter_content(1024):
            #            if not block:
            #                print "empty block, done writing"
            #                break
            #            print "writing block..."
            #            handle.write(block) 
            #if(self.target_type == "pdf"):
	    #    try:
            #        try:
            #            reader = PdfFileReader(open(filename,"rb"))	
            #            fileinfo = reader.getDocumentInfo()
            #            link['title'] = fileinfo.title
            #            link['pages'] = reader.getNumPages()
            #            link['author'] = fileinfo.author
            #        except IOError as problem:
            #            log.msg(str(problem))
            #    except PdfReadError as pdferror:
            #        if(str(pdferror)=="EOF marker not found"):
            #            log.msg("PDF too long for parser, likely textbook.")
            #            nomatch = False
            #            yield link
            #        else:
            #            log.msg("error reading PDF: "+str(pdferror),level=log.INFO)
            #            yield None
            #log.msg("done reading PDF at ["+link['url']+"]",level=log.INFO)
            #nomatch = True
            #try:
            #    log.msg("title: "+str(link['title']), level=log.INFO)
            #    if(self.target_title.replace("+"," ") in link['title']):
            #        log.msg("---> title matches!", level=log.INFO)
            #        nomatch = False
            #        yield link
            #except (TypeError, UnicodeEncodeError):
            #    pass
            #try:
            #    log.msg("author: "+str(link['author']), level=log.INFO)
            #    if(self.target_author.replace("+"," ") in link['author']):
            #        log.msg("---> author matches!", level=log.INFO)
            #        nomatch = False
            #        yield link
            #except (TypeError, UnicodeEncodeError):
            #    pass
            #gotpages = True
            #if(link['pages'] != -30):
            #    log.msg(str(link['pages'])+" pages long")
            #else:
            #    log.msg("Unable to get page count")
            #log.msg("filesize: "+str(os.stat(filename).st_size/1024) + "K")
            #if(self.target_pages == -30):
            #    log.msg("---> no desired pagecount specified; grabbing all results")
            #    nomatch = False
            #    yield link
            #if(self.compmode == "equals"):
            #    if(link['pages'] < self.target_pages+30 and link['pages'] > self.target_pages-30):
            #        log.msg("---> pagecount matches!", level=log.INFO)
            #        nomatch = False
            #        yield link
            #if(nomatch):
            #    log.msg("---> no match.",level=log.INFO)
            #    yield None
