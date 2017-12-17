# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re

class CorpusPipeline(object):
    # Method which tries to remove HTML tags from text
    def remove_tags(whocares, string):
        string = re.sub('<[^<]+?>', ' ', string)
        return string

    def process_item(self, item, spider):
        if 'title' in item:
            print item.get('title')
            item['title'] = self.remove_tags(item.get('title'))
            item['body'] = self.remove_tags(item.get('body'))
        return item
