# -*- coding: utf-8 -*-
import requests
import logging
import time

from scrapy import Selector

from proxy_pool.setting import Setting as config
from proxy_pool.database.redis_man import Redis

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.6 Safari/537.36'
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def xpath(response, xpath_rule, strip=False):
    result = response.xpath(xpath_rule).extract_first()
    if strip:
        result = result.strip()
    return result


class Html:
    def __init__(self, html):
        self.html = html

    @classmethod
    def from_text(cls, text):
        return cls(Selector(text=text))

    def xpath(self, xpath_rule):
        return self.html.xpath(xpath_rule)

    def xpath_first(self, xpath_rule):
        return xpath(self.html, xpath_rule)


class BaseSpiderFunc:
    def process_html(self, html_text, time_sleep=0):
        if time_sleep:
            time.sleep(time_sleep)
        return Html.from_text(html_text)

    def get(self, url, params=None, **kwargs):
        return self.process_html(requests.get(url, params=params, **kwargs).text)

    def post(self):
        raise Exception()

    def get_from_list(self, urls: list, params=None, time_sleep=0, **kwargs):
        return [self.process_html(requests.get(url, params=params, **kwargs).text, time_sleep) for url in urls]

    def get_proxy_from_xpath(self, response, ip_xpath, port_xpath, strip=False):
        return ':'.join((xpath(response, ip_xpath, strip), xpath(response, port_xpath, strip)))


class CrawlerMetaClass(type):
    def __new__(cls, names, bases, attrs):
        for name, func in attrs.items():
            if name.startswith('spider_'):
                attrs['__spider_func__'].update({name: func})
        return super(CrawlerMetaClass, cls).__new__(cls, names, bases, attrs)


class Crawler(BaseSpiderFunc, metaclass=CrawlerMetaClass):
    __spider_func__ = {}  # 存储爬虫

    def spider_xici(self):
        # 下载部分
        url = "https://www.xicidaili.com/nn"
        html = self.get(url, headers={'User-Agent': USER_AGENT})
        # 解析部分
        all_tr = html.xpath('//table[@id="ip_list"]//tr[(./td)]')
        proxy = (self.get_proxy_from_xpath(tr, './td[2]/text()', './td[3]/text()') for tr in all_tr)
        yield from proxy  # 生成器，优化内存

    def spider_iphai(self):
        # 下载部分
        url = "http://www.iphai.com/"
        html = self.get(url, headers={'User-Agent': USER_AGENT})
        # 解析部分
        all_tr = html.xpath('//div[@class="table-responsive module"]/table//tr[(./td)]')
        proxy = (self.get_proxy_from_xpath(tr, './td[1]/text()', './td[2]/text()', True) for tr in all_tr)
        yield from proxy

    def spider_yun(self):
        # 下载部分
        url = "http://www.ip3366.net/?stype=1&page={}"
        urls = [url.format(i) for i in range(1, 11)]
        html_list = self.get_from_list(urls, headers={'User-Agent': USER_AGENT})
        # 解析部分
        proxy = []
        for html in html_list:
            all_tr = html.xpath('//div[@id="list"]/table//tr[(./td)]')
            proxy += (self.get_proxy_from_xpath(tr, './td[1]/text()', './td[2]/text()') for tr in all_tr)
        yield from proxy

    def spider_kuai(self):
        # 下载部分
        url = "https://www.kuaidaili.com/free/inha/{}/"
        urls = [url.format(i) for i in range(1, 3)]
        html_list = self.get_from_list(urls, headers={'User-Agent': USER_AGENT}, time_sleep=1)
        # 解析部分
        proxy = []
        for html in html_list:
            all_tr = html.xpath('//div[@id="list"]/table//tr[(./td)]')
            proxy += (self.get_proxy_from_xpath(tr, './td[1]/text()', './td[2]/text()') for tr in all_tr)
        yield from proxy


class CrawlerProcess(Crawler):
    def __init__(self):
        self.redis = Redis.from_setting(config)
        self.setting = config

    def is_overflow(self):
        return self.redis.count() > self.setting.redis_pool_size

    def start(self):
        logger.info('爬虫开始运行')
        if not self.is_overflow():
            for name, func in self.__spider_func__.items():
                if not name.endswith(self.setting.allow_spider):
                    continue
                for proxy in func(self):
                    self.redis.add(proxy)
            self.redis.pipe_execute()


def main():
    s = CrawlerProcess()
    s.start()


if __name__ == '__main__':
    s = CrawlerProcess()
    s.start()
