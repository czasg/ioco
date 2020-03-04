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
        if r1 is None and r2 is None: return True
        if r1 is None or r2 is None: return False
        return (r1.val == r2.val) \
            and self.isMirror(r1.left, r2.right) \
            and self.isMirror(r1.right, r2.left)
```

### 4、翻转二叉树
翻转一棵二叉树。以中间轴为线反转过来
```python
class Solution:
    def invertTree(self, root: TreeNode) -> TreeNode:
        if root is None: return None
        left = self.invertTree(root.left)
        right = self.invertTree(root.right)
        root.left = right
        root.right = left
        return root
```

### 5、单值二叉树
如果二叉树每个节点都具有相同的值，那么该二叉树就是单值二叉树。
```python
class Solution:
    def isUnivalTree(self, root: TreeNode) -> bool:
        self.val = root.val
        return self.single(root) != -1

    def single(self, root):
        if not root: return
        val = self.single(root.left)
        if val == -1: return -1
        val = self.single(root.right)
        if val == -1: return -1
        if root.val != self.val: return -1
```

### 6、二叉树的坡度
给定一个二叉树，计算整个树的坡度。
> 一个树的节点的坡度定义即为，该节点左子树的结点之和和右子树结点之和的差的绝对值。空结点的的坡度是0。  
> 整个树的坡度就是其所有节点的坡度之和。
```python
class Solution:
    def findTilt(self, root: TreeNode) -> int:
        self.result = 0
        self.test(root)
        return self.result

    def test(self, root):
        if not root: return 0
        val1 = self.test(root.left)
        val2 = self.test(root.right)
        self.result += abs(val1 - val2)
        return val1 + val2 + root.val
```

### 7、二叉树的堂兄弟节点
在二叉树中，根节点位于深度 0 处，每个深度为 k 的节点的子节点位于深度 k+1 处。  
如果二叉树的两个节点深度相同，但父节点不同，则它们是一对堂兄弟节点。  
我们给出了具有唯一值的二叉树的根节点 root，以及树中两个不同节点的值 x 和 y。  
只有与值 x 和 y 对应的节点是堂兄弟节点时，才返回 true。否则，返回 false。
```python
class Solution:
    def isCousins(self, root: TreeNode, x: int, y: int) -> bool:
        parent = {}
        depth = {}

        def test(r, p=None):
            if not r: return
            depth[r.val] = 1 + depth[p.val] if p else 0
            parent[r.val] = p
            test(r.left, r)
            test(r.right, r)

        test(root)
        return depth[x] == depth[y] and parent[x] != parent[y]
```
