# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.loader.processors import Compose, TakeFirst

from de_uk_fr_shipping.items import AmazonItemLoader
from de_uk_fr_shipping.helpers import get_from_proxyrotator
from de_uk_fr_shipping.helpers import format_price

from de_uk_fr_shipping.constants import DE_INIT_URL, DE_HEADERS


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

    def start_requests(self):
        # start_urls = []
        # for url in start_urls:
            yield scrapy.Request(
                DE_INIT_URL, self.parse_result,
                headers=DE_HEADERS, meta={'dont_merge_cookies': True}
            )

    def parse_result(self, response):
        for l in self.lx_products.extract_links(response):
            self.logger.info('Parse url : {}'.format(l.url))
            yield scrapy.Request(
                l.url, self.parse,
                headers=DE_HEADERS, meta={'proxy': get_from_proxyrotator(), 'dont_merge_cookies': True}
            )

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
