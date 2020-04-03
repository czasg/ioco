<!--
https://ae01.alicdn.com/kf/Haf4d3b0529ba47669bf69c7bfc71a5f1Y.png
前端
javascript基础
javascript原生的一些知识点，虽然比较简单，但是学习基础是很重要的
javascript原生的一些知识点，虽然比较简单，但是学习基础是很重要的。原生js不适合用来开发，因为需要适配各个浏览器的差异，线上开发还是要用三方包
-->

## javascript基础

> javascript原生的一些知识点，虽然比较简单，但是学习基础是很重要的。原生js不适合用来开发，因为需要适配各个浏览器的差异，线上开发还是要用三方包

#### 浏览器对象
* window不仅是全局作用域，也表示当前浏览器窗口
* navigator对象表示当前浏览器信息，包含一些浏览器的版本，操作系统类型之类的
* screen表示当前屏幕信息
* location表示当前页面的URL信息
* document表示当前页面，其中浏览器以DOM形式表示，则document表示整个DOM树的根节点

1、操作DOM节点  
一般是用来获取对应的节点目标
```javascript
document.getElementById('app')
document.querySelector('#app')
document.querySelectorAll('.app')
```
2、更新DOM节点  
一般更新节点，可以修改对应的css样式，或者操作对应的html，或者仅仅插入对应的文本
```javascript
var node = document.querySelector('#app');
node.innerHTML = '<p>hello world</p>'
node.innerText = 'hello world'
node.style.fontSize = '20px'
```
3、插入DOM节点  
一般是对父节点使用，追加或者是插入某个子节点的前面。有appendChild和insertBefore两个方法
```javascript
var node = document.querySelector('#app');
var new_node = document.createElement('p');
new_node.setAttribute('id', 'new_node');
new_node.innerText = 'hello world';
node.appendChild(new_node);

var currentNode = document.querySelector('#new_node');
currentNode.parentNode.insertBefore(new_node, currentNode)  // 需要调用其父节点的insertBefore方法
```
4、删除DOM节点  
调用父节点的removeChild方法即可

针对input元素，提供`input.value`和`input.checked`等方法

#### 操作文件  
操作文件使用FileReader对象，需要体现注册reader.onload，调用readAsDataURL加载完成后会执行此回调函数

#### Ajax
网络异步请求，通过 XMLHttpRequest 对象来实现。低版本可以使用ActiveXObject  
```javascript
var request = new XMLHttpRequest();
request.onreadystatechange = function() {
    if (request.readyState === 4){
        if (request.status === 200){
            console.log('load success:', request.responseText)
        }
    }
}
request.open('GET', '/api/get/data')
request.send()
```
1、安全限制  
CORS跨域政策，当js向外域发请请求后，浏览器接受响应会首先检查Access-Control-Allow-Origin是否包含本域，如果是，则此次跨域请求成功。

#### Promise
将一个函数包装为Promise对象，当成功或失败时执行对应的回调。若需要继续回调，则对应的返回应该也是一个Promise对象  
我们可以通过then的方式链式的执行逻辑，保证先后序，或者我们可以并行的执行逻辑，如：  
```javascript
// 并发执行
Promise.all([Promise1, Promise2]).then(function(p1, p2) {})
// 仅获取最先完成的
Promise.reac([Promise1, Promise2]).then(function(result) {})
```

#### canvas
对于一个canvas，我们常用的有clearRect擦除、fillRect填充矩阵、fillText填充文本、stroke绘制路径等方法
```javascript
var canvas = document.getElementById('canvas'),
    ctx = canvas.getContext('2d'),  // 拿到一个CanvasRenderingContext2D，绘制2D
    gl = canvas.getContext("webgl");
ctx.clearRect(0, 0, 200, 200);  // 擦除从(0,0)开始，大小为(200,200)的矩形，即变为透明色
ctx.fillStyle = '#000';  // 设置颜色
ctx.fillRect(10, 10, 100, 100);  // 从(10,10)开始，大小为(100,100)的矩形涂色

cxt.shadowOffsetX = 2;  // 此处和css3一致
ctx.shadowOffsetY = 2;
ctx.font = '24px Arial';
ctx.fillStyle = '#333333';
ctx.fillText('带阴影的文字', 20, 40);  // 最后执行填充文字

var path = new Path2D();  // 定义个路径对象
path.arc(75, 75, 50, 0, Math.PI*2, true);
path.moveTo(110,75);
path.arc(75, 75, 35, 0, Math.PI, false);
path.moveTo(65, 65);
ctx.strokeStyle = '#0000ff';
ctx.stroke(path);  // 绘制路径
```







