import socket
import time

from selectors import DefaultSelector, EVENT_READ, EVENT_WRITE

selector = DefaultSelector()
stop_loop = 10


def fetch(sock):
    sock.setblocking(False)
    try:
        sock.connect(('www.baidu.com', 80))
    except BlockingIOError:
        pass

    future = Future()

    def _on_send():
        future.set_result(None)

    selector.register(sock.fileno(), EVENT_WRITE, _on_send)
    yield from future
    selector.unregister(sock.fileno())
    return future


def read(sock, future, flag, response=b''):
    def _on_recv():
        future.set_result(sock.recv(1024))

    selector.register(sock.fileno(), EVENT_READ, _on_recv)
    chunk = yield from future
    while chunk:
        response += chunk
        chunk = yield from future
    selector.unregister(sock.fileno())
    global stop_loop
    stop_loop -= flag
    return response


def loop():
    while stop_loop:
        events = selector.select()
        for sock, mask in events:
            sock.data()


class Future:
    def __init__(self):
        self.result = None
        self.callback = None

    def set_callback(self, func):
        self.callback = func

    def set_result(self, result):
        self.result = result
        self.callback(self) if self.callback else None

    def __iter__(self):
        yield self
        return self.result


class Task:
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
    def __init__(self, flag):
        self.flag = flag

    def fetch(self):
        sock = socket.socket()
        future = yield from fetch(sock)
        sock.send(b'GET / HTTP/1.0\r\n\r\n')
        response = yield from read(sock, future, self.flag)
        print(response)


if __name__ == '__main__':
    start = time.time()
    Task(Crawler(10).fetch())
    # [Task(Crawler(1).fetch()) for _ in range(10)]
    loop()
    print(time.time() - start)
