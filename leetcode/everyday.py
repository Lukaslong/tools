'''
Daily Question
'''

# 2020.5.9
# 69. square of x
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

# 2020.5.11
# 50. pow(x, n) 
# 快速幂 + 递归， 快速幂的本质是分治法，时间和空间复杂度均为O(logn)
class Solution_50_1:
    def myPow(self, x: float, n: int) -> float:
        return self.quickMul(x,n) if n>0 else 1.0/self.quickMul(x,-n)
    def quickMul(self,x:float,N:int)->float:
        if N==0:
            return 1.0
        y=self.quickMul(x,N//2)
        return y*y if N%2==0 else y*y*x
# 快速幂+迭代，将n二进制展开。时间复杂度O(logn)，空间复杂度O(1)
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