<!--
https://ae01.alicdn.com/kf/Hd06c682f94bc47839555ee6c0b954163f.png
前端
SGV学习（path）
SVG学习之path
path包括直线命令、曲线命令
-->

## SGV学习（path）

> SVG学习之path，path包括直线命令、曲线命令

### 1、直线命令
#### M - 移动到某点
> 用法: M x,y 表示移动到坐标(x, y)上  
> eg: d = "M 20,20"
#### L - 以直线的形式到
> 用法: L x,y 表示以直线的形式滑倒到坐标(x, y)上  
> eg: d = "L 20,20"
#### H - 以水平线的形式
#### V - 以垂直线的形式
#### Z - 终结。直接以直线的形式回到起点

### 3、曲线命令
曲线命令有三个，两个贝塞尔曲线，一个绘制圆弧形
#### C - 三次贝塞尔曲线
> 用法: C x1 y1, x2 y2, x, y 其中的(x1,y1),(x2,y2)表示贝塞尔曲线的两个点，而(x,y)则表示终点   
> eg: d = "C 120 140, 180 140, 170 110"
#### Q - 二次贝塞尔曲线
> 用法: C x1 y1, x, y 其中的(x,y)还是表示终点，而(x1,y1)则表示他们切线相交点   
> eg: d = "C 120 140, 180 140, 170 110"
#### A - 弧线
> 用法: A rx ry rotate angle flag x y   
> 其中 rx ry 表示x轴半径和y轴半径，可以理解为椭圆的两个半径  
> rotate表示旋转  
> angle表示角度是大于还是小于180度，0表示小角度弧，1表示大角度弧  
> flag表示弧线方向，0表示从起点到终点沿逆时针画弧，1表示从起点到终点沿顺时针画弧
> x,y 则还是终点的意思吗  
> eg: d = "A 30 50 0 0 1 162.55 162.45"

### 3、实例
绘制圆形
stroke-dasharray这个属性有点恨。是设置间隔的。  
> stroke-dasharray: 4 1; 表示将原型按5进行比例划分，其中每个5比例中，原path占据5份，一份空白  
> stroke-dasharray: 3 1 1; 同理，在每5个比例中，311划分为黑白黑，后面接着就是3的空白，即白黑白
```html
<style>
.path-loop{
    fill: none;
    stroke: #000;
    stroke-width: 3;
    --x: 0%;
    stroke-dasharray: var(--x) 100%;
    transition: stroke-dasharray 5s ease;
}
svg::hover path{
    --x: 100%
}
</style>
<svg>
    <path class="path-loop" d="M100 40 A 25 25 0 1 1 100 39 Z"></path>
</svg>
```
绘制圆形似乎不能同起点和终点。往前移动一格即可。

### stroke-dasharray - 用于创建虚线
表示虚线长度和每段虚线之间的间距.后面跟的是array的，是因为值其实是数组

### stroke-dashoffset - 偏移
这个属性是相对于起始点的偏移，正数偏移x值的时候，相当于往左移动了x个长度单位，负数偏移x的时候，相当于往右移动了x个长度单位。
