#!/usr/bin/python2

from bookcrawl.spiders.bookspider import BookSpider
from bookcrawl.spiders.amazonspider import AmazonSpider
from bookcrawl.assigner import BookAssigner
from scrapy.crawler import Crawler
from scrapy import log, signals
from twisted.internet import reactor
from scrapy.utils.project import get_project_settings

def google_assignments_at(assignment_location):
    assigner = BookAssigner(assignment_location)
    assignments = assigner.assignment_iterator()
    for task in assignments:
        spider = BookSpider(target_info_array=task)
        settings = get_project_settings()
        settings.overrides['FEED_FORMAT'] = 'json'
        settings.overrides['FEED_URI'] = 'google_result.json' 
        crawler = Crawler(settings)
        crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
        crawler.configure()
        crawler.crawl(spider)
        crawler.start()
        log.start()
        reactor.run()
