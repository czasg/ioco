<!--
https://ae01.alicdn.com/kf/Haf4d3b0529ba47669bf69c7bfc71a5f1Y.png
前端
svg旋转按钮
svg旋转按钮。通过circle绘制圆形，然后每个圆形上布置按钮。难点就是如何均匀分布这些按钮
svg旋转按钮。通过circle绘制圆形，然后每个圆形上布置按钮。难点就是如何均匀分布这些按钮
-->

## svg旋转按钮

> svg旋转按钮。通过circle绘制圆形，然后每个圆形上布置按钮。难点就是如何均匀分布这些按钮

#### 结构
第一个svg绘制虚线背景轨道  
第二个svg则是真的动态轨迹  
```html
<div class="middle">
    <div class="container">
        <svg></svg>
        <svg></svg>
        <div class="items">
            <div class="item"><div class="point"></div></div>
            <div class="item"><div class="point"></div></div>
        </div>
    </div>
</div>
```
对于items使用height、width大道100%，填充整个图形  
然后对于每一个item，则使用left、top为50%，使之左顶点位于圆心，
然后设置transform-origin: 0 0即可定位旋转圆心为正圆心。  
设置item的高度为0，长度为 calc(50% + 16px)  
代表item会超过正常圆，然后设置item内部的圆，top: -16px, right: 2px  
这里-16px表示垂直居中、2px表示水平居中，因为stroke-width: 2也是有宽度的

.point也是一个圆形，我们初始时设置transform: scale(0)，隐藏内部细节。
这一步会隐藏掉.point:before的内容，随后设置动画显示出即可。但我们主要显示
的内容，还是在.point:before里面

总体来说就是item移动到中心，并设置左上角为旋转点然后进行旋转，这是中心思想。

### box-shadow - 边框阴影
> box-shadow: h-shadow v-shadow blur spread color inset;  
h-shadow	必需。水平阴影的位置。允许负值。  
v-shadow	必需。垂直阴影的位置。允许负值。  
blur	可选。模糊距离。  
spread	可选。阴影的尺寸。  
color	可选。阴影的颜色。请参阅 CSS 颜色值。  
inset	可选。将外部阴影 (outset) 改为内部阴影。

###  animation - 动画
> animation: name duration func delay count direction fill-mode stats  
> name: 关键帧  
> duration：执行时间  
> func：执行方法，如ease等  
> delay：延迟时间  
> count：播放次数，可以写infinite  
> direction：是否轮流反向播放alternate表示来回交替  
> fill-mode：forwards保留动画，backwards不保留  
> stats：规定暂停或开始running/paused

### 旋转花环
实现原理也是需要画圆，，框架部分  
 
实现旋转花纹的效果：其实就是走马灯的意思，每个花瓣实现灯光的暗灭，定时跑即可。  

问题讲就是这个圆形的设计，有点令人费解，难搞。还是利用上述思维，可以搞定圆圈效果。
置于走马灯，物品发现nth-of-type需要搁在一起才能够定位，不然还是需要单独设置一个class。
