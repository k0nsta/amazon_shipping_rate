# -*- coding: utf-8 -*-
import scrapy


class AmazonFrSpider(scrapy.Spider):
    name = 'amazon.fr'
    allowed_domains = ['amazon.fr']
    start_urls = ['http://amazon.fr/']

    def parse(self, response):
        pass
