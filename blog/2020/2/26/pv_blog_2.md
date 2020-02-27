<!--
https://ae01.alicdn.com/kf/H3396ce222efd46788d48f98f2c09ff784.png
vue
动态密码生成器
基于Vue实现的动态密码生成器
基于Vue实现的动态密码生成器，能够根据用户设置，来生成长度、类型等均不相同的随机密钥
-->

## 动态密码生成器

> 基于Vue实现的动态密码生成器，能够根据用户设置，来生成长度、类型等均不相同的随机密钥

在开发过程中遇到了一些问题，正好记录下：
* 如何实现动态的跟随按钮
* 如何实现赋值

#### 1、如何实现动态的跟随按钮
* event.clientX: 表示鼠标到浏览器左侧的距离，则clientY表示到浏览器顶部的距离
* event.offsetX: 表示鼠标到触发事件元素左侧的距离
在实现过程中，本来打算直接使用event.offsetX来实现跟随的，但是没有考虑到事件触发机制，事件触发者没有指定。  
导致事件源来回的闪东。 改用clientX，来获取鼠标相对浏览的位置，然后用目标元素的父元素，
调用getBoundingClientRect函数来获取该DOM的相对位置，用二者进行相减得到目标元素的相对位置。

#### 2、js实现赋值
* 先创建一个textarea框，即 document.createElement('textarea')
* 然后赋值，textarea.value = '123'
* 将元素追加到body尾部, document.body.appendChild(textarea)
* 选中元素，textarea.select()
* 执行赋值命令 document.execCommand('copy')
* 最后移除元素 textarea.remove()

#### 3、如何修改原生的input样式
对于<input type="range">这种，如何修改原生的样式  
首先按钮需要消除既有样式，即使用为-webkit-appearance为none，然后修改-webkit-slider-thumb，可以更改按钮样式
```css
.btn{
    -webkit-appearance: none
}
.btn::-webkit-slider-thumb{
    -webkit-appearance: none
    background-image: url('./img.jpg')
}

```

#### 4、其他收获
* 滑动按钮：可以通过label的after/before进行绘制，效果还是不错的
* 棕色+黑色透明，整体颜色还是很好看的
