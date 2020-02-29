<!--
https://ae01.alicdn.com/kf/H8e998673bc8b486ca315e89c013a6026F.png
scrapy
Scrapy源码（七）
Scrapy是基于twisted搭建的异步分布式框架。下载出获取response之后，调用scraper刮擦器进行最后的处理。
Scrapy是基于twisted搭建的异步分布式框架。刮擦器主要调用爬虫中间件SpiderMidlleware方法，将call_spider作为回调函数传入，call_spider会调用开发编写爬虫执行并获取结果。
-->

## Scrapy源码（七）

> Scrapy是基于twisted搭建的异步分布式框架。下载出获取response之后，调用scraper刮擦器进行最后的处理。  
> 刮擦器主要调用爬虫中间件SpiderMidlleware方法，将call_spider作为回调函数传入，call_spider会调用开发编写爬虫执行并获取结果  
> 对于爬虫中间件的结果，调用_process_spidermw_output进行处理，若结果是Request则重新入队，
> 若是字典或者Item类则调用管道处理器处理，生死不论，后续指挥做日志处理。

### scraper
刮擦器时对response的最后一层处理，此层处理完后，engine中一次完整的爬虫流程结束。
```python
class ExecutionEngine(object):
    def __init__(self, crawler, spider_closed_callback):
        self.scraper = Scraper(crawler)

    def _handle_downloader_output(self, response, request, spider):
        d = self.scraper.enqueue_scrape(response, request, spider)
        return d
```

#### 1、enqueue_scrape - 刮擦器入口
刮擦器内部也维护有一个队列。add_response_request是入队的函数，next_response_request_deferred是出队函数
```python
class Scraper(object):
    def __init__(self, crawler):
        self.spidermw = SpiderMiddlewareManager.from_crawler(crawler)
        itemproc_cls = load_object(crawler.settings['ITEM_PROCESSOR'])  # 'scrapy.pipelines.ItemPipelineManager'
        self.itemproc = itemproc_cls.from_crawler(crawler) 

    def enqueue_scrape(self, response, request, spider): 
        slot = self.slot
        dfd = slot.add_response_request(response, request)
        def finish_scraping(_):
            slot.finish_response(response, request)
            self._check_if_closing(spider, slot)
            self._scrape_next(spider, slot)
            return _
        dfd.addBoth(finish_scraping)
        self._scrape_next(spider, slot)  # 主要是为了执行scrape_response，也就是scrape里面对response处理的函数
        return dfd

    def _scrape_next(self, spider, slot):
        while slot.queue:
            response, request, deferred = slot.next_response_request_deferred()
            self._scrape(response, request, spider).chainDeferred(deferred)

    def _scrape(self, response, request, spider):
        dfd = self._scrape2(response, request, spider) # returns spiders processed output
        dfd.addCallback(self.handle_spider_output, request, response, spider)
        return dfd

    def _scrape2(self, request_result, request, spider):
        if not isinstance(request_result, Failure):
            return self.spidermw.scrape_response(
                self.call_spider, request_result, request, spider)

    def call_spider(self, result, request, spider):
        result.request = request
        dfd = defer_result(result)
        dfd.addCallbacks(request.callback or spider.parse, request.errback)
        return dfd.addCallback(iterate_spider_output)

    def handle_spider_output(self, result, request, response, spider):
        if not result:
            return defer_succeed(None)
        it = iter_errback(result, self.handle_spider_error, request, response, spider)
        dfd = parallel(it, self.concurrent_items,
            self._process_spidermw_output, request, response, spider)
        return dfd

    def _process_spidermw_output(self, output, request, response, spider):
        if isinstance(output, Request):
            self.crawler.engine.crawl(request=output, spider=spider)
        elif isinstance(output, (BaseItem, dict)):
            dfd = self.itemproc.process_item(output, spider) 
            dfd.addBoth(self._itemproc_finished, output, response, spider)
            return dfd
        elif output is None:
            pass
```

#### 2、scrape_response - 爬虫中间件
```python
class SpiderMiddlewareManager(MiddlewareManager):
    def scrape_response(self, scrape_func, response, request, spider):
        def process_spider_input(response):
            for method in self.methods['process_spider_input']:
                try:
                    result = method(response=response, spider=spider)
                    assert result is None, \
                            'Middleware %s must returns None or ' \
                            'raise an exception, got %s ' \
                            % (fname(method), type(result))
                except:
                    return scrape_func(Failure(), request, spider)
            return scrape_func(response, request, spider) 

        def process_spider_output(result):
            for method in self.methods['process_spider_output']:
                result = method(response=response, result=result, spider=spider)
                assert _isiterable(result), \
                    'Middleware %s must returns an iterable object, got %s ' % \
                    (fname(method), type(result))
            return result

        dfd = mustbe_deferred(process_spider_input, response) 
        dfd.addCallback(process_spider_output)
        return dfd
```

#### 3、process_item - 管道处理器
对于爬虫中间件处理结果，如果是字典或者Item类，则调用管道进行后续的处理。
```python
class ItemPipelineManager(MiddlewareManager):
    def process_item(self, item, spider):
        return self._process_chain('process_item', item, spider)
```
