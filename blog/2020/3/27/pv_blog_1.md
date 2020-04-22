<!--
https://ae01.alicdn.com/kf/Haf4d3b0529ba47669bf69c7bfc71a5f1Y.png
python
Python异常与测试
python得异常包含常用sys.exit和Exception等，还有单元测试
python得异常包含常用sys.exit和Exception等，还有单元测试
-->

## Python异常与测试

> python得异常包含常用sys.exit和Exception等，还有单元测试

python所有得异常都继承自baseException这个类。如：  
系统返回错误码  
按键报错  
还有Exception
```
BaseException
 +-- SystemExit
 +-- KeyboardInterrupt
 +-- GeneratorExit
 +-- Exception
```

#### 单元测试得意义
单元测试得意思就是我们先定义好输入和输出，也就是目的性要明确。
然后通过单元测试后，一旦我们修改代码，或者修改了某处逻辑等，再次跑一边单元测试，一旦通过，
说明没有问题，一旦测试不通过，那就说明我们改错地方了。  

也叫“测试驱动开发”

#### 文档测试
可以自动执行写在注释中的这些代码
```python
def test(*args, **kwargs):
    """
    >>> test('hello', 'world')
    1
    """
    return 1
if __name__ == "__main__":
    import doctest
    doctest.testmod()
```
