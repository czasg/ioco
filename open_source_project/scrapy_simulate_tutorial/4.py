import _queue

from twisted.internet import defer, reactor
from twisted.web.client import getPage
from queue import Queue

q = Queue()


class Engine:
    def __init__(self):
        self.max_pool_size = 4
        self.crawling = []

    @defer.inlineCallbacks
    def start(self):
        self._closewait = defer.Deferred()
        yield self._closewait

    def _handle_downloader_output(self, byte_content, request):
        response = Response(byte_content, request)
        request.callback(response)
        self.crawling.remove(request)

    def _next_request(self):
        if len(self.crawling) < self.max_pool_size:
            while True:
                try:
                    request = q.get(block=False)
                    self.crawling.append(request)
                    dfd = getPage(request.url.encode())
                    dfd.addCallback(self._handle_downloader_output, request)
                    dfd.addCallback(lambda _: reactor.callLater(0, self._next_request))
                except _queue.Empty:
                    break
        if q.qsize() == 0 and not self.crawling:
            self._closewait.callback(None)

    @defer.inlineCallbacks
    def open_spider(self, spider):
        for request in spider.start_requests():
            q.put(request)
        reactor.callLater(0, self._next_request)
        yield


class Request:
    def __init__(self, url, callback=None):
        self.url = url
        self.callback = callback


class Response:
    def __init__(self, byte_content, request):
        self.content = byte_content
        self.request = request
        self.url = request.url
        self.text = str(byte_content, encoding='utf-8')


class MySpider:
    start_urls = ['http://www.czasg.xyz', 'http://www.czasg.xyz', 'http://www.czasg.xyz', 'http://www.czasg.xyz',
                  'http://www.czasg.xyz', 'http://www.czasg.xyz', 'http://www.czasg.xyz', 'http://www.czasg.xyz']

    def start_requests(self):
        yield from (Request(url, self.parse) for url in self.start_urls)

    def parse(self, response):
        print(response.url)


if __name__ == '__main__':
    @defer.inlineCallbacks
    def crawl():
        spider = MySpider()
        engine = Engine()
        yield engine.open_spider(spider)
        yield engine.start()
    d = crawl()
    d.addBoth(lambda _: reactor.stop())
    reactor.run()
