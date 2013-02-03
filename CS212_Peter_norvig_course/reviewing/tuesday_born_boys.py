import itertools
from fractions import Fraction

sex = 'BG'
two_kids = product(sex, sex)                # >>> two_kids
one_boy = [b for b in two_kids if 'B' in b] # ['BB', 'BG', 'GB', 'GG'] 
days = 'SMTWtFs'
two_kids_bday = product(sex, days, sex, days)
tuesday_born_boys = [s for s in two_kids_bday if 'BT' in s]

def product(*variables):
    return map(''.join, itertools.product(*variables))

def two_boys(s): return s.count('B') == 2

def condition_probability(predicate, event):
    pred = [s for s in event if predicate(s)]
    return Fraction(len(pred), len(event))

#what's the probability of a family having two boys given that
#the family have two kids,and at least one of the kid is a boy born on tuesday

# >>> condition_probability(two_boys, tuesday_born_boys)
# 13/27


