<!--
https://ae01.alicdn.com/kf/H78b31e912d92482cbffe0837b4675798I.png
计算机基础
TCP粘包与拆包
TCP是面向连接的，面向流的，提供高可靠性服务。UDP是无连接的，面向消息的，提供高效率服务。
TCP是面向连接的，面向流的，提供高可靠性服务。UDP是无连接的，面向消息的，提供高效率服务。
-->

## TCP粘包与拆包

> TCP是面向连接的，面向流的，提供高可靠性服务。UDP是无连接的，面向消息的，提供高效率服务。

tcp的协议数据不会丢，没有收完包，下次接收，会继续上次继续接收，
接收放总是在收到ack时才会清除缓冲区内容。数据是可靠的，但是会粘包。

#### 粘包情况
1、发送方缓冲区未满  
当每次发送数据很小的时候，发送间隔很短的时候，会被北部优化算法，会产生粘包，即两条消息会被合成一条。
```python
import socket
server, client = socket.socketpair()
client.send(b'hello')
client.send(b'world')
data1 = server.recv(10)
```
此时client端发送的两次数据会被合并为：b"helloworld"

2、接收方未及时接收  
即服务端第一次只拿了一部分，剩下包与之后的包，产生粘包。
```python
import socket
server, client = socket.socketpair()
client.send(b'hello')
client.send(b'world')
data1 = server.recv(4)
data2 = server.recv(4)
print(data1, data2)
```
此时接收方数据就发生紊乱，不清楚那些数据属于哪个包。

#### 解决方法  
传输数据时，以二进制为例，计算数据的长度，然后将长度也计算一个固定长度的掩码，
传输数据时将掩码+数据一同发送过去即可。

如websocket协议中，数据头一般长度为2，根据该数据第二个字节，来确定数据长度。  
根据数据的长度，分为三种：  
1、原始数据长度小于126，则该第二位字节，即代表数据的长度。  
2、原始数据长度 大于125 小于65536，则第二位字节为126，且后2位字节代表数据的长度。  
3、否则，第二位字节为127，则后8位字节代表数据的长度。
```java
if(length<126){
    pushHead=new byte[2];
    pushHead[0]=buff[0];
    pushHead[1]=(byte)x.getBytes("UTF-8").length;
    out.write(pushHead);
}
else if(length>125 && length<65536){
    pushHead=new byte[4];
    pushHead[0]=buff[0];
    pushHead[1]=(byte)126;
    pushHead[2]=(byte)((length>>8) & 0xFF);
    pushHead[3]=(byte)(length & 0xFF);
    out.write(pushHead);
}
else if(length>65535){
    pushHead=new byte[10];
    pushHead[0]=buff[0];
    pushHead[1]=(byte)127;
    pushHead[2]=(byte)((length>>56) & 0xFF);
    pushHead[3]=(byte)((length>>48) & 0xFF);
    pushHead[4]=(byte)((length>>40) & 0xFF);
    pushHead[5]=(byte)((length>>32) & 0xFF);
    pushHead[6]=(byte)((length>>24) & 0xFF);
    pushHead[7]=(byte)((length>>16) & 0xFF);
    pushHead[8]=(byte)((length>>8) & 0xFF);
    pushHead[9]=(byte)(length & 0xFF);
    out.write(pushHead);
}
```

#### struct
在python中，有struct模块用于数据的打包

|格式|标准大小|
|---| --- |
|B|1|
|H|2|
|L|4|
|Q|8|

```python
import struct

data = "CzaOrz"
length = len(data)  # 6

format = "B"

mask = struct.pack(format, length)
unpack, = struct.unpack(format, mask)
```