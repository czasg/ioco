<!--
https://ae01.alicdn.com/kf/Ha92f087c8f84421e80d0449d2fa77dccl.png
vue
css动态赋值
动态滑动按钮type="range"，对css赋值修改样式
动态滑动按钮type="range"，对css赋值修改样式。包括-webkit-slider-thumb、-webkit-slider-runnable-track的修改，还有var和attr两个赋值方法
-->

## css动态赋值

> 动态滑动按钮type="range"，对css赋值修改样式。包括-webkit-slider-thumb、-webkit-slider-runnable-track的修改，还有var和attr两个赋值方法

css动态赋值的方式有两种，一种通过style进行赋值，还有一种通过属性赋值
### 1、赋值方式
需要使用--开头定义样式
```html
<style>
    .box{
        --x: 0;
        --y: 0;
    }
    .box:before{
        content: attr(data-length);
    }
    .box:after{
        content: var(--x, 'default');
    }
</style>
<div class="box" data-length="0"></div>
```
如上两种方式即可完成赋值，样式通过var的方式进行赋值，可以指定默认值  
而属性，则可以通过attr的方式获取，都需要在同一个标签内

### 2、修改按钮样式
* -webkit-appearance: 原生样式，需要指定为none后才可以修改
* -webkit-slider-thumb: 按钮
* -webkit-slider-runnable-track: 按钮滑动轨道

### 3、其他
使用column-count：可以指定列数，实现瀑布式效果，但是不友好  
还有column-gap，指定各列之间的间隔。
