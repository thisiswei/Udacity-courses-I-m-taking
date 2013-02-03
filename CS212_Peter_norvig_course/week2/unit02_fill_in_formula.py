""" 
   ODD + ODD = EVEN   figure out a way to fill in the formula
"""
from __future__ import division
import string, re, itertools, time

def solve(formula):
    for f in fill_in(formula): 
        if valid(f):
            return f
    # for anwser in ( for f in fill_in(formula) if valid(f) ):
    #      return anwser

def fill_in(formula):
    ' will return all possible formulas'
    #letters = ''.join( re.findall(r'[A-Z]',formula) )
    letters = ''.join( set(l for l in formula if l in string.uppercase) )
    for digit in itertools.permutations( '1234567890', len(letters) ):
        table = string.maketrans( letters, ''.join(digit) )
        yield formula.translate(table)
   

def valid(f):
    try:
        return not re.search(r'\b0[0-9]',f) and eval(f) is True
    except ArithmeticError:
        return False 

#----------- compile method --------------------

def faster_solve(formula):
    """Given a formula like 'ODD + ODD == EVEN', fill in digits to solve it.
    Input formula is a string; output is a digit-filled-in string or None.
    This version precompiles the formula; only one eval per formula."""
    f, letters = compile_formula(formula,verbose=False)
    for d in itertools.permutations( (1,2,3,4,5,6,7,8,9,0), len(letters) ):
        try: 
            if f(*d) is True:
                table = string.maketrans( letters, ''.join(map(str,d)) )
                return formula.translate(table)
        except ArithmeticError:
            pass

def compile_formula(formula, verbose=False):
    """
    Compile formula into a function.   Also return letters found, as a str,
    in same order as parms of function. For example, 'YOU == ME**2' returns
    (lambda Y, M, E, U, O): Y!=0 and M!= 0 and (U+10*O+100*Y) == (E+10*M)**2), 'YMEUO' 
    """
    
    letters       = ''.join( set(re.findall('[A-Z]',formula)) )
    first_letters = set ( re.findall(r'\b(A-Z)[A-Z]',formula) )
    params        = ', '.join(letters) 
    token         = map(compile_word,re.split('([A-Z]+)',formula))
    body          = ''.join(token)
    if first_letters:
        tests     = ' and '.join(L+'!=0' for L in first_letters)
        body      = '%s and %s' %(tests, body) 
    f             = 'lambda %s: %s' %(params, body)
    if verbose: print f
    return eval(f), letters


def compile_word(word):
    """Compile a word of uppercase letters as numeric digits.
    E.g., compile_word('YOU') => '(1*U+10*O+100*Y)'
    Non-uppercase words unchanged: compile_word('+') => '+'""" 
    if word.isupper():
        terms = [ ('%s*%s'%(10**i,letter)) for (i,letter) in enumerate(word[::-1]) ]
        return '(' + '+'.join(terms) + ')'
    else:
        return word





#----------- method end  --------------------

    

examples = """TWO + TWO == FOUR
A**2 + B**2 == C**2
A**2 + BE**2 == BY**2
X / X == X
A**N + B**N == C**N and N > 1
ATOM**0.5 == A + TO + M
GLITTERS is not GOLD
ONE < TWO and FOUR < FIVE
ONE < TWO < THREE
RAMN == R**3 + RM**3 == N**3 + RX**3
sum(range(AA)) == BB
sum(range(POP)) == BOBO
ODD + ODD == EVEN
PLUTO not in set([PLANETS])""".splitlines()


def test():
    t0 = time.clock()
    for example in examples:
        print; print 13*' ', example
        print '%6.4f sec:   %s ' % timedcall(solve,example)
        print '%6.4f sec:   %s ' % timedcall(faster_solve,example)
    print '%6.4f total.' % (time.clock()-t0)


def timedcalls(n, fn, *args):
    """Call fn(*args) repeatedly: n times if n is an int, or up to
    n seconds if n is a float; return the min, avg, and max time"""
    if isinstance(n,int):
        times = [ timedcall(fn,*args)[0] for _ in range(n) ]
    else:
        times =[]
        total = 0.
        while total < n:
            t = timedcall(fn,*args)[0]
            total += t
            times.append(t)
    return min(times), average(times), max(times)

def timedcall(fn, *args):
    t0 = time.clock()
    result = fn(*args)
    t1 = time.clock()
    return t1-t0, result

def average(n):
    return sum(n)/ len(n)+ 0.


test()
