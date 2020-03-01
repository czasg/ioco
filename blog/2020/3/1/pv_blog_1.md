<!--
https://ae01.alicdn.com/kf/H46b03db65df345d8915c1d803a9c8b16u.png
前端
鼠标跟随变脸
前端学习，鼠标滑动，根据相对位置变化脸色
前端学习，鼠标滑动，根据相对位置变化脸色，常规css动画实现不了，需要使用js方法requestAnimationFrame
-->

## 鼠标跟随变脸

> 前端学习，鼠标滑动，根据相对位置变化脸色，常规css动画实现不了，需要使用js方法requestAnimationFrame

浏览器在下次重绘之前调用指定的回调函数更新动画。该方法需要传入一个回调函数作为参数，该回调函数会在浏览器下一次重绘之前执行

### 1、requestAnimationFrame
我们只需要修改对应的css样式，动画的渲染则交给浏览器执行。

### 2、笑脸结构
.face标签，我们设置为圆，然后定义其::after，再内部绘制一个由上到下的，绿->白  
.eye标签，绘制眼白，然后再::after，绘制眼珠  
.mouse标签，绘制一个矩形，然后调用border-radius，四个值：左上角，右上角，右下角，左下角
```html
<div class="face">
    <div class="eye-left"></div>
    <div class="eye-right"></div>
    <div class="mouse"></div>
</div>
```
如果想要绘制切割形状，可以调用xlip-path方法。  
```clip-path: polygon(50% 0,100% 50%,50% 100%,0 50%);```

### 3、js结构
调用Vue来绑定相关的属性，然后早mounted中调用equestAnimationFrame方法来执行动画。  
每次页面更新时都会调用相关的想法来实现动画，而不是transition，因为会有延迟。
