'''
Daily Question
'''

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