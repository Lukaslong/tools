### 69. square of x  (2020.5.9)
class Solution_69:
    def mySqrt(self, x: int) -> int:
        left,right=0,x
        while left<right:
            mid=(left+right+1)//2
            temp=mid*mid
            if temp==x:
                return mid
            elif temp>x:
                right=mid-1
            else:
                left=mid
        return left

### 50. pow(x, n)  (2020.5.11)
快速幂 + 递归， 快速幂的本质是分治法，时间和空间复杂度均为O(logn)
```
class Solution_50_1:
    def myPow(self, x: float, n: int) -> float:
        return self.quickMul(x,n) if n>0 else 1.0/self.quickMul(x,-n)
    def quickMul(self,x:float,N:int)->float:
        if N==0:
            return 1.0
        y=self.quickMul(x,N//2)
        return y*y if N%2==0 else y*y*x

```

快速幂+迭代，将n二进制展开。时间复杂度O(logn)，空间复杂度O(1)
```
class Solution_50_2:
    def myPow(self,x:float,n:int)->float:
        return self.quickMul(x,n) if n>0 else 1.0/self.quickMul(x,-n)
    def quickMul(self,x:float,N:int)->float:
        if N==0:
            return 1.0
        ans=1.0
        temp=x
        while N>0:
            if N%2==1:
                ans*=temp
            temp*=temp
            N=N//2
        return ans
```

### MinStack (2020.5.12)
最小栈，要求自己定义栈，并完成栈的基本操作函数定义
```
# Your MinStack object will be instantiated and called as such:
# obj = MinStack()
# obj.push(x)
# obj.pop()
# param_3 = obj.top()
# param_4 = obj.getMin()
class MinStack:

    def __init__(self):
        """
        initialize your data structure here.
        """
        self.sta=[]
        

    def push(self, x: int) -> None:
        self.sta.append(x)
        

    def pop(self) -> None:
        self.sta.pop()
        

    def top(self) -> int:
        return self.sta[-1]
        

    def getMin(self) -> int:
        #minsta=self.sta[0]
        #for i in range(len(self.sta)):
        #    minsta=min(minsta,self.sta[i])
        return min(self.sta)
```

### 102. 二叉树的层序遍历 (2020.5.13)

```
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

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
```

### 560. 和为K的子数组
```
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
```