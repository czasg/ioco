<!--
https://ae01.alicdn.com/kf/H7a9157260a3748e89be24de8399da4cdK.png
数据结构
二叉树遍历
包含三种遍历方式：前序遍历、中序遍历、后续遍历
包含三种遍历方式：前序遍历、中序遍历、后续遍历。二叉树模型由一个个节点组成，每一个节点包含该节点值，和其对应的左右节点。
-->

## 二叉树遍历

> 包含三种遍历方式：  
> 前序遍历、中序遍历、后续遍历

#### 二叉树模型
由一个个节点组成，每一个节点包含该节点值，和其对应的左右节点。
```python
class Node:
    def __init__(self, value=None, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right
```
创建一个二叉树：
```python
tree = last = Node('A')
for i in 'BCDEFG':
    if last.left is None:
        last.left = Node(i)
        continue
    if last.right is None:
        last.right = Node(i)
        continue
    last = last.left
    last.left = Node(i)
```

#### 前序遍历
```python
def pre(root):
    if root == None:
        return
    print(root.value)
    pre(root.left)
    pre(root.right)
```
打印值为：
A
B
D
F
G
E
C

#### 中序遍历
```python
def mid(root):
    if root == None:
        return
    mid(root.left)
    print(root.value)
    mid(root.right)
```
打印值为：
F
D
G
B
E
A
C

#### 后续遍历
```python
def aft(root):
    if root == None:
        return
    aft(root.left)
    aft(root.right)
    print(root.value)
```
打印值为：
F
G
D
E
B
C
A

#### 总结
总体来说，如下图：  
![二叉树](https://ae01.alicdn.com/kf/H2bf30b58a7974647a492e6960cb08325j.png)