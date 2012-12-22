

def poly(coefs):
    def _f(x):
        return sum([num * x**pos for (pos,num) in enumerate(coefs)])
    _f.coefs = coefs
    _f.__name__ = formula_name(coefs)
    return _f

def formula_name(coefs):
    """(10, 20, 30) => [10, 20 * x, 30 * x**2] => 30 * x**2 + 20 * x + 10 
       (0, 0, 0, 1) => [x**3] => x**3 not 
                             1 * x**3 + 0 * x**2 + 0 * x**1
    """
    body = reversed([name(pos,num) for (pos,num) in enumerate(coefs) if num])
    return ' + '.join(body)

def name(pos,num):
    if pos == 0: return str(num)
    xnum = 'x' if pos == 1 else 'x**%s'%pos
    return xnum if num == 1 else '-%s'%xnum if num == -1 else '%s * %s'%(num,xnum)
                                             
def is_poly(x):
    "Return true if x is a poly (polynomial)."
    ## For examples, see the test_poly function
    return hasattr(x,'coefs')

def add(p1, p2):
    "Return a new polynomial which is the sum of polynomials p1 and p2."
    return combine(p1.coefs, p2.coefs)
    

def sub(p1, p2):
    "Return a new polynomial which is the difference of polynomials p1 and p2."
    p3 = [-i for i in p2.coefs]
    return combine(p1.coefs, tuple(p3))

def combine(A, B):
    maxlen = max(len(A), len(B))
    n = [0 for i in range(maxlen)]
    for (pos, item) in enumerate(A): n[pos] = item
    for (pos, item) in enumerate(B): n[pos] += item
    return poly(tuple(n)) 



def mul(p1, p2):
    "Return a new polynomial which is the product of polynomials p1 and p2."
    c1, c2 = p1.coefs, p2.coefs
    return  poly(tuple(sum(n1*n2 for (pos1,n1) in enumerate(c1) 
                                 for (pos2,n2) in enumerate(c2) 
                                 if pos1+pos2 == i) 
                                 for i in range(len(c1)+len(c2)-1)))


def power(p, n):
    "Return a new polynomial which is p to the nth power (n a non-negative integer)."
    return reduce(mul, [p]*n)

"""deriviative of a polynomial term (c * x**n) is (c*n * x**(n-1)).
The derivative of a sum is the sum of the derivatives.
So the derivative of (30 * x**2 + 20 * x + 10) is (60 * x + 20).

The integral is the anti-derivative:
The integral of 60 * x + 20 is  30 * x**2 + 20 * x + C, for any constant C.
Any value of C is an equally good anti-derivative.  We allow C as an argument
to the function integral (withh default C=0).
"""

def deriv(p):
    "Return the derivative of a function p (with respect to its argument)."
    return poly(tuple(coe*pos for pos,coe in enumerate(p.coefs) if pos))


def integral(p, C=0):
    "Return the integral of a function p (with respect to its argument)."
    params = tuple([C] + [num/(pos+1) for pos, num in enumerate(p.coefs)])
    return poly((params))



