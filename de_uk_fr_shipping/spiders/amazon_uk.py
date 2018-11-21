# -*- coding: utf-8 -*-
import scrapy


class AmazonUkSpider(scrapy.Spider):
    name = 'amazon.uk'
    allowed_domains = ['amazon.uk']
    start_urls = ['http://amazon.uk/']

    def parse(self, response):
        pass
