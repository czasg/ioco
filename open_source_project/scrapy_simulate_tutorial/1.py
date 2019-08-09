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
    def start_requests(self):
        url = 'http://www.czasg.xyz'
        yield Request(url, self.parse)

    def parse(self, response):
        print(response.url)


if __name__ == '__main__':
    spider = MySpider()
    request = next(spider.start_requests())           # 获取一个Request对象，作为入口

    import requests                                   # scrapy是基于Twisted实现的异步下载，此处requests就是凑凑
    byte_content = requests.get(request.url).content  # 假装是通过Twisted获取Request对象，下载目标DOM

    response = Response(byte_content, request)        # 构造Response对象
    request.callback(response)                        # 执行回调函数
