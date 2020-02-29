<!--
https://ae01.alicdn.com/kf/H5b7d744c730749d38c943f30ed10e0330.png
数据结构
二叉树算法（简单）
平衡二叉树、合并二叉树、对称二叉树、翻转二叉树、对称的二叉树、单值二叉树...
平衡二叉树、合并二叉树、对称二叉树、翻转二叉树、对称的二叉树、单值二叉树、二叉树的坡度、二叉树的镜像 、二叉树的堂兄弟节点 、修剪二叉搜索树、二叉树的深度、二叉树的直径
-->

## 二叉树算法（简单一）

> 平衡二叉树、合并二叉树、对称二叉树、翻转二叉树、对称的二叉树、单值二叉树、二叉树的坡度、
> 二叉树的镜像 、二叉树的堂兄弟节点 、修剪二叉搜索树、二叉树的深度、二叉树的直径

```python
class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right
```

### 1、平衡二叉树
给定一个二叉树，判断它是否是高度平衡的二叉树。
> 高度平衡二叉树定义为：一个二叉树每个节点 的左右两个子树的高度差的绝对值不超过1。  

思路：  
1、从底至顶：做深度优先遍历DFS（深度优先搜索算法）。
当越过叶子节点时返回0，每返回一层则升深度+1.若发现不平衡树，则直接返回-1
```python
class Solution:
    def isBalanced(self, root: Node) -> bool:
        return self.depth(root) != -1

    def depth(self, root):
        if not root: return 0
        left = self.depth(root.left)
        if left == -1: return -1
        right = self.depth(root.right)
        if right == -1: return -1
        return max(left, right) + 1 if abs(left - right) < 2 else -1
```

### 2、合并二叉树
给定两个二叉树，合并为一个新的二叉树。合并的规则是如果两个节点重叠，
那么将他们的值相加作为节点合并后的新值，否则不为 NULL 的节点将直接作为新二叉树的节点
```python
class Solution:
    def mergeTrees(self, t1: Node, t2: Node) -> Node:
        if not t1: return t2
        if not t2: return t1
        t1.val += t2.val
        t1.left = self.mergeTrees(t1.left, t2.left)
        t1.right = self.mergeTrees(t1.right, t2.right)
        return t1
```

### 3、对称二叉树
给定一个二叉树，检查它是否是镜像对称的。即二叉树是否以中线对称
```python
class Solution:
    def isSymmetric(self, root: TreeNode) -> bool:
        return self.isMirror(root, root)

    def isMirror(self, r1, r2):
        if all((r1, r2)): return (r1.val == r2.val) \
            and self.isMirror(r1.left, r2.right) \
            and self.isMirror(r1.right, r2.left)
        return True if r1 is r2 else False
```

### 4、翻转二叉树
翻转一棵二叉树。以中间轴为线反转过来
```python
class Solution:
    def invertTree(self, root: TreeNode) -> TreeNode:
        if root:
            left = self.invertTree(root.left)
            right = self.invertTree(root.right)
            root.left = right
            root.right = left
            return root
```
