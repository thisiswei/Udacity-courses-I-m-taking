#
# write up_heapify, an algorithm that checks if
# node i and its parent satisfy the heap
# property, swapping and recursing if they don't
#
# L should be a heap when up_heapify is done
#

def up_heapify(L, i):
    def up(L, i):
        if i == 0: return
        if L[parent(i)] < L[i]: return
        if L[parent(i)] > L[i] :
            L[parent(i)], L[i] = L[i], L[parent(i)]
            up_heapify(L, parent(i)) 
    for i in range(len(L)-1, 0, -1):
        up(L, i)
    return L



def parent(i): 
    return (i-1)/2


def test():
    L = [2, 4, 3, 5, 9, 7, 7]
    L.append(1)
    up_heapify(L, 7)
    assert 1 == L[0]
    assert 2 == L[1]

