class Tree(object):
    def __init__(self,dataval):
        self.val=dataval
        self.left=None
        self.right=None
    
    # recursion
    def pre1(self,root):
        if not root:
            return
        print(root.val)
        self.pre1(root.left)
        self.pre1(root.right)
    def mid1(self,root):
        if not root:
            return
        self.mid1(root.left)
        print(root.val)
        self.mid1(root.right)
    def post1(self,root):
        if not root:
            return
        self.post1(root.left)
        self.post1(root.right)
        print(root.val)
    
    # iteration
    def pre2(self,root):
        nodes=[]
        t=root
        while t or nodes:
            if t:
                print(t.val)
                nodes.append(t)
                t=t.left
            else:
                t=nodes[-1]
                nodes.pop()
                t=t.right
                
        
    def mid2(self,root):
        nodes=[]
        t=root
        while t or nodes:
            if t:
                nodes.append(t)
                t=t.left
            else:
                t=nodes[-1]
                nodes.pop()
                print(t.val)
                t=t.right


    def post2(self,root):
        t=root
        pre=None
        nodes=[]
        while t or nodes:
            while t:
                nodes.append(t)
                t=t.left
            t=nodes[-1]
            if not t.right or pre==t.right:
                print(t.val)
                pre=t
                nodes.pop()
                t=None
            else:
                t=t.right

def find_diff(nums):
    odd,odd_1=0,0
    for i in nums:
        odd^=i
    right=odd&(~odd+1)
    for i in nums:
        if i&right!=0:
            odd_1^=i
    return odd_1,odd_1^odd