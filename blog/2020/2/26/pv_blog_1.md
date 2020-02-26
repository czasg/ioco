<!--
https://ae01.alicdn.com/kf/H02dd8213a09149a5b8f1aef4fbcb3e98B.png
scrapy
Scrapy源码（四）
Scrapy是基于twisted搭建的异步分布式框架。Crawler实例化过程，创建了Spider和Engine实例。
Scrapy是基于twisted搭建的异步分布式框架。创建爬虫和引擎的实例，该部分则正式进入异步操作，引擎是整个框架运作的核心，管理其他模块的正常运行。
-->

## Scrapy源码（四）

> Scrapy是基于twisted搭建的异步分布式框架。Crawler实例化过程，创建了Spider和Engine实例。  
> 创建爬虫和引擎的实例后，该部分则正式进入异步操作，引擎是整个框架运作的核心，管理其他模块的正常运行。

### engine
在crawler中，创建了爬虫和引擎实例。  
主要包括：engine.open_spider 和 engine.start
```
yield self.engine.open_spider(self.spider, start_requests)
yield defer.maybeDeferred(self.engine.start)
```
整个爬虫框架由引擎、调度器、下载器、爬虫、管道组成。 
其中 在下载器之前有一个downloadMiddleware下载中间件，爬虫之前有一个spiderMiddleware爬虫中间件

#### 1、open_spider - 引擎初始化爬虫
该函数也是一个异步执行的函数，里面初始化了调度器scheduler、心跳slot、scraper、状态记录stats。  
下载器downloader在引擎实例创建过程中就已完成初始化，故在此函数中没有体现。  
`yield self.scraper.spidermw.process_start_requests`我们可以发现，第一次接触的中间件为爬虫中间件，且仅执行一次
```
class ExecutionEngine(object):
    @defer.inlineCallbacks
    def open_spider(self, spider, start_requests=(), close_if_idle=True):
        nextcall = CallLaterOnce(self._next_request, spider)
        scheduler = self.scheduler_cls.from_crawler(self.crawler)  # scrapy.core.scheduler.Scheduler
        start_requests = yield self.scraper.spidermw.process_start_requests(start_requests, spider)
        slot = Slot(start_requests, close_if_idle, nextcall, scheduler)
        self.slot = slot
        self.spider = spider
        yield scheduler.open(spider) 
        yield self.scraper.open_spider(spider) 
        self.crawler.stats.open_spider(spider)
        yield self.signals.send_catch_log_deferred(signals.spider_opened, spider=spider)
        slot.nextcall.schedule()
        slot.heartbeat.start(5)
```
CallLaterOnce是一个异步唤醒类，该类中注册由待唤醒目标函数，每一次执行nextcall.schedule()，则会执行一次目标函数，
此处即self._next_request

#### 2、_next_request - 异步轮询请求
该函数，实在start函数启动后，才会开始执行的。  
* self._needs_backout(spider)：表示是否需要退出
    * 当引擎没有running、心跳slot关闭了、下载器确认退出、scrape确认退出
* self._next_request_from_scheduler：表示从调度器中取出一个request请求  

我们可以看出首次执行时，self._needs_backout(spider)为False。即不需要退出，
然后调度器中也没有请求，直接break。直接进入start_requests，从中取出一个，
执行self.crawl()函数，将请求入调度器的队列，然后再次执行此函数。  
但是这时，_next_request_from_scheduler就会执行了，因为调度器队列中已经有了数据了
```
    def _next_request(self, spider):
        while not self._needs_backout(spider):
            if not self._next_request_from_scheduler(spider):
                break

        if slot.start_requests and not self._needs_backout(spider): 
            try:
                request = next(slot.start_requests)
            except StopIteration:
                slot.start_requests = None
            else:
                self.crawl(request, spider)

        if self.spider_is_idle(spider) and slot.close_if_idle:
            self._spider_idle(spider)
```

#### 3、crawl - 请求入队
首先执行self.schedule函数，该函数执行了scheduler.enqueue_request(request)，也就是请求入队，推到调度器所在队列
```
    def crawl(self, request, spider):
        self.schedule(request, spider)
        self.slot.nextcall.schedule() 

    def schedule(self, request, spider):
        self.signals.send_catch_log(signal=signals.request_scheduled,
                request=request, spider=spider)
        if not self.slot.scheduler.enqueue_request(request):
            self.signals.send_catch_log(signal=signals.request_dropped,
                                        request=request, spider=spider)
```

#### 4、_next_request_from_scheduler - 请求出队
从调度器中获取一个request，初始时，该请求来自start_requests，即开发指定url  
然后执行self._download下载函数，得到最终的结果。紧接着执行 self._handle_downloader_output 函数处理获取到的结果。
再从slot中一处该请求，继续触发请求轮询
```
    def _next_request_from_scheduler(self, spider):
        slot = self.slot
        request = slot.scheduler.next_request()
        if not request:
            return
        d = self._download(request, spider)
        d.addBoth(self._handle_downloader_output, request, spider)
        d.addErrback(lambda f: logger.info('Error while handling downloader output',
                                           exc_info=failure_to_exc_info(f),
                                           extra={'spider': spider}))
        d.addBoth(lambda _: slot.remove_request(request))
        d.addErrback(lambda f: logger.info('Error while removing request from slot',
                                           exc_info=failure_to_exc_info(f),
                                           extra={'spider': spider}))
        d.addBoth(lambda _: slot.nextcall.schedule())
        d.addErrback(lambda f: logger.info('Error while scheduling new request',
                                           exc_info=failure_to_exc_info(f),
                                           extra={'spider': spider}))
        return d
```

#### 5、_download - 请求下载
对于引擎来说，真正的下载由self.downloader.fetch实现，返回结果由_on_success实现  
再此处指定了返回结果必须是(Response, Request)中的一种，如果是Response，则将request赋值进去
```
    def _download(self, request, spider):
        def _on_success(response):
            assert isinstance(response, (Response, Request))
            if isinstance(response, Response):
                response.request = request # tie request to response received
                logkws = self.logformatter.crawled(request, response, spider)
                logger.log(*logformatter_adapter(logkws), extra={'spider': spider})
                self.signals.send_catch_log(signal=signals.response_received, \
                    response=response, request=request, spider=spider)
            return response

        def _on_complete(_):
            slot.nextcall.schedule()
            return _

        dwld = self.downloader.fetch(request, spider) 
        dwld.addCallbacks(_on_success)
        dwld.addBoth(_on_complete)
        return dwld
```

#### 6、_handle_downloader_output - 处理下载结果
在该函数中，处理下载结果的时候，如果该结果是Request，则继续入队，如果是Response，
则丢到self.scraper.enqueue_scrape进行后续的处理，里面应该包括爬虫和管道的后续处理。  
但对于引擎来说，一个完整的调度过程已完成。
```
    def _handle_downloader_output(self, response, request, spider): 
        assert isinstance(response, (Request, Response, Failure)), response
        # downloader middleware can return requests (for example, redirects)
        if isinstance(response, Request): 
            self.crawl(response, spider)
            return
        # response is a Response or Failure
        d = self.scraper.enqueue_scrape(response, request, spider)
        return d
```