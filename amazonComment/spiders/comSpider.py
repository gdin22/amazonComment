import scrapy
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from ..items import AmazoncommentItem

from pymongo import MongoClient
conn = MongoClient('localhost', 27017)
asin = conn.amazon.asin

asinList = [i[0] for i in asin.find_one()['asinToSku'].items()]
asinList = ['B077FFJRV6']

amazonUrl = 'https://www.amazon.com'
"""
爬取评论进行词云分析
"""


class comSpider(scrapy.Spider):
    name = 'comSpider'

    def start_requests(self):  # 用动态生成来生成一批初始链接 与start_urls同样 有这个时 start_urls无效
        pages = []
        for asin in asinList:
            url = 'https://www.amazon.com/dp/%s' % asin
            page = scrapy.Request(url)
            pages.append(page)
        return pages

    def parse(self, response):  # 获取评论区的第一个链接
        try:
            href = response.css('.a-link-emphasis.a-text-bold').xpath('@href')[0].extract()
        except:
            href = response.css('.a-section .a-spacing-large .a-text-bold').xpath('@href')[0].extract()
        commentUrl = urljoin(amazonUrl, href)
        yield scrapy.Request(url=commentUrl, callback=self.getComment)

    def getComment(self, response):  # 在获取第一页评论后 如果有下一页 会继续爬取
        item = AmazoncommentItem()
        item['url'] = response.url
        item['stars'] = response.css('.a-link-normal .review-rating  .a-icon-alt::text').extract()
        commentlist = response.css('.review-text')
        commentLen = len(commentlist)
        commentitem = []
        for i in range(commentLen):
            commentitem.append(''.join(commentlist[i].css('::text').extract()))
        item['comment'] = commentitem
        sizeOrColor = response.css('.a-color-secondary.a-size-mini.a-link-normal::text').extract()
        item['size'] = []
        item['color'] = []

        for eachSizeColor in sizeOrColor:
            if 'color' in eachSizeColor.lower():
                item['color'].append(eachSizeColor)
            else:
                item['size'].append(eachSizeColor)


        colorLen = len(item['color'])
        sizeLen = len(item['size'])

        if commentLen > colorLen:
            item['color'] += ([''] * (commentLen - colorLen))

        if commentLen > sizeLen:
            item['size'] += ([''] * (commentLen - sizeLen))

        yield item
        next_href = response.css('.a-last a').xpath('@href').extract()

        if next_href:
            next_url = urljoin(amazonUrl, next_href[0])
            yield scrapy.Request(url=next_url, callback=self.getComment)
