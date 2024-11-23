def build_tree(arr,tree,node,start,end):
    if start==end:
        tree[node]=arr[start]
    else:
        left_node=2*node+1
        right_node=2*node+2
        mid=(start+end)//2
        build_tree(arr,tree,left_node,start,mid)
        build_tree(arr,tree,right_node,mid+1,end)
        tree[node]=tree[left_node]+tree[right_node]
def update(arr,tree,node,index,value,start,end):
    if start==end:
        arr[index]=value
        tree[node]=value
    else:
        mid=(start+end)//2 
        left_node=2*node+1
        right_node=2*node+2
        if start<=index<=mid:
            update(arr,tree,left_node,index,value,start,mid)
        else:
            update(arr,tree,right_node,index,value,mid+1,end)
        tree[node]=tree[left_node]+tree[right_node]
def query(arr,tree,node,start,end,L,R):
    if(L>end):
        return 0
    if(R<start):
        return 0
    if start==end or start==L and end==R:
        return tree[node]
    mid=(start+end)//2
    left_node=2*node+1
    right_node=2*node+2
    sum_left=query(arr,tree,left_node,start,mid,L,R)
    sum_right=query(arr,tree,right_node,mid+1,end,L,R)
    return sum_left+sum_right
class SegmentTree:
    def __init__(self,arr):
        self.tree=[0]*1000
        build_tree(arr,self.tree,0,0,len(arr)-1)
    def query(self,start,end):
        pass
    def update(self,arr,node,index,value,start,end):
        mid=(start+end)//2
        if end>=index>mid:
            self.update
arr=[1,3,5,7,9,11]
STree=SegmentTree(arr)
update(arr,STree.tree,0,4,6,0,5)
print(query(arr,STree.tree,0,0,5,2,5))
print(STree.tree[:20])