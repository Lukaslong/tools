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

### 448. 找到消失的元素
class Solution448:
    def finddDisappearNumbers1(self,nums:List[int])->List[int]:
        ans=[]
        d={}
        for k in nums:
            d[k]=1
        for i in range(1,len(nums)+1):
            if i not in d.keys():
                ans.append(i)
        return ans
    
    def finddDisappearNumbers(self,nums):
        ans=[]
        for i in range(len(nums)):
            newindex=abs(nums[i])-1
            if nums[newindex]>0:
                nums[newindex]*=-1
        for j in range(len(nums)):
            if nums[j]>0:
                ans.append(j+1)
        return ans

class Solution560:
    def subarraySum(self, nums: List[int], k: int) -> int:
        ans=0
        curSum=0
        curDict={0:1}
        for i in range(len(nums)):
            curSum+=nums[i]
            oldSum=curSum-k
            if oldSum in curDict:
                ans+=curDict[oldSum]
            curDict[curSum]=curDict.get(curSum,0)+1
        return ans
                