from __future__ import division
import doctest
import math    

def inverse(f,delta=1/1023.):
    def f_1(y):
        lo,hi = find_bounds(f,y)
        return binary_search(f,y,lo,hi,delta)
    return f_1

def find_bounds(f,y):
    x = 1.
    while f(x) < y:
        x = x*2.
    lo = 0 if (x==1) else (x/2.)
    return lo, x

def binary_search(f,y,lo,hi,delta):
    while lo <= hi:
        x = (lo + hi) / 2. 
        if f(x) < y:
            lo = x + delta 
        elif f(x) > y:
            hi = x - delta 
        else: 
            return x;

    return hi if (f(hi)-y < y-f(lo)) else lo 







def sq(x): return x*x

sqr = inverse(sq)  

class Test:"""

>>> sqr(81)

>>> sqr(100)


"""

print doctest.testmod()
