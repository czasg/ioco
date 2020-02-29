<!--
https://ae01.alicdn.com/kf/Haf4d3b0529ba47669bf69c7bfc71a5f1Y.png
scrapy
Scrapy源码（六）
Scrapy是基于twisted搭建的异步分布式框架。其中下载器是爬虫获取信息的关键。
Scrapy是基于twisted搭建的异步分布式框架。Engine实例化过程，创建了调度器、下载器、刮擦器等实例。下载器是爬虫获取信息的关键。
-->

## Scrapy源码（六）

> Scrapy是基于twisted搭建的异步分布式框架。Engine实例化过程，创建了调度器、下载器、刮擦器等实例。
> 下载器是爬虫获取信息的关键。

### downloader
在engine中。下载器初始化后，真正起作用的地方其实就只有一处，就是在执行self._download的时候  
调用了下载器的self.downloader.fetch(request, spider)函数。
```Python
class ExecutionEngine(object):
    def __init__(self, crawler, spider_closed_callback):
        downloader_cls = load_object(self.settings['DOWNLOADER'])  # 'scrapy.core.downloader.Downloader'
        self.downloader = downloader_cls(crawler)

    def _next_request_from_scheduler(self, spider):
        d = self._download(request, spider)

    def _download(self, request, spider):
        dwld = self.downloader.fetch(request, spider)
        return dwld
```

#### 1、fetch - 下载器入口
fetch入口调用了中间件的download方法，该中间件，即下载中间件，由downloader函数传递了一个
self._enqueue_request作为回调函数。下载中间件收集所有已注册中间件中的三个函数：  
> 1、process_request：进入下载器之前，对request进行处理。返回None则接着处理其他中间件，否则直接返回   
> 2、process_response：下载完成后，对response进行处理。若是返回Request则直接返回，否则会处理完所有的response中间件  
> 3、process_exception：处理异常时使用   

```Python
class Downloader(object):
    def __init__(self, crawler):
        self.middleware = DownloaderMiddlewareManager.from_crawler(crawler)

    def fetch(self, request, spider):
        dfd = self.middleware.download(self._enqueue_request, request, spider)

class DownloaderMiddlewareManager(MiddlewareManager):
    def download(self, download_func, request, spider):
        @defer.inlineCallbacks
        def process_request(request):
            for method in self.methods['process_request']:
                response = yield method(request=request, spider=spider)
                assert response is None or isinstance(response, (Response, Request))
                if response: 
                    defer.returnValue(response)
            defer.returnValue((yield download_func(request=request,spider=spider)))

        @defer.inlineCallbacks
        def process_response(response):
            for method in self.methods['process_response']:
                response = yield method(request=request, response=response,
                                        spider=spider)
                assert isinstance(response, (Response, Request))
                if isinstance(response, Request):
                    defer.returnValue(response)
            defer.returnValue(response)

        deferred = mustbe_deferred(process_request, request)  # 执行顺序，现执行request，再执行exception，最后才是response
        deferred.addCallback(process_response)
        return deferred
```

#### 2、_enqueue_request - 请求入队
在处理process_request的时候，若一切正常，则会调用Downloader传递过来的回调函数_enqueue_request  
在Slot中维护有下载队列，并且定义有下载延迟、当前并发量
```python
class Slot(object):
    def __init__(self, concurrency, delay, randomize_delay):
        self.concurrency = concurrency
        self.delay = delay
        self.randomize_delay = randomize_delay

        self.active = set()
        self.queue = deque()
        self.transferring = set()
        self.lastseen = 0
        self.latercall = None

    def free_transfer_slots(self):  # 控制当前并发量
        return self.concurrency - len(self.transferring)

    def download_delay(self):  # 定义时延
        if self.randomize_delay:
            return random.uniform(0.5 * self.delay, 1.5 * self.delay)
        return self.delay
```

调度器维护有一个请求队列，下载器也维护有一个下载队列  
下载器通过获取设置的最大并发量和下载时延，来创建一个Slot管理器，并将请求推到队列中。  
通过slot.lastseen来维护下载的时延，不停递归从下载队列中拿出request，丢到self.handlers.download_request进行下载。
```python
class Downloader(object):
    def __init__(self, crawler):
        self.handlers = DownloadHandlers(crawler)

    def _enqueue_request(self, request, spider):
        key, slot = self._get_slot(request, spider)
        deferred = defer.Deferred().addBoth(_deactivate)
        slot.queue.append((request, deferred))
        self._process_queue(spider, slot)
        return deferred

    def _get_slot(self, request, spider):
        conc, delay = _get_concurrency_delay(conc, spider, self.settings)
        self.slots[key] = Slot(conc, delay, self.randomize_delay)
        return key, self.slots[key]

    def _process_queue(self, spider, slot):
        now = time()
        delay = slot.download_delay()
        if delay:
            penalty = delay - now + slot.lastseen
            if penalty > 0:
                slot.latercall = reactor.callLater(penalty, self._process_queue, spider, slot)
                return

        while slot.queue and slot.free_transfer_slots() > 0:
            slot.lastseen = now
            request, deferred = slot.queue.popleft()
            dfd = self._download(slot, request, spider)
            dfd.chainDeferred(deferred)
            if delay:
                self._process_queue(spider, slot)
                break

    def _download(self, slot, request, spider):
        dfd = mustbe_deferred(self.handlers.download_request, request, spider)

        def finish_transferring(_):
            self._process_queue(spider, slot)
            return _

        return dfd.addBoth(finish_transferring)
```

#### 3、download_request

```python
class DownloadHandlers(object):
    def __init__(self, crawler):
        handlers = without_none_values(
            crawler.settings.getwithbase('DOWNLOAD_HANDLERS')) 
        # 'http'和'https': 'scrapy.core.downloader.handlers.http.HTTPDownloadHandler',
        for scheme, clspath in six.iteritems(handlers):  
            self._schemes[scheme] = clspath
            self._load_handler(scheme, skip_lazy=True)

    def download_request(self, request, spider):
        scheme = urlparse_cached(request).scheme
        handler = self._get_handler(scheme)
        return handler.download_request(request, spider)
```

#### 4、

```python
class HTTP11DownloadHandler(object):
    def download_request(self, request, spider):
        agent = ScrapyAgent(contextFactory=self._contextFactory, pool=self._pool,
            maxsize=getattr(spider, 'download_maxsize', self._default_maxsize),
            warnsize=getattr(spider, 'download_warnsize', self._default_warnsize),
            fail_on_dataloss=self._fail_on_dataloss)
        return agent.download_request(request)

class ScrapyAgent(object):
    def download_request(self, request):
        url = urldefrag(request.url)[0]
        method = to_bytes(request.method)
        headers = TxHeaders(request.headers)
        d = agent.request(
            method, to_bytes(url, encoding='ascii'), headers, bodyproducer)
        d.addCallback(self._cb_bodydone, request, url)
        return d

    def _cb_bodydone(self, result, request, url):
        respcls = responsetypes.from_args(headers=headers, url=url, body=body)
        return respcls(url=url, status=status, headers=headers, body=body, flags=flags)
```
这里的respcls就是TextResponse，也就是我们在解析时候用的response
