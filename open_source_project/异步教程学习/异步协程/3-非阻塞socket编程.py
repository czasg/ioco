import socket
import time


def no_blocking_socket(response=b''):
    sock = socket.socket()
    sock.setblocking(False)
    try:
        sock.connect(('www.baidu.com', 80))
    except BlockingIOError:
        pass

    while True:
        try:
            sock.send(b'GET / HTTP/1.0\r\n\r\n')
            break
        except OSError:
            continue

    while True:
        try:
            chunk = sock.recv(1024)
            while chunk:
                response += chunk
                chunk = sock.recv(1024)
            return response
        except OSError:
            pass


def multi_no_blocking_socket():
    return [no_blocking_socket() for _ in range(10)].__len__()


if __name__ == '__main__':
    start = time.time()
    no_blocking_socket()  # 执行一次
    # multi_no_blocking_socket()  # 执行十次
    print(time.time() - start)
