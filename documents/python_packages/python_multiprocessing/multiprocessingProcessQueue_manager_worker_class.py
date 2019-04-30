import time
from multiprocessing import Process, Queue

queue = Queue()


class Human(object):

    def __init__(self, _name=None, _position=None):
        self.queue = queue
        self._name = _name
        self._position = _position

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


class Manager(Human):
    def __init__(self, *args, **kwargs):
        super(Manager, self).__init__(*args, **kwargs)

    def create_task(self, task):
        print('create a new task...: {task}'.format(task=task))
        time.sleep(2)
        self._distribute(task)
        print('task {task} create success!'.format(task=task))

    def _distribute(self, task):
        self.queue.put(task)


class Worker(Human):
    def __init__(self, *args, **kwargs):
        super(Worker, self).__init__(*args, **kwargs)

    def receive_task(self, **kwargs):
        while True:
            task = self.queue.get(**kwargs)
            self._process_task(task)

    def _process_task(self, task):
        print('processing task: {task}'.format(task=task))
        time.sleep(1)
        print('processing task: {task} done!'.format(task=task))


class WorkFlow:
    def __init__(self, worker=None, manager=None):
        self.worker = worker
        self.manager = manager

    def create_task(self, *args):
        self.task_count = len(args)
        for task in args:
            self.manager.create_task(task)

    def process_task(self, **kwargs):
        self.worker.receive_task(**kwargs)

    def single_flow(self, *args, **kwargs):
        self.create_task(*args)
        self.process_task(**kwargs)

    def multi_flow(self, *args, **kwargs):
        m = Process(target=self.create_task, args=args)
        w = Process(target=self.process_task, args=kwargs)
        m.start()
        w.start()
        m.join()
        w.terminate()


if __name__ == "__main__":
    w = Worker('Bob', 'boss')
    m = Manager('Dave', 'employee')
    wf = WorkFlow(worker=w, manager=m)
    wf.multi_flow('test1', 'test2', 'test3')
    # wf.single_flow('test4', 'test5', 'test6')  # todo, add a signal module for stop the single_flow process
