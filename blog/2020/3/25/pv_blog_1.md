<!--
https://ae01.alicdn.com/kf/Hf111b2be3fcf4f5681042025bad26905E.png
正则
正则的基本使用
正则的基本使用，包括findall、search、match、sub、split等
正则的基本使用，包括findall、search、match、sub、split等
-->

## 正则的基本使用

> 正则的基本使用


match，匹配开头一次  
search， 匹配符合的str一次  
findall，匹配所有符合的规则，但是每次匹配不管你是否需要，匹配完后都会‘去除’   
sub，替换所有符合规则的str  
split，切割所有符合规则的符号  

#### 零宽断言
我们一般在使用findall的时候，会切割掉我们所有已匹配到的规则，即我们需要用它定位，但也需要用它进行下一次的匹配。
此时我们就可以使用零宽断言，在不切割的前提下，进行对应位置的判断。
* (?=)
* (?!)
* (?<=)
* (?<!)

#### groupdict
能够讲匹配到的group装到字典中
```python
import re
re.search('(?P<test1>.*?)_(?P<test2>.*)', "hello_world").groupdict()  # 能够得到匹配的字典咯
```
















