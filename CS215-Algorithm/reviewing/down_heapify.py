


L = [random.randint(0, 100) for i in range(20)]

def left(i): return i*2 + 1
def right(i): return i*2 + 2
def parent(i): return (i-1)/2
def root(i): return i == 0
def leaf(L, i): return len(L) <= right(i) and len(L) <= left(i)
def one_child(L, i): return right(i) == len(L)

# if the heap rooted at i satisfies the heap property
# *except* perhaps i to its immediate children

def downheap(L, i):
    if leaf(L, i): return
    if one_childe(L, i): 
        if L[i] > L[left(i)]:
            L[i], L[left(i)] = L[left(i)], L[i]
        return
    if min(L[left(i)], L[right(i)]) >= L[i]: return
    if L[left(i)] > L[right(i)]:
        L[i], L[right(i)] = L[right(i)], L[i]
        downheap(L, left(i))
        return
    L[left(i)], L[i] = L[i], L[left(i)]
    downheap(L, right(i))
    return

# swap L[i] with its right child's value if its left child is bigger than right
# else left. and continue heapify with its childrens
