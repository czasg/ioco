<!--
https://ae01.alicdn.com/kf/Hdc8f1b555aea4e389287d2a84331da62i.png
vue
动态菜单设计
可伸缩，弹出。并针对者两种样式配置不同的css样式，实现不同的效果。
可伸缩，弹出。并针对者两种样式配置不同的css样式，实现不同的效果。主要由spread和shrink两个主类进行控制。
-->

## 动态菜单

> 可伸缩，弹出。并针对者两种样式配置不同的css样式，实现不同的效果。

#### 菜单
根据不同的class类，指定不同的样式。
* spread为伸展
* shrink为收缩
```html
.spread{
    width: 200px;
}
.spread .item-box-body{
    max-height: 0;
}
.spread > .menu-item:hover .item-box-body{
    max-height: 180px;
}


.shrink{
    width: 60px;
}
.shrink .menu-item-box{
    opacity: 0;
    width: 0;
    position: absolute;
    left: 60px;
    transition: opacity .5s ease;
}
.shrink > .menu-item:hover .menu-item-box{
    width: 200px;
    opacity: 1;
    border-left: 3px solid #fff;
}
```

#### svg
svg是绘制出来的，可以根据计算规则绘制动画路径，然后控制起点，长度来实现动画的展示。  
但是如何制作svg，这个是个问题
```html
<style>
svg > path{
    fill: none; 控制背景填充
    stroke: #fff; 控制线条颜色
    stroke-width; 控制线条宽度
    stroke-linecap: round; 控制两端样式为圆
    stroke-linejoin; round; 控制交汇处为圆
    stroke-dasharray: x,y; 控制虚线?
    stroke-dashoffset: 100; 控制起始位置?
}
</style>
```
