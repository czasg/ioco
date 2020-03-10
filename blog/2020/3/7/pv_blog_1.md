<!--
https://ae01.alicdn.com/kf/H7e040060ce6448c1a90050ba49a1d9ecE.png
flask
Flask源码（一）
Flask源码学习，包括对wsgi协议的学习。该篇主要通过学习低级原生接口了解底层实现。
Flask源码学习，包括对wsgi协议的学习，涉及很多低级原生接口，如socketserver.py内部的一些接口文件。
-->

## Flask源码（一）

> Flask源码学习，包括对wsgi协议的学习。涉及很多低级原生接口，如socketserver.py内部的一些接口文件。  
> 我们可以通过低级原生接口了解底层实现，从而进一步了解学习flask

### 1、线程本地数据

![线程本地数据](https://ae01.alicdn.com/kf/Ha9d75d7c2440417d9fda73ce50e73d2d3.png)

每个线程能够以 "全局变量" 的形式，维护自己的一个 "本地" 数据  
大致原理即，存在一个全局对象，内部维护有一个字典，修改__setattr__和__getattr__两个魔术方法   
每次set和get的时候，会调用 get_ident 方法，获取当前线程的唯一ID  
并以之为字典的key，在字典中维护一个新得数据结构作为value，从而保证每一个线程都只会调用自己得value

### 2、WSGI服务
开发web服务时，为了避免接触底层TCP连接、HTTP响应格式，统一开发接口，即WSGI标准  
Web Server Gateway Interface  

该接口要求开发者实现一个函数即可响应HTTP请求  
该函数需要符合wsgi标准，即接收两个参数：
* environ：一个包含了所有http请求信息得字典对象
* start_response：一个发送http响应的函数
    * 该函数其实是发送响应Header的，且只能发送一次。他也接收两个参数，一个是响应码，一个一组list组成的Header，
    而每一个header则为一个tuple元组，内含两个str
```python
def application(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    return [b'<h1>Hello, web!</h1>']
```

### 3、底层socketserver服务
对于ThreadingTCPServer类，重写了方法process_request，当服务启动后，正常流程变为：  
1. serve_forever。服务启动并监听端口，当有监听到请求时，调用_handle_request_noblock方法处理请求
2. _handle_request_noblock。获取请求得socket句柄，并调用process_request对请求进行处理
3. process_request。该方法被ThreadingMixIn重写，实际会重开一个新线程，然后调用finish_request方法
4. finish_request。调用了RequestHandlerClass，并实例化，至此，关键得处理流程已走完。
```python
class BaseServer:
    def __init__(self, server_address, RequestHandlerClass):
        self.server_address = server_address
        self.RequestHandlerClass = RequestHandlerClass

    def serve_forever(self, poll_interval=0.5):
        with _ServerSelector() as selector:
            selector.register(self, selectors.EVENT_READ)
            while not self.__shutdown_request:
                ready = selector.select(poll_interval)
                if self.__shutdown_request: break
                if ready: self._handle_request_noblock()

    def _handle_request_noblock(self):
        request, client_address = self.get_request()
        self.process_request(request, client_address)

    def finish_request(self, request, client_address):
        self.RequestHandlerClass(request, client_address, self)

class TCPServer(BaseServer):
        """Constructor.  May be extended, do not override."""

class ThreadingMixIn:
    def process_request_thread(self, request, client_address):
        try: self.finish_request(request, client_address)
        finally: self.shutdown_request(request)

    def process_request(self, request, client_address): 
        t = threading.Thread(target=self.process_request_thread, args=(request, client_address))

class ThreadingTCPServer(ThreadingMixIn, TCPServer): pass
```

对于每一个handler，在实例化之后，会执行setup -> handle -> finish三个函数，只需要按需要重写即可
```python
class BaseRequestHandler:
    def __init__(self, request, client_address, server):
        self.request = request
        self.client_address = client_address
        self.server = server
        self.setup()
        try: self.handle()
        finally: self.finish()

    def setup(self): pass

    def handle(self): pass

    def finish(self): pass
```

### 4、Flask底层启动

```python
class WSGIRequestHandler:
    def handle(self):
        self.handle_one_request()

    def handle_one_request(self):
        self.parse_request()
        return self.run_wsgi()

    def parse_request(self):
        self.command = None
        self.path = None
        self.headers = None

    def run_wsgi(self):
        environ = None
        start_response = None
        self.app(environ, start_response)

class BaseWSGIServer():
    def __init__(self):
        handler = WSGIRequestHandler

class ThreadingMixIn: ...

class ThreadedWSGIServer(ThreadingMixIn, BaseWSGIServer): ...

def make_server(): return ThreadedWSGIServer()

def run_simple():
    srv = make_server()
    srv.serve_forever()
```
Flask是基于wsgi标准搭建的web端开发框架，所以，从全局的角度来看，Flask其实就是一个app顶层应用  
用来对接wsgi接口的两个参数，一个environ、一个start_response  

故我们上层开发过程，是基于这两个参数进行的，Flask对这两个参数进行了适当的封装和拓展
