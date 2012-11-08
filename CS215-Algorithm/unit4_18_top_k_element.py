import random
def partition(L, v):
    a = [v]
    for element in L:

        if element > v:
            a.append(element)
        elif element < v:
            a.insert(0,element)
    v_pos = a.index(v)
    return (a[0:v_pos], [v] , a[v_pos+1::])

# select top k from list L
def top_k(L,k):
    v = L[random.randrange(len(L))]
    (left,middle,right) = partition(L,v)
    if len(left)   ==k: return left
    if len(left)+1 ==k: return left+[v]
    if len(left)  <  k: return left + [v] + top_k(right,k-len(left)-1)
    return top_k(left,k)


L = [31,34,45,66,77,88,54,44,90,110,56,32,50,60]

print top_k(L,7)
