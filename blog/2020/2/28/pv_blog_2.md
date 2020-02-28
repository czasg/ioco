<!--
https://ae01.alicdn.com/kf/H0babaa506e534701afbfcf43be15e2e27.png
scrapy
Scrapy源码（五）
Scrapy是基于twisted搭建的异步分布式框架。Engine实例化过程，创建了调度器、下载器、刮擦器等实例。
Scrapy是基于twisted搭建的异步分布式框架。Engine实例化过程，创建了调度器、下载器、刮擦器等实例。初始化时数据都在start_requests中，然后从中推到调度器。这次主要分析调度器在整个流程中的作用。
-->

## Scrapy源码（五）

> Scrapy是基于twisted搭建的异步分布式框架。Engine实例化过程，创建了调度器、下载器、刮擦器等实例。  
> 初始化时数据都在start_requests中，然后从中推到调度器。这次主要分析调度器在整个流程中的作用。

### scheduler
调度器是在引擎执行初始化函数open_spider的时候，一并初始化好的。  
创建实例对象'scrapy.core.scheduler.Scheduler'，并保留引用到slot管理器中   
异步执行调度器的open函数，完成了初始化
```
class ExecutionEngine(object):
    def __init__(self, crawler, spider_closed_callback):
        self.scheduler_cls = load_object(self.settings['SCHEDULER'])  # 'scrapy.core.scheduler.Scheduler'

    @defer.inlineCallbacks
    def open_spider(self, spider, start_requests=(), close_if_idle=True):
        scheduler = self.scheduler_cls.from_crawler(self.crawler)
        slot = Slot(start_requests, close_if_idle, nextcall, scheduler)
        yield scheduler.open(spider)

    def _next_request_from_scheduler(self, spider):
        request = slot.scheduler.next_request()

    def schedule(self, request, spider):
        if not self.slot.scheduler.enqueue_request(request)
```

#### 1、open - 调度器打开
调度器初始化时，可以指定：  
* jobdir：为存储路径。需要指定 JOBDIR 参数，该参数是存储目标文件的路径。存储的是未完成的Request信息
* pqclass：为优先级队列。 默认参数为 'queuelib.PriorityQueue'
* dqclass：为lifo，先进后出队列，且为序列化队列。  'scrapy.squeues.PickleLifoDiskQueue'
* mqclass：也是lifo，而且是存在内存中的队列。 'scrapy.squeues.LifoMemoryQueue'
```
class Scheduler(object):
    def __init__(self, dupefilter, jobdir=None, dqclass=None, mqclass=None,
                 logunser=False, stats=None, pqclass=None):
        self.df = dupefilter
        self.dqdir = self._dqdir(jobdir)  # 还支持把他写到文件里面咯，存的是json
        self.pqclass = pqclass  # 优先级队列
        self.dqclass = dqclass  # lifo队列，经过pickle序列化，但没有存储到文件哦
        self.mqclass = mqclass  # 内存中，lifo队列

    def open(self, spider): 
        self.spider = spider
        self.mqs = self.pqclass(self._newmq)
        self.dqs = self._dq() if self.dqdir else None
        return self.df.open()

    def _newmq(self, priority):
        return self.mqclass()
```
open函数首先创建了一个内存FIFO队列，并将其指定为优先级最低的一条队列 self.pqclass 的默认创建对象。  
然后根据是否存在 dqdir ，也就是序列化参数，来创建序列化队列。  
然后最后打开了 dupefilter 过滤器。该函数啥也没做。

#### 2、next_request - 从调度器取出Request
从next_request函数中，我们可以看出，先从内存队列中推出一个request，如果存在，则计数加一  
若不存在，则从序列化队列中pop一个。然后再首次初始化的时候，内存队列中是没有数据的，故
首次初始化时，如果指定了jobdir，则会扫描上次未完成的爬虫任务，然后进行爬虫的流程。
```
    def next_request(self):
        request = self.mqs.pop()
        if request:
            self.stats.inc_value('scheduler/dequeued/memory', spider=self.spider)
        else:
            request = self._dqpop()
            if request:
                self.stats.inc_value('scheduler/dequeued/disk', spider=self.spider)
        if request:
            self.stats.inc_value('scheduler/dequeued', spider=self.spider)
        return request
```

#### 3、enqueue_request - 数据入队
首先调用了 self.df.request_seen，也就是将request计算出一个唯一指纹，并保存。
若后续存在同一指纹的request，且没有设置dont_filter参数，则此条数据将被过滤。  

而当诗句没有过滤，则有限推到序列化队列，如果没成功，则再推到内存队列。  
推到队列的时候，有指定该条数据的优先级，一般都使用默认的最低级。
```
class Scheduler(object):
    def enqueue_request(self, request):
        if not request.dont_filter and self.df.request_seen(request):
            self.df.log(request, self.spider)
            return False
        dqok = self._dqpush(request)
        if dqok:
            self.stats.inc_value('scheduler/enqueued/disk', spider=self.spider)
        else:
            self._mqpush(request)
            self.stats.inc_value('scheduler/enqueued/memory', spider=self.spider)
        self.stats.inc_value('scheduler/enqueued', spider=self.spider)
        return True

    def _mqpush(self, request): 
        self.mqs.push(request, -request.priority)

class RFPDupeFilter(BaseDupeFilter):
    def request_seen(self, request):
        fp = self.request_fingerprint(request)
        if fp in self.fingerprints:
            return True
        self.fingerprints.add(fp)
        if self.file:
            self.file.write(fp + os.linesep)
```

#### 4、队列
* mqs：内存队列。基于 deque 实现
    * LIFO：后进先处队列，由pop实现
    * FIFO：先进先出队列，有popleft实现
* dqs：
    * 根据 SIZE_FORMAT 表示分隔符，每条记录均由一个 SIZE_FORMAT 跟随。  
    初始化时，如果存在目标文件，则以rb+的形式打开，以SIZE_FORMAT读取该文件的大小记录  
    一条纪律包含两个数据，原始数据和分割标记。
        * 原始数据，即用户需要存储的数据
        * 分割标记。由指定标记符，和用户存储数据的大小，重新编译出新的标记数据。  
        读取的时候先读取分割标记。然后解析分割标记，获取目标的大小。
    * pickle.dumps
    * pickle.loads：这两个时序列化的数据
* pqclass：优先级队列
    * 整个就是一个字典，然后由以优先级为key，以队列为value。保存优先级最大的那个队列，
    从中取出数据，然后重新计算优先级。如果数据为0，则del掉该队列。


```
class LifoDiskQueue(object):

    SIZE_FORMAT = ">L"
    SIZE_SIZE = struct.calcsize(SIZE_FORMAT)

    def __init__(self, path):
        self.path = path
        if os.path.exists(path):
            self.f = open(path, 'rb+')
            qsize = self.f.read(self.SIZE_SIZE)
            self.size, = struct.unpack(self.SIZE_FORMAT, qsize)
            self.f.seek(0, os.SEEK_END)
        else:
            self.f = open(path, 'wb+')
            self.f.write(struct.pack(self.SIZE_FORMAT, 0))
            self.size = 0

    def push(self, string):
        if not isinstance(string, bytes):
            raise TypeError('Unsupported type: {}'.format(type(string).__name__))
        self.f.write(string)
        ssize = struct.pack(self.SIZE_FORMAT, len(string))
        self.f.write(ssize)
        self.size += 1

    def pop(self):
        if not self.size:
            return
        self.f.seek(-self.SIZE_SIZE, os.SEEK_END)
        size, = struct.unpack(self.SIZE_FORMAT, self.f.read())
        self.f.seek(-size-self.SIZE_SIZE, os.SEEK_END)
        data = self.f.read(size)  # 读取之后指针又往后移动了size
        self.f.seek(-size, os.SEEK_CUR)  # 故再此处再次移动回来
        self.f.truncate()
        self.size -= 1
        return data

    def close(self):
        if self.size:
            self.f.seek(0)
            self.f.write(struct.pack(self.SIZE_FORMAT, self.size))
        self.f.close()
        if not self.size:
            os.remove(self.path)

    def __len__(self):
        return self.size
```