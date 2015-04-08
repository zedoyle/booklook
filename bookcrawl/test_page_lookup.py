#!/usr/bin/python2

import json
import shutil

from bookcrawl.spiders.pagespider import PageSpider
from bookcrawl.assigner import BookAssigner
from scrapy.crawler import Crawler
from scrapy import log, signals
from twisted.internet import reactor, defer
from scrapy.utils.project import get_project_settings


def announce_completion(data):
    print "done"

def lookup_pages_by_urls(p_urls):
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


def main():
    lookup_pages_by_urls(["http://www.amazon.com/Computer-Networks-5th-Andrew-Tanenbaum/dp/0132126958"])

if __name__ == "__main__":
    main()
