# 102. 二叉树的层序遍历 (2020.5.13)
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

class Solution:
    def levelOrder(self, root: TreeNode) -> List[List[int]]:
        if not root:
            return []
        ans=[]
        curlayer=[root]
        while curlayer:
            curans=[]
            nextlayer=[]
            for node in curlayer:
                if node:
                    curans.append(node.val)
                    nextlayer.append(node.left)
                    nextlayer.append(node.right)
            curlayer=nextlayer
            if curans:
                ans.append(curans)
        return ans