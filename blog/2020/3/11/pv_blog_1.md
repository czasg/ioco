<!--
https://ae01.alicdn.com/kf/H413f0f5efa724ffe8ae7f450778a07448.png
数据结构|java
HashMap和字典
java中的HashMap和python中的dict，有很大的相似之间，可以一起学习
java中的HashMap和python中的dict，有很大的相似之间，可以一起学习
-->

## HashMap和字典

> java中的HashMap和python中的dict，有很大的相似之间，可以一起学习

#### 简单实例
1、Java  
```java
HashMap<String, String> map = new HashMap<String, String>();
map.put(  'key1', 'value1' );
map.put(  'key2', 'value2' );
```
通过上述代码，我们可以得到数据结构如下
```json
{
  "key1": "value1",
  "key2": "value2"
}
```

2、Python  
```python
map = dict(key1="value1", key2="value2")
```

#### 底层简单原理
底层的基础数据结构还是数组，不过是习稀疏数组，即数组内部很多空间是滞空状态，未被使用。

再赋值和取值的时候，会先根据 key 值计算出一个 hash 值，然后根据此 hash 值对数组进行取模，
就会定位到数组中的一个元素中去。  
赋值：`array[3] = <key1, value1>`  
取值：`return array[3]`

#### jdk1.8寻址算法优化
```java
static final int hash(Object key){
    int h;
    return (key == null) ? 0 : (h = key.hasCode()) ^ (h >>> 16);
}
```
原来的算法：计算hash，然后取模运算。  
优化后算法：计算hash，然后右移16位，将二者进行异或运算。  

`hash & (n - 1)`的效果和 hash 对 n 取模的效果是一样的。但运算性能要比取模高很多。  
数组长度是2的n次方，则保持数组长度是2的n次方，则二者对于上述条件是成立的。

但是原算法中，不能直接采用与计算，因为原算法中，高16位二进制，在取模算法中基本无法发挥作用。
一旦出现两个hash值，仅仅高16位存在部分不同，则会导致hash冲突  
优化后算法，高16位与低16位进行异或运算后，会同时保留二者的特征，就避免上述情况。

#### HashMap如何解决hash碰撞
1、基本情况：  
底层是一个数组，然后对key进行hash，并和（n - 1）进行与运算后，计算得到位置。然后一旦两个key计算得到得位置相同。
则称之为hash冲突或hash碰撞。此时会在value位置，挂一个链表，并将数据放进链表中。get得时候，如果发现是一个链表，
则遍历该链表直到找到自己所需数据即可。

2、优化后：
当某个value中链表达到一定长度，可以将其转化位红黑树结构，此时查询效率会变为O(log(n))

#### HashMap如何扩容
一般是2倍扩容。底层是数组，当数组满了之后，可以进行扩容，编程一个更大得数组，存放更多得数据。  

但是在扩容得时候，需要进行rehash计算。即某些value内部可能是链表结构，或者红黑树结构。
则需要对值进行rehash运算，运算规则还是：计算hash值，高16与低16位异或运算得出新得hash值，
然后该值与新数组长度得（n-1）进行与运算，计算得出新得数组位置。后续规则不变，一旦出现hash碰撞，
则以链表得结构进行存储。当链表达到一定长度，可以转为红黑树，增加查询效率。

![HashMap](https://ae01.alicdn.com/kf/Hf840473fc8f44ae39b03c7b1d16c9dafN.png)