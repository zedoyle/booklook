#!/usr/bin/python2

import json
import shutil
import sys

from bookcrawl.spiders.pagespider import PageSpider
from bookcrawl.assigner import BookAssigner
from scrapy.crawler import Crawler
from scrapy import log, signals
from twisted.internet import reactor, defer
from scrapy.utils.project import get_project_settings

args = sys.argv
if len(args) != 2:
    print("arg failure: expected one url param")
    sys.exit(1)

p_urls = [args[1]]

spider = PageSpider(p_urls)
settings = get_project_settings()
settings.overrides['FEED_FORMAT'] = 'json'
settings.overrides['FEED_URI'] = 'page_result.json' 
crawler = Crawler(settings)
crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
crawler.configure()
crawler.crawl(spider)
crawl_result = crawler.start()
log.start()
reactor.run()
