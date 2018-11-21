# -*- coding: utf-8 -*-
from scrapy.exceptions import DropItem

# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class AsinUniqueFilterPipeline(object):

    def __init__(self):
        self.asin_seen = set()

    def process_item(self, item, spider):
        if item.get('asin'):
            if item.get('asin') in self.asin_seen:
                raise DropItem('Duplicate ASIN found: %s' % item)
            self.asin_seen.add(item.get('asin'))
        return item
