import requests
from bs4 import BeautifulSoup
import re
from pymongo import MongoClient
import os


class Asin2asin(object):
    """
    这个类用于将子asin转换为母asin
    在类中写入 子asin
    调用getNasub方法 返回母asin
    """
    def __init__(self, asin):
        asinurl = 'https://www.amazon.com/dp/'
        self.asin = asin
        self.url = os.path.join(asinurl, self.asin)
        self.headers = r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'

    def gethtml(self):
        try:
            html = requests.get(self.url, headers=self.headers)
            html.encoding = html.apparent_encoding
            return html.text
        except:
            pass

    def getMasin(self):
        htmltext = self.gethtml()
        try:
            masin = re.findall('>[0-9A-Z]{10}<', htmltext)[0][1:-1]
            return masin
        except:
            pass
