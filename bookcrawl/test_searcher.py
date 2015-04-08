#!/usr/bin/python2

import json
import shutil
import sys

from bookcrawl.spiders.bookspider import BookSpider
from bookcrawl.spiders.amazonspider import AmazonSpider
from bookcrawl.assigner import BookAssigner
from scrapy.crawler import Crawler
from scrapy import log, signals
from twisted.internet import reactor, defer
from scrapy.utils.project import get_project_settings

args = sys.argv
if len(args) != 3:
    print("arg failure: "+str(len(args))+" instead of 3")
    sys.exit(1)

d_title = args[1]
d_author = args[2]

if(d_author == None):
    spider = AmazonSpider(d_title)
else:
    spider = AmazonSpider(d_title, d_author)
settings = get_project_settings()
settings.overrides['FEED_FORMAT'] = 'json'
settings.overrides['FEED_URI'] = 'search_result.json' 
crawler = Crawler(settings)
crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
crawler.configure()
crawler.crawl(spider)
crawl_result = crawler.start()
log.start()
reactor.run()
