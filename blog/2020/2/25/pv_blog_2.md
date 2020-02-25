<!--
https://ae01.alicdn.com/kf/Hc80c70315e124ce6853e053333335bbfr.png
scrapy
Scrapy源码（三）
Scrapy是基于twisted搭建的异步分布式框架。command指令执行CrawlerProcess类中的方法
Scrapy是基于twisted搭建的异步分布式框架。CrawlerProcess是整个Scrapy爬虫框架的启动者，包含创建Engine引擎、然后Engine进行其他相关模块的创建
-->

## Scrapy源码（三）

> Scrapy是基于twisted搭建的异步分布式框架。command指令执行CrawlerProcess类中的方法  
> CrawlerProcess是整个Scrapy爬虫框架的启动者，包含创建Engine引擎、然后Engine进行其他相关模块的创建

### crawler
#### 1、CrawlerProcess - 爬虫进程管理者
在上篇博客中，看到真正的启动，其实时执行了CrawlerProcess的crawl和start两个方法  
**crawl**方法  
定义在CrawlerRunner类中。执行`self.create_crawler()`方法创建Crawler实例  
该函数最终目的就是创建一个Crawler实例，并将其添加到管理队列中，在添加前，执行了函数`d = crawler.crawl(*args, **kwargs)`
运行了爬虫，此时爬虫是待启动状态，已添加到了未来期程中。  
```
class CrawlerProcess(CrawlerRunner):
    def crawl(self, crawler_or_spidercls, *args, **kwargs):
        crawler = self.create_crawler(crawler_or_spidercls)
        return self._crawl(crawler, *args, **kwargs)

    def create_crawler(self, crawler_or_spidercls):
        if isinstance(crawler_or_spidercls, Crawler):
            return crawler_or_spidercls
        return self._create_crawler(crawler_or_spidercls)

    def _create_crawler(self, spidercls):
        if isinstance(spidercls, six.string_types):
            spidercls = self.spider_loader.load(spidercls)
        return Crawler(spidercls, self.settings)

    def _crawl(self, crawler, *args, **kwargs):
        self.crawlers.add(crawler)
        d = crawler.crawl(*args, **kwargs)
        self._active.add(d)

        def _done(result):
            self.crawlers.discard(crawler)
            self._active.discard(d)
            self.bootstrap_failed |= not getattr(crawler, 'spider', None)
            return result

        return d.addBoth(_done)
```
其中还有一个很重要的方法`self.spider_loader.load(spidercls)`，是用来加载爬虫的  
其中`loader_cls = load_object(cls_path)`还不是加载的爬虫，而是 SPIDER_LOADER_CLASS 这个类方法  
该类中实例化的时候，就会扫描项目中的所有爬虫，并将其加载到一个字典中进行管理。
```
def _get_spider_loader(settings):
    loader_cls = load_object(cls_path)
    return loader_cls.from_settings(settings.frozencopy())

@implementer(ISpiderLoader)
class SpiderLoader(object):
    def load(self, spider_name):
        try:
            return self._spiders[spider_name]
        except KeyError:
            raise KeyError("Spider not found: {}".format(spider_name))
```
**start**方法  
创建了一个线程池，然后调用`reactor.run`方法，此时整个异步程序正式启动。
```
class CrawlerProcess(CrawlerRunner):
    def start(self, stop_after_crawl=True):
        if stop_after_crawl:
            d = self.join()
            if d.called:
                return
            d.addBoth(self._stop_reactor)

        reactor.installResolver(self._get_dns_resolver())
        tp = reactor.getThreadPool()
        tp.adjustPoolsize(maxthreads=self.settings.getint('REACTOR_THREADPOOL_MAXSIZE'))
        reactor.addSystemEventTrigger('before', 'shutdown', self.stop)
        reactor.run(installSignalHandlers=False)  # blocking call
```
#### 2、CrawlerRunner - 爬虫进程执行者
该类的主要方法，已在 CrawlerProcess 类中实现

#### 3、Crawler - 爬虫执行子单元
* `self.spidercls.update_settings(self.settings)`：spidercls是爬虫类，此时还未实例化，此处执行的
update_settings 方法，是初始化 custom_settings 设置。故，我们将custom_settings写在爬虫的init中是没有效果的，
因为在该操作是在爬虫实例化之前执行的
* `@defer.inlineCallbacks`：是异步函数的装饰器  
```
class Crawler(object):
    def __init__(self, spidercls, settings=None):
        self.spidercls = spidercls
        self.spidercls.update_settings(self.settings)

    @defer.inlineCallbacks
    def crawl(self, *args, **kwargs):
        self.spider = self._create_spider(*args, **kwargs)
        self.engine = self._create_engine()
        start_requests = iter(self.spider.start_requests())
        yield self.engine.open_spider(self.spider, start_requests)
        yield defer.maybeDeferred(self.engine.start)
```
至此，爬虫终于创建了实例，同时还创建了引擎的实例。然后调用引擎的open_spider方法，  
此方法是一个异步方法，表示执行完open_spider方法后，立即执行`self.engine.start`方法


