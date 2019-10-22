import socket
import time

from selectors import DefaultSelector, EVENT_READ, EVENT_WRITE

selector = DefaultSelector()
stop_loop = 10


class Future:
    # 用于存放未来可能出现的数据，当出现时执行一次回调函数
    # 此种的result仅作为一个中转，实际还是通过回调返回给协程

    def __init__(self):
        self.result = None
        self.callback = None

    def set_callback(self, func):
        self.callback = func

    def set_result(self, result):
        self.result = result
        self.callback(self) if self.callback else None


class Task:
    # 用于启动协程，该类实例初始化时传入为协程对象，执行self.process方法
    # 调用协程的send方法，启动协程，并最后绑定回调函数

    def __init__(self, co_routine):
        self.co_routine = co_routine
        future = Future()
        self.process(future)

    def process(self, future):
        try:
            next_future = self.co_routine.send(future.result)
        except StopIteration:
            return
        next_future.set_callback(self.process)


class Crawler:
    def __init__(self, flag=10):
        self.flag = flag
        self.sock = None
        self.response = b''

    def fetch(self):
        self.sock = socket.socket()
        self.sock.setblocking(False)
        try:
            self.sock.connect(('www.baidu.com', 80))
        except BlockingIOError:
            pass

        future = Future()

        def _on_send():
            future.set_result(None)

        def _on_recv():
            future.set_result(self.sock.recv(1024))

        selector.register(self.sock.fileno(), EVENT_WRITE, _on_send)
        yield future
        selector.unregister(self.sock.fileno())
        self.sock.send(b'GET / HTTP/1.0\r\n\r\n')
        selector.register(self.sock.fileno(), EVENT_READ, _on_recv)
        while True:
            chunk = yield future  # 在此处轮询EVENT_READ事件，直至所有数据加载完毕
            if chunk:
                self.response += chunk
            else:
                global stop_loop
                stop_loop -= self.flag
                return self.response


def loop():
    while stop_loop:
        events = selector.select()
        for sock, mask in events:
            sock.data()


if __name__ == '__main__':
    start = time.time()
    Task(Crawler(10).fetch())  # 传入协程fetch，使用Task实例化调用协程的send方法来启动协程
    # [Task(Crawler(1).fetch()) for _ in range(10)]  # 同理，启动十个协程任务
    loop()
    print(time.time() - start)
