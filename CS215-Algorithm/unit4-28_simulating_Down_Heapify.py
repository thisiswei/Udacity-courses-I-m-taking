###     5
   #   3 4
   # 2 1 3 2
   #1 0

   # when everything except the top(or ith position) node with its child not satifying Heap 
   
   
import random


L = [random.randrange(90) for _ in range(20)]

def left(i):  return 2*i + 1
def right(i): return 2*i + 2. 
def parent(i):return (i-1)/2
def root(i):  return i==0

#leaf: i got no child.
def leaf(L,i):      return left(i) >= len(L) or right(i) >= len(L)
def one_child(L,i): return right(i) == len(L)


def down_heapify(L,i):
    if leaf(L,i):        return 
    if one_child(L,i):
        if L[left(i)] < L[i] : 
            L[left(i)],L[i] = L[i], L[left(i)]
            return
    if min(L[left(i)],L[right(i)]) >= L[i]: return 
    if L[left(i)] > L[right(i)]:
        L[right(i)],L[i] = L[i],L[right(i)]  #swap value
    down_heapify(L,right(i))  #after swap,we make sure it continue to swap unitil it satisfy heap
        return
    
    L[left(i)],L[i] = L[i], L[left(i)]
    down_heapify(L,left(i))
    return
    
