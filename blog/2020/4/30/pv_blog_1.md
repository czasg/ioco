<!--
https://ae01.alicdn.com/kf/Haf4d3b0529ba47669bf69c7bfc71a5f1Y.png
vue
vue源码学习（一）
vue给dom节点建立了一个数据模型，开发并不直接操作dom而是修改对应的数据模型即可
vue给dom节点建立了一个数据模型，开发并不直接操作dom而是修改对应的数据模型即可
-->

## vue源码学习（一）

> vue给dom节点建立了一个数据模型，开发并不直接操作dom而是修改对应的数据模型即可

##### 数据监测
vue的数据监测利用了js提供的特殊方法`Object.defineProperty`，可以直接修改对象的相关属性，包括：
是否可遍历、是否可修改、是否可删除，还有setter和getter两个拦截器。本质上和观察者模式还是有点像的。

但是js提供的方法，无法监测新增的数据变化、数组内部元素的数据变化，所以真对Object，vue提供了`$set`和`$delete`等方法，支持数据监测。
而真对Array，vue则修改了原生Array的原型，在其之上做了一个拦截器，同样支持依赖的收集与update

##### 虚拟DOM
虚拟DOM和原生DOM的区别，原生DOM是浏览器所支持的对象，内部包含复杂的属性与结构，而虚拟DOM则是由js来描述一个原生DOM节点。
描述并不会完全模仿，而是将主要的属性和特征摘取，如tag、attrs、text、children等

之所使用虚拟DOM，就是为了避免大面积的直接操作原生DOM节点，所以虚拟DOM的出现，就是利用了js的计算性能来换取操作DOM所消耗的性能。

##### VNode
vue中的虚拟节点，可以描述各种类型的真实DOM节点，包括元素节点、文本节点、注释节点等。  

在视图渲染之前，把写好的template末班先编译为VNode并缓存，然后当数据发生变化需要重新渲染的时候，我们先比对新旧VNode，
找出最终需要重新渲染的节点，然后根据差异创建出新的DOM节点再插入到视图中，完成一个视图更新

而在vue中针对VNode的差异对比，有一个dom-diff的过程，主要做了三件事：创建节点、删除节点、更新节点

##### 模板编译
将template中的内容，先编译为抽象语法树AST，然后对AST中的静态节点打上标记，最后生成render渲染函数，也就是一段字符串

对于模板字符串，vue采用正则的方式来解析，比如遇到<div>就认为是一个start标签，遇到一个</div>则认为是一个结束标签，  
对于开始标签，会生成包含tag、attrsList、children等的AST
```javascript
export function createASTElement (tag,attrs,parent) {
  return {
    type: 1,
    tag,
    attrsList: attrs,
    attrsMap: makeAttrsMap(attrs),
    parent,
    children: []
  }
}
```

而对于文本类型的AST
```javascript
if(res = parseText(text)){
    let element = {
        type: 2,
        expression: res.expression,
        tokens: res.tokens,
        text
    }
} else {
    let element = {
        type: 3,
        text
    }
}
```
比如：带有`{{}}`标记的文本，我们即可认为是动态文本  
expression属性就是把文本中的变量和非变量提取出来，然后把变量用_s()包裹，最后按照文本里的顺序把它们用+连接起来。  
tokens是个数组，数组内容也是文本中的变量和非变量，不一样的是把变量构造成{'@binding': xxx}。
```javascript
let text = "我叫{{name}}，我今年{{age}}岁了"
let res = parseText(text)
res = {
    expression:"我叫"+_s(name)+"，我今年"+_s(age)+"岁了",
    tokens:[
        "我叫",
        {'@binding': name },
        "，我今年"
        {'@binding': age },
    	"岁了"
    ]
}
```
expression和token主要是为了给后面的渲染函数render使用  
具体的判断还是使用的正则，会提供一个delimiters。表示动态文本的识别符号

注释类型的AST
```javascript
comment (text: string) {
    let element = {
        type: 3,
        text,
        isComment: true
    }
}
```

如何根据AST生成渲染函数，
```javascript
<div id="NLRX"><p>Hello {{name}}</p></div>
ast = {
    'type': 1,
    'tag': 'div',
    'attrsList': [
        {
            'name':'id',
            'value':'NLRX',
        }
    ],
    'attrsMap': {
      'id': 'NLRX',
    },
    'static':false,
    'parent': undefined,
    'plain': false,
    'children': [
        {
            'type': 1,
            'tag': 'p',
            'plain': false,
            'static':false,
            'children': [
                {
                    'type': 2,
                    'expression': '"Hello "+_s(name)',
                    'text': 'Hello {{name}}',
                    'static':false,
                }
            ]
        }
    ]
}
```
如何根据已有的AST生成渲染函数，
```javascript
/*
* _c()可以创建一个元素型VNode
*/
_c('div',{attrs:{"id":"NLRX"}},[])
_c('div',{attrs:{"id":"NLRX"}},[_c('p'),[]])
_c('div',{attrs:{"id":"NLRX"}},[_c('p'),[_v("Hello "+_s(name))]])
```
最后我们通过这种递归的形式得到了render函数的字符串，而具体如何执行这个渲染函数，我们可以使用`new Function(code)`来完成
```
with(this){
    return _c(
        'div',
        {
            attrs:{"id":"NLRX"},
        }
        [
            _c('p'),
            [
                _v("Hello "+_s(name))
            ]
        ])
}
```

根据AST生成对应的render函数，大致会生成三种，即元素节点、文本节点、注释节点  
元素节点渲染函数：生成元素节点的render函数就是生成一个_c()函数调用的字符串，_c =》createElement，返回 VNode | Array<VNode>
```javascript
const data = el.plain ? undefined : genData(el, state)  // 获取属性

const children = el.inlineTemplate ? null : genChildren(el, state, true)  // 获取子节点
code = `_c('${el.tag}'${
data ? `,${data}` : '' // data
}${
children ? `,${children}` : '' // children
})`
```

文本节点渲染函数：生成元素节点的render函数就是生成一个_v()函数调用的字符串，_v =》createTextVNode，返回 VNode
```javascript
export function genText (text: ASTText | ASTExpression): string {
  return `_v(${text.type === 2
    ? text.expression // no need for () because already wrapped in _s()
    : transformSpecialNewlines(JSON.stringify(text.text))
  })`
}
```

注释节点渲染函数：生成元素节点的render函数就是生成一个_e()函数调用的字符串，_e =》createEmptyVNode，返回 VNode
```javascript
export function genComment (comment: ASTText): string {
  return `_e(${JSON.stringify(comment.text)})`
}
```
```javascript
export function installRenderHelpers (target: any) {
  target._o = markOnce;
  target._n = toNumber;
  target._s = toString;
  target._l = renderList;
  target._t = renderSlot;
  target._q = looseEqual;
  target._i = looseIndexOf;
  target._m = renderStatic;
  target._f = resolveFilter;
  target._k = checkKeyCodes;
  target._b = bindObjectProps;
  target._v = createTextVNode;
  target._e = createEmptyVNode;
  target._u = resolveScopedSlots;
  target._g = bindObjectListeners;
  target._d = bindDynamicKeys;
  target._p = prependModifier
}
```

开发编写的template，会被编译为AST抽象语法树，然后对AST优化，即对静态节点标注，不进行深度的解析。  
然后将AST转化为渲染函数，也就是一段with语法开头的字符串  
最后调用 new Function 方法执行渲染函数即得到了最终的虚拟DOM

AST本身就可以看成是虚拟DOM的一个初版，因为他只包含最基本的属性，如tag、attrs、children等  
我们的虚拟DOM是包含数据监测等功能的，所以需要AST转化为VNode，构建虚拟DOM