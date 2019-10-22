import socket
import time


def blocking_socket(response=b''):
    sock = socket.socket()
    sock.connect(('www.baidu.com', 80))
    sock.send(b'GET / HTTP/1.0\r\n\r\n')
    chunk = sock.recv(1024)
    while chunk:
        response += chunk
        chunk = sock.recv(1024)
    return response


def mutil_blocking_socket():
    return [blocking_socket() for _ in range(10)].__len__()


if __name__ == '__main__':
    start = time.time()
    blocking_socket()  # 执行一次
    # mutil_blocking_socket()  # 执行十次
    print(time.time() - start)
