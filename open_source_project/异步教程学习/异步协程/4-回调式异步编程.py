import socket
import time

from selectors import DefaultSelector, EVENT_READ, EVENT_WRITE

selector = DefaultSelector()
stop_loop = 10


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
        selector.register(self.sock.fileno(), EVENT_WRITE, self.on_send)  # fileno()获取当前socket套接字的文件描述符，并绑定事件回调

    def on_send(self):
        selector.unregister(self.sock.fileno())
        self.sock.send(b'GET / HTTP/1.0\r\n\r\n')
        selector.register(self.sock.fileno(), EVENT_READ, self.on_recv)

    def on_recv(self):
        chunk = self.sock.recv(1024)
        if chunk:
            self.response += chunk
        else:
            global stop_loop
            stop_loop -= self.flag
            selector.unregister(self.sock.fileno())


def loop():  # 事件循环，由操作系统通知那个事件发生了，应该对应执行那些事件的回调。
    while stop_loop:
        events = selector.select()
        for sock, mask in events:
            sock.data()


if __name__ == '__main__':
    start = time.time()
    Crawler(10).fetch()  # 执行一次
    # [Crawler(1).fetch() for _ in range(10)]  # 执行十次
    loop()
    print(time.time() - start)
