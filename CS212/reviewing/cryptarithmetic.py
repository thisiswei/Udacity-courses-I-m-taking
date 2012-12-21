""" 
   ODD + ODD = EVEN   figure out a way to fill in the formula
"""

'111 + 222 = 333'
" generate all the possible formula, check if valid, if yes return "

import string
import re

digits = string.digits

def solve(formula):
    for answer in (f for f in fill_in(formula) if valid_f(f)):
        return answer

def fill_in(formula):
#   letters = ''.join(re.findall(r'[A-Z]', formula))
    letters = ''.join(set(l for l in formula if l in string.uppercase))
    for nums in itertools.permutations(digits, len(letters)):
        table = string.maketrans(letters, ''.join(nums))
        yield formula.translate(table)

def valid_f(formula):
    try:
        return not re.search(r'\b0[0-9]', formula) and eval(formula) 
    except ArithmeticError:
        return False


#--- compile formula -------

def faster_solve(formula):
    f, letters = compile_formula(formula)
    for d in itertools.permutations((0,1,2,3,4,5,6,7,8,9), len(letters)):
        try:
            if f(*d):
                table = string.maketrans(letters, ''.join(map(str, d)))
                return formula.translate(table)
        except ArithmeticError:
            pass

""" (lambda Y, M, E, U, O): Y!=0 and M!= 0 and (U+10*O+100*Y) == (E+10*M)**2), 'YMEUO' """

def compile_formula(formula):
    letters = ''.join(set(l for l in formula if l in string.uppercase))
    first_letters = set(re.findall(r'\b([A-Z])[A-Z]', formula))
    body = ''.join(map(compile_word, re.split('([A-Z]+)', formula)))
    if first_letters:
        condition = ' and '.join(L+' !=0 ' for L in first_letters)
        body = condition + ' and ' + body
    f = 'lambda %s: %s ' % (', '.join(letters), body)
    return eval(f), letters


def compile_word(word): 
    " ('YOU') => '(1*U+10*O+100*Y) "
    return '(' + ' + '.join('%s*%s'%(10**i, l) for i,l in enumerate(word[::-1])) + ')' if word.isupper() else word



