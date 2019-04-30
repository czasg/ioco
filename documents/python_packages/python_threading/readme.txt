from threading import Thread, current_thread
current_thread().name  -> it will return the current thread name, first is main thread, which name is MainThread
t = Thread(target=func, name=threadName)  -> by this way, you can appoint the thread name when you new one
t.start()
t.join()

from threading import Lock
lock = Lock()  -> when you want to manage the public variable, you need this function
lock.acquire()  -> get lock
lock.release()  -> release lock

import threading
local = threading.local()  -> this is manager when you need to delivery params inside one thread
local.param = param  -> define it in one function
param = local.param  -> then you can get it in other function directly rather than delivery it


The Second Way To Calling Thread, By Class To Inherit
class MyThread(threading.Thread):
    def __init__(self, test):
        super(MyThread, self).__init__()
        self.test = test
    def run(self):  # you must define what the thread do in run function
        doSomething()



