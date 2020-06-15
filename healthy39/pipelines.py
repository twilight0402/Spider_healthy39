# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from healthy39.utils.util import saveItems
from healthy39.utils.util import printMsg


class Healthy39Pipeline(object):
    def __init__(self):
        pass

    def process_item(self, item, spider):
        printMsg(f"#### 保存item: {item['diseaseName']}", True)
        saveItems(item)
        return item
