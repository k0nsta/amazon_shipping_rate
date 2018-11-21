# -*- coding: utf-8 -*-
import time

import scrapy
from scrapy_splash import SplashRequest
from scrapy.linkextractors import LinkExtractor
from scrapy.loader.processors import Compose, TakeFirst

from de_uk_fr_shipping.items import AmazonItemLoader
from de_uk_fr_shipping.helpers import get_from_proxyrotator
from de_uk_fr_shipping.helpers import format_price

from de_uk_fr_shipping.lua import DE_SHIPPING, LOAD_PAGE
from de_uk_fr_shipping.cookies import DE_COOKIE, DE_HEADERS


class AmzDeItemLoader(AmazonItemLoader):
    description_out = Compose(TakeFirst(), lambda x: x.strip())
    price_out = Compose(TakeFirst(), format_price)
    shipping_rate_out = Compose(TakeFirst(), format_price)


class AmazonDeSpider(scrapy.Spider):
    name = 'amazon.de'
    allowed_domains = ['amazon.de']

    lx_products = LinkExtractor(
        restrict_css='#resultsCol', deny=[r'(b|B)estseller', r'.*(r|R)eviews.*', r'deal_dot.*']
    )

    # def start_requests(self):
    #     start_urls = ['https://www.amazon.de/s?marketplaceID=A1PA6795UKMFR9&me=A3C99XFET32HI1&merchant=A3C99XFET32HI1&redirect=true']
    #     for url in start_urls:
    #         yield SplashRequest(
    #             url, self.parse_result, endpoint='execute',
    #             args={'lua_source': LOAD_PAGE},
    #         )

    # def parse_result(self, response):
    #     for l in self.lx_products.extract_links(response):
    #         proxy = get_from_proxyrotator()
    #         # print('URL :', url)
    #         self.logger.info('Parse url : {}'.format(l.url))
    #         self.logger.info('Proxy: {}'.format(proxy))
    #         # time.sleep(5)
    #         yield SplashRequest(
    #             l.url, self.parse, endpoint='execute',
    #             args={
    #                 'lua_source': DE_SHIPPING, 'proxy': proxy, 'images': 0, 'timeout': 90, 'wait': 2
    #             },
    #         )

    #     pagination_links = response.css('#pagn.pagnHy span.pagnLink a::attr(href)')
    #     if pagination_links:
    #         for l in pagination_links:
    #             yield response.follow(l, self.parse_result)

    def start_requests(self):
        start_urls = ['https://www.amazon.de/s?marketplaceID=A1PA6795UKMFR9&me=A3C99XFET32HI1&merchant=A3C99XFET32HI1&redirect=true']
        for url in start_urls:
            yield scrapy.Request(
                url, self.parse_result,
                headers=DE_HEADERS, meta={'dont_merge_cookies': True}
            )

    def parse_result(self, response):
        # links_amount = len(self.lx_products.extract_links(response))
        for l in self.lx_products.extract_links(response):
            self.logger.info('Parse url : {}'.format(l.url))
            yield scrapy.Request(
                l.url, self.parse,
                headers=DE_HEADERS, meta={'proxy': get_from_proxyrotator(), 'dont_merge_cookies': True}
            )

        # pagination_links = response.css('#pagn.pagnHy span.pagnLink a::attr(href)')
        # if pagination_links:
        #     for l in pagination_links:
                # link = response.urljoin(l)
        next_page = response.css('#pagnNextLink.pagnNext::attr(href)').extract_first()
        if next_page is not None:
            yield response.follow(
                next_page, self.parse_result,
                headers=DE_HEADERS, meta={'dont_merge_cookies': True}
            )

    def parse(self, response):
        l = AmazonItemLoader(response=response)
        l.add_value('url', response.url)
        l.add_css('asin', '#prodDetails div.column.col2 td.value::text')
        l.add_css('description', '#productTitle.a-size-large::text')
        l.add_css('price', '#priceblock_ourprice_row td.a-span12 span#priceblock_ourprice::text')
        l.add_css('shipping_rate', '#soldByThirdParty span.a-size-small::text')
        return l.load_item()
