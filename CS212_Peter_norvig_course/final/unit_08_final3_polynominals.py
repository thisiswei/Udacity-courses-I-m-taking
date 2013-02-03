"""
CS212 final problem 3

A polynomial is a mathematical formula like:

    30 * x**2 + 20 * x + 10

More formally, it involves a single variable (here 'x'), and the sum of one
or more terms, where each term is a real number multiplied by the variable
raised to a non-negative integer power. (Remember that x**0 is 1 and x**1 is x,
so 'x' is short for '1 * x**1' and '10' is short for '10 * x**0'.)

We will represent a polynomial as a Python function which computes the formula
when applied to a numeric value x.  The function will be created with the call:

    p1 = poly((10, 20, 30))

where the nth element of the input tuple is the coefficient of the nth power of x.
(Note the order of coefficients has the x**n coefficient neatly in position n of 
the list, but this is the reversed order from how we usually write polynomials.)
poly returns a function, so we can now apply p1 to some value of x:

    p1(0) == 10

Our representation of a polynomial is as a callable function, but in addition,
we will store the coefficients in the .coefs attribute of the function, so we have:

    p1.coefs == (10, 20, 30)

And finally, the name of the function will be the formula given above, so you should
have something like this:

    >>> p1
    <function 30 * x**2 + 20 * x + 10 at 0x100d71c08>

    >>> p1.__name__
    '30 * x**2 + 20 * x + 10'

Make sure the formula used for function names is simplified properly.
No '0 * x**n' terms; just drop these. Simplify '1 * x**n' to 'x**n'.
Simplify '5 * x**0' to '5'.  Similarly, simplify 'x**1' to 'x'.
For negative coefficients, like -5, you can use '... + -5 * ...' or
'... - 5 * ...'; your choice. I'd recommend no spaces around '**' 
and spaces around '+' and '*', but you are free to use your preferences.

Your task is to write the function poly and the following additional functions:

    is_poly, add, sub, mul, power, deriv, integral

They are described below; see the test_poly function for examples.
"""

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



