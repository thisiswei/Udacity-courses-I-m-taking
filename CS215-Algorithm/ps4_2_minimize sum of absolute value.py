
# Given a list of numbers, L, find a number, x, that
# minimizes the sum of the absolute value of the difference
# between each element in L and x: SUM_{i=0}^{n-1} |L[i] - x|
# 
# Your code should run in Theta(n) time
#
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
def top_k(L,k):
    v = L[random.randrange(len(L))]
    (left,middle,right) = partition(L,v)
    if len(left)   ==k: return left
    if len(left)+1 ==k: return left+[v]
    if len(left)  <  k: return left + [v] + top_k(right,k-len(left)-1)
    return top_k(left,k)

def minimize_absolute(L):
    if len(L)%2 != 0:
        result = top_k(L,len(L)/2+1)
    else:
        result = top_k(L,len(L)/2)
    return result[-1]
