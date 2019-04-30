import time
import queue
from multiprocessing.managers import BaseManager


class _Queue:
    queue_task = queue.Queue()
    queue_result = queue.Queue()

    @classmethod
    def task(cls):
        return cls.queue_task

    @classmethod
    def result(cls):
        return cls.queue_result


class Master(BaseManager):
    def __init__(self, address, authkey):
        super(Master, self).__init__(address=address, authkey=authkey)

    @classmethod
    def register_master(cls, ip, port, key):
        cls.register('get_task_queue', callable=_Queue.task)
        cls.register('get_result_queue', callable=_Queue.result)
        return cls(address=(ip, port), authkey=key)


class Worker(BaseManager):
    def __init__(self, address, authkey):
        super(Worker, self).__init__(address=address, authkey=authkey)

    @classmethod
    def register_worker(cls, ip, port, key):
        cls.register('get_task_queue')
        cls.register('get_result_queue')
        return cls(address=(ip, port), authkey=key)


class WorkFlow:
    def __init__(self, ip, port, key):
        self.ip = ip
        self.port = port
        self.key = key

    def register_worker(self):
        self.worker = Worker.register_worker(self.ip, self.port, self.key)
        self.worker.connect()
        self.worker_task_queue = self.worker.get_task_queue()
        self.worker_result_queue = self.worker.get_result_queue()

    def register_master(self):
        self.master = Master.register_master(self.ip, self.port, self.key)
        self.master.start()
        self.master_task_queue = self.master.get_task_queue()
        self.master_result_queue = self.master.get_result_queue()

    def register_all(self):
        self.register_master()
        self.register_worker()
        return self

    def master_create_task(self, *args):
        print('creating tasks...')
        for task in args:
            self.master_task_queue.put(task)
            print('TASK: {} create done!'.format(task))
            time.sleep(2)
        print('tasks create done')

    def master_get_result(self):
        print('worker done! now i will get result')
        while True:
            try:
                time.sleep(2)
                res = self.master_result_queue.get(timeout=10)
                print(res)
            except queue.Empty:
                break

    def worker_flow(self):
        while True:
            try:
                time.sleep(2)
                task = self.worker_task_queue.get(timeout=2)
                print('worker have get task: {}'.format(task))
                self.worker_result_queue.put('test done')
                print('{} done!'.format(task))
            except queue.Empty:
                break

    def single_flow(self, *args):
        self.master_create_task(*args)
        self.worker_flow()
        self.master_get_result()


if __name__ == "__main__":
    worker = WorkFlow('127.0.0.1', 5000, b'123').register_all().single_flow('test1', 'test2', 'test3')
