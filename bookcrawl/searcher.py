#!/usr/bin/python2

import json
import shutil

from bookcrawl.spiders.bookspider import BookSpider
from bookcrawl.spiders.amazonspider import AmazonSpider
from bookcrawl.assigner import BookAssigner
from scrapy.crawler import Crawler
from scrapy import log, signals
from twisted.internet import reactor, defer
from scrapy.utils.project import get_project_settings


def announce_completion(data):
    print "done"

def search_amazon_for(d_title, d_author=None):
    if(d_author == None):
        spider = AmazonSpider(d_title)
    else:
        spider = AmazonSpider(d_title, author=d_author)
    settings = get_project_settings()
    settings.overrides['FEED_FORMAT'] = 'json'
    settings.overrides['FEED_URI'] = 'search_result.json' 
    crawler = Crawler(settings)
    crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
    crawler.configure()
    crawler.crawl(spider)
    crawl_result = crawler.start()
    crawl_result.addCallback(announce_completion)
    log.start()
    reactor.run()
