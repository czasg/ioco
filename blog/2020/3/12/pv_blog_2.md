<!--
https://ae01.alicdn.com/kf/H2bfbd8cbeb74440f92b2b445b98aeddbT.png
python
concurrent学习
包含线程池和进程池，内部还有多种锁，threading.Lock、threading.Condition等
包含线程池和进程池，内部还有多种锁，threading.Lock、threading.Condition等
-->

## concurrent学习

> 包含线程池和进程池，内部还有多种锁，threading.Lock、threading.Condition等

#### 线程锁
锁只有共同使用一把的时候，才能相互解锁，如果新创建了一个锁对象，或者不同的锁对象，那么其实各自实现各自锁逻辑。

1、threading.Lock  
原始锁。在锁定是不属于特定线程的同步基元组件。只有`acquire`和`release`两种方法。具有原子性！

这里不属于特定线程的意思就是，该锁可以被任意线程释放。如果在某个上锁的线程中再次开启新线程，是可以执行的，
而且在新线程中不能上锁，但可以释放锁。

2、threading.RLock  
![重入锁](https://ae01.alicdn.com/kf/Hc085cd5ce8544edca36880ae2e60014e0.png)
重入锁。如果使用python重写，则是基于Lock原始锁实现的。  

重入锁只允许持锁的当前线程来释放。而持锁的当前线程，再次获取锁对象时，并不会阻塞，而是重入锁内部维护锁计数+1  

不同线程申请重入锁时，首先会判断当前线程是否为持锁线程，不是则调用原始锁申请锁并等待，知道持锁线程释放，然后再获取锁。
获取锁后，会更新重入锁内部对象信息。

3、threading.Condition  
![条件锁](https://ae01.alicdn.com/kf/Hb6e8ca83c96049b68c38dae7f25c16acO.png)
条件锁。再内部维护一个waiter队列，每当有线程调用wait函数的时候，会重新获取一个原始锁，并将其推到waiter队列。
然后释放重入锁，紧接着再次申请获取到的原始锁，进入死锁状态。

eg：  
线程1持锁重入锁，并调用wait函数，申请原始锁，释放重入锁，原始锁死锁  
线程2申请重入锁，并调用notify  
线程1原始锁解锁，申请重入锁，此时被线程2持有，进入等待  
线程2释放重入锁  
线程1获取重入锁

4、threading.Event  
![事件锁](https://ae01.alicdn.com/kf/H4dc474fd3ead451f9a570a37d6b51520D.png)
事件锁。内部使用条件锁，则其底层使用原始锁。本质上事件锁并不影响线程之间的运行，每一个函数的运行都有内置的条件锁。

set，申请条件锁，flag=True，然后调用notify_all释放所有等待队列中的原始锁。  
clear，申请条件锁，flag=False。  
wait，申请条件锁，如果flag=False，则调用条件锁的wait，进入等待队列。


#### Executor  
这个execute基类中，exit很重要，每次上下文管理器结束时，都会执行一次self.shutdown函数

executor - ThreadPoolExecutor - 内部有一把_shutdown_lock原始锁。  
分别在submit和shutdown中上锁，这把锁的目的就是为了防止创建线程和结束ThreadPoolExecutor时的冲突。  
属于主线程所有。

#### Future
每一个未来对象中，都有一把属于自己的条件锁，所有参数中较为重要的就是waiter队列。

条件锁，在创建新线程的set_result、主线程的_AcquireFutures中上锁。条件锁在同一线程中不会死锁。
但是不同线程会阻塞。

分场景：  
在执行_AcquireFutures之前就完成了任务。此时由线程1持条件锁，执行对未来对象赋值操作，然后释放。
接着主线程申请并持条件锁，检查当前未来对象的状态，是不是已经完成的，是的话则剔除，剩下的未完成的，
执行创建并安装waiter流程。每一个future共享一个waiter，然后释放future的条件锁，让其他线程可以持锁写数据，
此时waiter也在主线程中wait阻塞。直到其他线程触发set_result函数，释放阻塞在主线程的waiter持有的事件锁。

#### 等待对象
没以waiter对象中，有一把最基础的事件锁，主要用在主线程锁住，然后再其他线程中调用set_result，才释放锁。

分场景：  
1、all_complete：（lock -> 线程）  
其本意是只有当所有的未来对象都完成其任务后，才会返回结果。  

其waiter额外配置由一把原始锁吗，用来锁住创建的新线程，因为当他们完成任务需要set_result写数据的时候，
需要共同修改公共数据total_threads，也即是待处理任务量，当任务量为0的时候，会触发事件锁，释放主线程。

2、as_complete：（lock -> 线程/主线程）  
其本意是当由未来对象完成任务后，立即返回，然后阻塞等待他们未来对象完成时，又可以返回其结果，直至完成所有任务。

其waiter也配置由一把原始锁，用来锁住创建的新线程和主线程两个地方。再线程中，每次只允许一个线程来写数据，
即只有一个线程能够触发set_result函数，而主线程也调用了waiter.lock，表示主线程和线程，只能由一个线程能够执行逻辑。

线程往里面写数据，而主线程时往里面拿数据，二者只能由一个进行。

3、first_complete：（no lock）  
其本意是只要由一个未来对象完成，即立即返回。

每次子线程完成后，调用set_result，即会立即释放主线程的事件锁。

#### asyncio

