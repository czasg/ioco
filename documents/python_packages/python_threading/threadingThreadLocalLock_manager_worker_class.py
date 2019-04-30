import time
import threading
from queue import Queue

lock = threading.Condition()
local = threading.local()

queue = Queue()


class Man(object):
    queue = queue
    lock = lock
    local = local

    def __init__(self, name=None, position=None):
        self._name = name
        self._position = position

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, _name):
        self._name = _name

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, _position):
        self._position = _position


class Manager(Man):
    def __init__(self, *args, **kwargs):
        super(Manager, self).__init__(*args, **kwargs)

    def create_task(self, task):
        lock.acquire()
        print('{creator} create a new task...: {task}'.format(creator=threading.current_thread().name, task=task))
        time.sleep(2)
        self._distribute(task)
        print('{creator} task {task} create success!'.format(creator=threading.current_thread().name, task=task))
        lock.wait()  # it will release the lock
        lock.release()

    def _distribute(self, task):
        self.queue.put(task)


class Worker(Man):
    def __init__(self, *args, **kwargs):
        super(Worker, self).__init__(*args, **kwargs)

    def receive_task(self):
        while True:
            lock.acquire()
            task = self.queue.get()
            self._process_task(task)
            lock.notify()
            lock.release()
            time.sleep(1)  # why it still go circle to acquire lock? i have to sleep it so manager can get a lock

    def _process_task(self, task):
        print('{threading} task: {task}'.format(threading=threading.current_thread().name, task=task))
        time.sleep(2)
        print('{threading} task: {task} done!'.format(threading=threading.current_thread().name, task=task))


class WorkFlow:
    def __init__(self, worker=None, manager=None):
        self.worker = worker
        self.manager = manager

    def create_task(self, *args):
        self.task_count = len(args)
        for task in args:
            self.manager.create_task(task)

    def process_task(self):
        self.worker.receive_task()

    def single_flow(self, *args):
        self.create_task(*args)
        self.process_task()

    def multi_flow(self, *args):
        m = threading.Thread(target=self.create_task, args=args, name='MAKER')
        w = threading.Thread(target=self.process_task, name='WORKER')
        m.start()
        w.start()
        m.join()
        w.join()


if __name__ == "__main__":
    w = Worker('Bob', 'boss')
    m = Manager('Dave', 'employee')
    wf = WorkFlow(worker=w, manager=m)
    wf.multi_flow('test1', 'test2', 'test3')
