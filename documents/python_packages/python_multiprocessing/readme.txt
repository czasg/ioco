from multiprocessing import Process
p = Process(target=func, args=(params,))  -> create subprocess
p.start()
p.join()

from multiprocess import Pool
p = Pool(4)
p.apply_async(func, args=(params,))
p.close()  -> must be call before p.join(), it mean you can't add other new process in this main line
p.join()

import subprocess
this is a way for user to control the input&output in subprocess, ignore temporary

from multiprocess import Queue, Process
q = Queue()
worker = Process(target=func, args=(params,))
manager = Process(target=func, args=(params,))
worker.start()
manager.start()
worker.join()
manager.join()

multiprocessing.cpu_count()  -> in this way, you will get the statistic num of you cup


from multiprocessing.managers import BaseManager
class QueueManager(BaseManager): pass  -> it needn't define anything, just inherit
QueueManager.register('func_name', callback=lambda: Queue)  -> There exist bug
QueueManager.register('func_name')
m = QueueManger(address=(ip, port), authkey=b'123')
m.start()  -> if you are publisher and manager, starting it
m.connect()  -> in this case, worker will go here to connect the host
queue = m.func_name()  -> so you can operate the queue by this way

callback=lambda: Queue  -> window has no fork(), it will imitate this func such as pickle
so it will raise error when you run it in Window just because pickle can't serialize lambda func
you need structure a new func rather lambda