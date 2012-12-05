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
