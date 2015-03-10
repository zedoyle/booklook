#!/usr/bin/python2

from bookcrawl.spiders.bookspider import BookSpider
from bookcrawl.assigner import BookAssigner
from scrapy.crawler import Crawler
from scrapy import log, signals
from twisted.internet import reactor
from scrapy.utils.project import get_project_settings

assigner = BookAssigner("assignments.txt")
assignments = assigner.assignment_iterator()
for task in assignments:
    spider = BookSpider(target_info_array=task)
    #log_settings = {'LOG_ENABLED': True, 'ITEM_PIPELINES': 'bookcrawl.pipelines.BookcrawlPipeline'}   
    settings = get_project_settings()
    #settings.overrides.update(log_settings)
    settings.overrides['FEED_FORMAT'] = 'json'
    settings.overrides['FEED_URI'] = 'result.json' 
    crawler = Crawler(settings)
    #crawler.install()
    #crawler.configure()
    crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
    crawler.configure()
    crawler.crawl(spider)
    crawler.start()
    log.start()
    reactor.run()
