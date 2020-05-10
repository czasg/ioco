<!--
https://ae01.alicdn.com/kf/Haf4d3b0529ba47669bf69c7bfc71a5f1Y.png
职场
前端面试复习
前端涉及到的知识点非常的多，需要沉下心来好好学习
包括网络、设计模式、安全、javascript基础、css基础、框架vue等
-->

## 前端面试复习

> 前端涉及到的知识点非常的多，需要沉下心来好好学习。包括网络、设计模式、安全、javascript基础、css基础、框架vue等

#### 网络
* 常见的状态码有哪些
    * 1开头表示指示信息，表示请求已接收，需要继续处理
    * 2开头表示请求已被成功接收处理
    * 3开头表示请求更进一步处理，即被重定向
    * 4开头表示客户端出现错误
    * 5开头表示服务端出现错误
    * 100请求者应当继续提出请求
    * 101切换协议，请求者要求服务器切换协议，服务器已确认并准备进行切换
    * 200表示此次请求成功
    * 201表示资源被正确创建，比如post请求创建用户，创建成功即可返回201
    * 202表示请求时正确的，但是结果正在处理中，客户端可以通过轮询等机制继续请求
    * 300表示请求成功，但结果有多种选择
    * 301表示请求成功，但是资源被永久转移
    * 302表示服务端要求客户端重新再发一个请求，即重定向
    * 303使用GET来访问新的地址来获取资源
    * 304表示请求资源并没有被修改过，可以使用缓存
    * 400表示客户端请求的语法有问题，不能被服务器理解，比如请求头不对等
    * 401表示此次请求未被授权，没有提供认证信息，如没有带上token等
    * 为以后需要所保留的状态码
    * 403表示请求资源不允许访问。即服务端接收到了请求，但是拒绝提供服务
    * 404表示请求资源不存在
    * 500表示请求资源找到了，服务端发生了未知错误
    * 501表示请求还没有被实现
    * 503表示服务端当前不能处理客户请求，一段时间后可能恢复
* 304表示什么-和302有什么区别
    * 302表示客户端需要再次发起一次请求
    * 304表示客户端直接从缓存中拿到结果
* 介绍一下HTTP的缓存策略
* connect为keep-alive
* 介绍下DNS
* TCP三次握手四次挥手
* HTTPS工作原理
* CND是什么以及应用场景
* CND回源是什么
* 输入URL到页面展示

#### 设计模式
* vue和react中的应用有什么设计模式

#### 数据结构
* 栈-队列-链表-树
* 用javascript实现?

#### 算法
* 排序算法和复杂度
* 二叉树前中后序3遍历
* 深度优先和广度优先的思路和应用场景
* 动态规划

#### 安全
* CORS
* XSS
* CSRF
* HTTPS
* 风控策略
* 可信前端
* 前端-服务端的安全策略

#### javascript基础
* 浏览器如何渲染页面
* 垃圾回收机制
* JSONP原理，为啥不是真正的ajax
* 什么是同源策略
* null和undefined
    * null和undefined都可以表示值得空缺，undefined是系统级的，表示错误的空缺，null则是开发级别的空缺值
* document.write和innerHTML区别
    * document.write是直接写入到页面的内容流，如果写之前没有调用document.open，则浏览器自动调用open，
    每次写完后自动调用该函数，会导致页面被重写
    * innerHTML是DOM元素的一个属性，代表该DOM节点的html内容
* cookie，sessionStorage，localStorage
    * cookie
    * sessionStorage
    * localStorage
    * 存储大小
    * 过期时间
    * 数据与服务器之间的交互
* 拖拽事件
    * drag在整个拖拽期间都会触发此事件
    * dragover在目标元素时，会持续触发此事件。无论时拖拽元素还是目标元素，在元素内就会持续触发
    * dragenter拖拽过程中，进入目标元素时会触发此事件
    * dragleave拖拽过程中，离开目标元素时会触发此事件
    * 拖拽元素
        * dragstart拖拽开始时会触发此事件
        * dragend
    * 目标元素
        * drop
* 事件代理
    * 事件冒泡，当子元素的事件被触发后，该事件会从事件源开始逐级向上传播，触发父元素的相关事件
    * 将事件绑定到目标父元素上，利用冒泡机制触发该事件。比如有一个菜单栏，要监听每一个栏目的事件，
    可以为每一个栏目添加监听事件，也可以通过冒泡机制，在其父元素做监听。
* 宏任务和微任务
    * 这是js异步模型的概念，也叫事件驱动模型，内部有一些消息事件循环，
    只有当某些事件触发后才会执行，执行完后回重复监听继续执行其他事件。
* 继承的方式
    * 构造函数，使用call或者apply，将父对象的构造函数绑定在子对象上
    * 原型继承，对子对象的原型prototype指向父对象的一个实例
* 执行上下文
* 作用域链
* 闭包及应用场景
* this-call-apply-bind
* 原型和继承
* Promise
* 深浅拷贝，如何实现及解决循环引用的问题
* 事件机制-宏任务和微任务
* 数组的方法

#### css基础
* document.onready和window.onload
* meta标签
    * 提供关于html文档的元数据，不会显示在页面上，但是对于及其是可读的，告诉机器如何解析该页面
* css选择符有那么，优先级算法如何计算
* margin重合问题
* 样式覆盖规则
    * 标签选择器 - 1
    * 类选择器 - 10
    * id选择器 - 100
    * 内联样式 - 1000
    * 伪元素(:first-children) - 1
    * 伪类(:link) - 10
* calc，support，media
    * calc函数，可用于动态计算长度值
    * support主要用于检测浏览器是否支持css的某个属性，属于条件判断的一种
    * media针对不同的媒体类型定义不同的样式
* css水平居中与垂直居中
    * 水平居中
        * 内联级元素，text-align: center
        * 块级元素，margin: 0 auto
        * position:absolute + left:50% + transform:translateX(-50%)
        * display:flex + justify-content:center
    * 垂直居中
        * 内联级元素，将line-height设置为父级高度
        * position:absolute + top:50% + translate:translateY(-50%)
        * display:flex + align-items:center
        * display:table + display:table-cell + vertical-align:middle
* rem,em,vh,px各有什么含义
    * 1rem，即全部的长度都相当于根元素html，通常给html元素设置一个字体大小，然后其他元素的长度单位就是rem
    * em
        * 子元素的字体大小，其em是相对于父元素的字体大小
        * 当前元素的width、height、padding、margin等em是相对于该元素的font-size而定
    * vw/vh，全称为viewpoint width/height，表示当前设备的宽高
    * px像素，相对长度单位，像素px是相对于显示器屏幕分辨率而言的
* 画一条0.5px像素的直线
    * height:1px + transform:scale(.5)
* 画一个三角形
    * height:0 + width:0 + border:100px solid + border-color:#f1f1f1 transparent transparent transparent
    * clip-path
        * 多边形，ploygon(x y, x y, x y)，xy是坐标，可以使用%
        * 圆形，circle(r at x y)，r是半径，xy则是圆心
        * 椭圆，ellipse(w h at x y)，w为水平宽度，h为垂直宽度，xy为椭圆圆心
        * 矩形，inset(x y z p)，x为top距离，y为right距离，z为bottom距离，p为left距离
* 盒模型
    * 组成，由外之至内，margin、border、padding、content，一般常说的width是指的content
    * 
* 清除浮动
    * clear:both
    * 父级设置足够的高度
    * 创建父级BFC(overflow:hidden)，块级格式化上下文，他是一个独立的渲染区域，让处于内部的元素相互隔离，
    使内部元素的相互定位不会相互影响
* label标签的作用
    * 方便鼠标点击使用，可以扩大鼠标的点击范围
* css sprites
    * 将网页中的一些背景图片整合到一张图片文件中，再利用css的background-position/size等方法定位到目标图篇获取。
    可以节约宽带，提高用户加载速度和体验，而不需要加载更多图片，适用于一些logo图片之类的
* position
* 行内元素和块元素
* flex布局
* 如何使用flex实现9宫格布局
* flex:1 是指什么
* flex-shrink和flex-basic属性
* grid布局
* 移动端的ipx是怎么解决的
* rem和vw方案，各有什么优缺点
* rem方案的font-size是挂在哪
* rem方案时移动端字体是如何处理的
* 重绘回流，什么是重绘和回流，如何避免
* 居中的几种常见布局
* 层叠上下文，z-index
* sass和less

#### vue框架
* react和vue的区别
* mvvm和mvc的区别
* 生命周期中nextTick如何实现的
* 父子组件挂载，生命周期顺序如何
* 数据绑定中，双向绑定如何实现，即数据劫持和发布订阅
* 数组和对象的数据观察有什么特殊处理
* defineProperty和proxy有什么区别
* vue中数据频繁更新，但最后为什么只会更新一次
* 状态管理，什么是状态管理，为什么需要状态管理
* vuex和redux的区别
* 如何实现简单的状态管理
* 父子组件如何实现通信
* 爷孙组件如何实现通信
* 兄弟组件如何实现通信
* virtual DOM是什么，为什么要有，解决了什么问题
* vue的diff策略，和react有什么不同
* key有什么用
* vue的computed计算属性和watch是如何实现的
* react hook是什么
* vue和react有什么不同，如何考虑选型

#### 工程化
* webpack构建流程
* 热更新是如何实现的
* webpack如何做性能优化
* 前端页面是如何发布到线上的
* weex是什么，为什么比h5块，有什么缺点

#### 性能优化
* 优雅降级和渐进增强
    * 优雅降级，相当于向下兼容。一开始就构建站点的完整功能，然后根据浏览器及其版本的不同，去除相关的功能实现兼容
    * 渐进增强，相当于向上兼容。一开始就针对地板构建页面，完成基础功能，然后针对高级浏览器进行构建
* 打包优化
    * webpack
        * loader
        * dll
        * happypack
        * 压缩代码
        * tree shaking
    * 图片base64、cnd
* 网络优化
    * dns
    * cdn
    * 缓存
    * preload、prefetch、懒加载
    * ssr
* 代码优化
    * 懒加载
    * dom、style批量更新

#### typescript
* typescript是什么，和js相比优缺点如何
* 什么是泛型
* 接口interface
* d.ts是什么
* 如何编译的
* namespace/module












