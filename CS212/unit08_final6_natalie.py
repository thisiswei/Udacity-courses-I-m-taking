import itertools
import doctest

def natalie(list): 
    if len(list) < 2: return None
    results = []
    for pairs in combos(list):
        w1, w2 = pairs
        r = combine(w1, w2)
        if r:
            results.append(r)
    return sorted(results)[-1][-1] if results else None

def combine(w1, w2):
    if w1 in w2 or w2 in w1: return None
    candidates = pre_sub_fixes(w1)
    is_in_w2 = part_of(w2)
    for c in candidates:
        if is_in_w2(c):
            return three_parts(c, w1, w2)
    return None

def three_parts(letters, w1, w2):
    parts= form_word(letters, w1, w2)
    if not parts: return
    new_word = ''.join(parts)
    scores = sum([calculate(*s) for s in zip(parts, (new_word,)*3, ('s', 'm', 'e'))], 12)
    return scores, new_word

def form_word(L, w1, w2):
    if w1.startswith(L) and w2.startswith(L):
        return False
    word = ((w2+w1)if w1.startswith(L) else
            (w1+w2))
    word = word.replace(L, '', 1) 
    i = word.index(L)
    return word[:i], L, word[i+len(L):]

def combos(lists):
    return [i for i in itertools.combinations(lists,2)]
    
def pre_sub_fixes(w):
    return sorted([y for x in zip(*[(w[i:],w[:i]) for i in range(len(w))])
                   for y in x if y], reverse=True, key=len)

def calculate(letters, word, part):
    lw = len(word)
    ll = len(letters)
    div = 4. if part in 'se' else 2.
    idea_l = lw / div 
    return -abs(ll - idea_l) 

def part_of(y):
    return lambda x: x in y


class Test:"""
>>> natalie(['adolescent', 'scented', 'centennial', 'always', 'ado']) #in ('adolescented','adolescentennial')
'adolescented'
>>> natalie(['eskimo', 'escort', 'kimchee', 'kimono', 'cheese'])# == 'eskimono'
'eskimono'
>>> natalie(['kimono', 'kimchee', 'cheese', 'serious', 'us', 'usage'])
'kimcheese'
>>> natalie(['circus', 'elephant', 'lion', 'opera', 'phantom'])# == 
'elephantom'
>>> natalie(['programmer', 'coder', 'partying', 'merrymaking']) #== 
'programmerrymaking'
>>> natalie(['int', 'intimate', 'hinter', 'hint', 'winter'])# == 
'hintimate'
>>> natalie(['morass', 'moral', 'assassination'])# == 
'morassassination'
>>> natalie(['entrepreneur', 'academic', 'doctor', 'neuropsychologist', 'neurotoxin', 'scientist', 'gist']) #
'entrepreneuropsychologist' 
>>> natalie(['perspicacity', 'cityslicker', 'capability', 'capable'])
'perspicacityslicker'
>>> natalie(['backfire', 'fireproof', 'backflow', 'flowchart', 'background', 'groundhog'])# == 
'backgroundhog'
>>> natalie(['streaker', 'nudist', 'hippie', 'protestor', 'disturbance', 'cops'])# == 
'nudisturbance'
>>> natalie(['night', 'day']) #== None 

>>> natalie(['dog', 'dogs'])# == None

>>> natalie(['test'])# == None

>>> natalie(['']) #==  None

>>> natalie(['ABC', '123']) #== None

>>> natalie([]) #== None

"""

print doctest.testmod()
