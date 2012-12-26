import itertools
import doctest

def natalie(list): 
    if len(list) < 2: return None
    results = []
    for pairs in combos(list):
        r = combine(*pairs)
        if r:
            results.append(r)
    return sorted(results) if results else None

def combine(w1, w2):
    if (w1 in w2) or (w2 in w1): return None
    candidates = pre_subs(w1)
    is_in_w2 = part_of(w2)
    for c in candidates:
        if is_in_w2(c) and valid(c, w1, w2):
            return three_parts(c, w1, w2)
    return None

def valid(letters, w1, w2):
    return (w1.startswith(letters) + w2.startswith(letters)) == 1

def three_parts(letters, w1, w2):
    parts= form_word(letters, w1, w2)
    if not all(parts): return 
    new_word = parts[0] + parts[-1]  
    return calculate(*parts), new_word

def form_word(L, w1, w2):
    x, y = w1.index(L), w2.index(L)
    word = ((w2[:y], L,  w1) if not x else
            (w1[:x], L,  w2))
    return word 


def combos(lists):
    return [i for i in itertools.combinations(lists,2)]
    
def pre_subs(w): 
    return sorted([y for x in zip(*[(w[i:],w[:i]) for i in range(1, len(w))]) for y in x], reverse=True, key=len)

def calculate(*words):
    s, m, e = map(len, words)
    t = s + m + e
    return t - abs(s-t/4.) - abs(m-t/2.) - abs(e-t/4.)

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


