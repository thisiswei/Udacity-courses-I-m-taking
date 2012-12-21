

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
    body = reversed([name(pos,num) for (pos,num) in enumerate(coefs) if num != 0])
    return ' + '.join(body)

def name(pos,num):
    if pos == 0:
        return str(num)
    xnum = 'x' if pos == 1 else 'x**%s'%pos
    return xnum if num == 1 else '-%s'%xnum if num == -1 else '%s * %s'%(num,xnum)

    assert add(poly((10, 20, 30)), poly((1, 2, 3))).coefs == (11,22,33)
    assert sub(poly((10, 20, 30)), poly((1, 2, 3))).coefs == (9,18,27) 
    assert mul(poly((10, 20, 30)), poly((1, 2, 3))).coefs == (10, 40, 100, 120, 90)
    assert power(poly((1, 1)), 2).coefs == (1, 2, 1) 
    assert power(poly((1, 1)), 10).coefs == (1, 10, 45, 120, 210, 252, 210, 120, 45, 10, 1)
                                             
def is_poly(x):
    "Return true if x is a poly (polynomial)."
    ## For examples, see the test_poly function
    return hasattr(x,'coefs')

def add(p1, p2):
    "Return a new polynomial which is the sum of polynomials p1 and p2."
    c1, c2 = p1.coefs, p2.coefs
    new_c = [c1[i]+c2[i] for i in range(len(c1))]
    return poly(new_c)

def sub(p1, p2):
    "Return a new polynomial which is the difference of polynomials p1 and p2."
    c1, c2 = p1.coefs, p2.coefs
    new_c = [0 for i in range(len(c1))]
    for (pos,num) in enumerate(c1): new_c[pos] = num
    for (pos,num) in enumerate(c2): new_c[pos] -= num
    return poly(new_c)


def mul(p1, p2):
    "Return a new polynomial which is the product of polynomials p1 and p2."
    c1, c2 = p1.coefs, p2.coefs
    return  poly(tuple(sum(n1*n2 for (pos1,n1) in enumerate(c1) 
                                 for (pos2,n2) in enumerate(c2) 
                                 if pos1+pos2 == i) 
                                 for i in range(len(c1)+len(c2)-1)))


def power(p, n):
    "Return a new polynomial which is p to the nth power (n a non-negative integer)."



