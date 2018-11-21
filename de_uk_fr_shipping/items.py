# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
import six

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Compose, TakeFirst


class DeUkFrShippingItem(scrapy.Item):
    # define the fields for your item here like:
    url = scrapy.Field()
    description = scrapy.Field()
    asin = scrapy.Field()
    price = scrapy.Field()
    shipping_rate = scrapy.Field()


class AmazonItemLoader(ItemLoader):
    default_item_class = DeUkFrShippingItem
    default_output_processor = Compose(TakeFirst(), six.text_type, six.text_type.strip)

