import time
import threading

lock = threading.Condition()

task = None


class Consumer(threading.Thread):
    def __init__(self, name):
        super(Consumer, self).__init__(name=name)
        self.name = name

    def run(self):
        lock.acquire()
        print('{}: I will use it'.format(self.name))
        time.sleep(2)
        while True:
            if not task:
                print('{}: task is None!'.format(self.name))
                lock.notify()
            lock.wait()
            print('{}: take over the lock'.format(self.name))
            time.sleep(2)


class Productor(threading.Thread):
    def __init__(self, name):
        super(Productor, self).__init__(name=name)
        self.name = name

    def run(self):
        lock.acquire()
        while True:
            if not task:
                print('{}: task is None! produce success!'.format(self.name))
                lock.wait()
                print('{}: take over the lock'.format(self.name))
            lock.notify()
            time.sleep(2)


if __name__ == "__main__":
    p = Productor('boss')
    c = Consumer('cza')
    p.start()
    c.start()
    p.join()
    c.join()
