<!--
https://ae01.alicdn.com/kf/H0bdd65cb0b4e4801aa5b2d093defdf4dK.png
计算机基础
代理及负载均衡
代理包括正向代理和反向代理，负载均衡则包括http重定向、DNS负载均衡、反向代理等
代理包括正向代理和反向代理，负载均衡则包括http重定向、DNS负载均衡、反向代理等
-->

## 代理及负载均衡

> 代理包括正向代理和反向代理，负载均衡则包括http重定向、DNS负载均衡、反向代理等

#### 正向代理
客户端通过一个代理服务器，范问目标服务器，从而获取请求结果的过程。
![正向代理](https://ae01.alicdn.com/kf/H7ccd87bfe73c4649832448705d670c24f.png)

#### 反向代理
客户端访问目标服务器，而目标服务器实则是一个反向代理服务器，他接受用户的请求，并转发给真正处理请求的服务器。
![反向代理](https://ae01.alicdn.com/kf/Hefbe092240a84627b5c4de9e60567c90A.png)

### 负载均衡

##### 1、基于第七层交换技术的负载均衡  
![nginx](https://ae01.alicdn.com/kf/H485b67951bd4477da96e31ce4f8cdff0I.png)
以flask为例，flask是基于WSGI标准搭建的web后端应用框架。WSGI标准由werkzeug实现。
我们从socket角度来讲，服务端挂起socket监听服务，一次http请求就是，服务端监听到请求，读取请求的http报文数据，
转成WSGI标准能够接收的形式，也就是一个environ和一个start_response，一共两个参数。再转交给flask应用进行处理。
然后生成响应的响应报文返回。

然后负载均衡，以flask+uwsgi+nginx为例，nginx扮演的角色，和werkzeug扮演的差不多，
也是监听请求，但是并不对请求做任何处理，他做的仅仅是转交此次请求，如转给uwsgi处理请，
生成WSGI标准数据后，在转交给flask处理。

负载均衡的实际作用就是在应用层分发接受到的请求。所以他是基于第7层交换技术的负载均衡。

##### 2、基于第四层交换技术的负载均衡  
![LVS](https://ae01.alicdn.com/kf/H341653dde48844268bf9558369ad89e8V.png)
第四层也就是传输层。lvs，在负载均衡服务器中，修改报文中的IP、端口、MAC地址等方式，转发请求。  
2.1、VS/NAT（Virtual Server / Network Address Translation）  
网络地址翻转技术。在direction server中，将客户端请求数据包中的IP地址和端口，修改为real server服务器的IP和端口。
real server处理完后返回响应报文给direction server，再由direction server将数据包中的源地址和源端口改为客户但的地址和端口。

每次请求都需要通过direction server。和nginx功能类似，类似一个中转站。

2.2、VS/TUN（Virtual Server / Tunneling）  
IP隧道技术，即和NAT基本一样，不过响应报文直接返回给客户端服务器，不经过direction server。

相比于NAT，大大较少了direction serve服务器的压力

2.3、VS/DR（Virtual Server / Direct Routing）  
路由技术，即直接修改请求数据包中的MAC地址，将请求转交给real server。
而响应报文直接返回给客户端服务器。

##### 3、http重定向  
通过Location报文头，指向真正的工作服务器。

##### 4、DNS负载均衡  
DNS服务器中，多个IP地址配置同一个域名。但是DNS负载均衡无法考虑到真是服务器的性能，
性能最差的那台服务器，将成为性能瓶颈。

