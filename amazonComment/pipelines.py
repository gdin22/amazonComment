# -*- coding: utf-8 -*-
import pymongo
from scrapy.conf import settings
import re


# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class AmazoncommentPipeline(object):
    def process_item(self, item, spider):
        return item


# 项目管道 在settings开启使用 在每次返回item后对item进行处理入库
class saveCommentPipeline(object):
    def __init__(self):
        self.client = pymongo.MongoClient(host=settings['MONGO_HOST'])
        self.db = self.client[settings['MONGO_DB']]
        self.coll = self.db[settings['MONGO_COLL']]

    def process_item(self, item, spider):
        asin = re.findall('[A-Z0-9]{10}', item['url'])[0]
        colors = [i.split(':')[-1].strip() for i in item['color']]
        comments = item['comment']
        sizes = [i.split(':')[-1].strip() for i in item['size']]
        stars = [float(i.split(' ')[0]) for i in item['stars']]
        dictList = [{'asin': asin, 'color': color, 'comment': comment, 'size': size, 'star': star} for color, comment,
                    size, star in zip(colors, comments, sizes, stars)]
        for dict in dictList:
            self.coll.insert(dict)
        return item
