
"""
A portmanteau word is a blend of two or more words, like 'mathelete',
which comes from 'math' and 'athelete'

rules are: a portmanteau must be composed of three non-empty pieces, 
             start+mid+end, 
        'adolescented' comes from 
        'adolescent','scented', with 
    start+mid+end='adole'+'scent'+'ed'.

score:    'adole'+'scent'+'ed', the 
start,mid,end lengths are 5,5,2 and the total length is 12.  The ideal
start,mid,end lengths are 12/4,12/2,12/4 = 3,6,3. So the final score

     12 - abs(5-3) - abs(5-6) - abs(2-3) = 8.  

A portmanteau must be composed of two different words (not the same word twice).

The output of natalie(words) should be the best portmanteau, or None """
#--------------------------------------------------------------------------


import itertools
import doctest

def natalie(words): 
    results = []
    # ['int', 'intimate', 'hinter', 'hint', 'winter']
    for w1, w2 in itertools.combinations(words,2):
        if w1 not in w2 and w2 not in w1:  
            for m in presubfixes(w1):# all possible prefix,subfixes from w1 
                if m in w2 and valid(m, w1, w2):  #invalid => ('hi' 'hint' 'hiner') 
                    results.append(three_parts(m, w1, w2))
                    break #(presub fixes are sorted by lens), when we find :'initi' not need to do 'init'
    return sorted(results) if results else None

def valid(m, w1, w2): 
    return w1.startswith(m) + w2.startswith(m) == 1


#     middle   word1     word2
# ('phant', 'elephant', 'phantom') => 'ele + phant + om'
#('int', 'intimate', 'hint') => 'h + int + imate' 

def three_parts(m, w1, w2):
    L = len(m)
    parts = ((w1[:-L], m, w2[L:]) if w2.startswith(m) else 
             (w2[:w2.index(m)], m, w1[L:]))
    if not all(parts): return # if not compose of start, mid, end
    return calculate(*parts), ''.join(parts) 

def calculate(*words):
    s, m, e = map(len, words)
    t = s + m + e
    return t - abs(s-t/4.) - abs(m-t/2.) - abs(e-t/4.)

# >>> presubfixes('kimono') 
#['kimon', 'imono', 'kimo', 'mono', 'kim', 'ono', 'no', 'ki', 'o', 'k']   

def presubfixes(w):
    mixes = [(w[i:],w[:i]) for i in range(1, len(w))] 
    return sorted([y for x in mixes for y in x], key=len)[::-1]
 





#--------------------------------test------------------------------------------
class Test:"""
>>> natalie(['adolescent', 'scented', 'centennial', 'always', 'ado']) 
[(2.0, 'alwayscented'), (4.0, 'centennialways'), (8.0, 'adolescented'), (8.0, 'adolescentennial')]
>>> natalie(['eskimo', 'escort', 'kimchee', 'kimono', 'cheese'])
[(2.0, 'kimchescort'), (2.0, 'kimcheskimo'), (4.0, 'cheescort'), (4.0, 'cheeskimo'), (7.5, 'kimcheese'), (8.0, 'eskimono')]
>>> natalie(['kimono', 'kimchee', 'cheese', 'serious', 'us', 'usage'])
[(4.0, 'cheeserious'), (4.0, 'seriousage'), (7.5, 'kimcheese')]
>>> natalie(['circus', 'elephant', 'lion', 'opera', 'phantom'])
[(1.0, 'opelephant'), (2.0, 'phantopera'), (9.0, 'elephantom')]
>>> natalie(['programmer', 'coder', 'partying', 'merrymaking'])
[(6.0, 'programmerrymaking')]
>>> natalie(['int', 'intimate', 'hinter', 'hint', 'winter'])
[(3.5, 'hintimate'), (3.5, 'hintimate'), (3.5, 'wintimate')]  
>>> natalie(['morass', 'moral', 'assassination'])
[(4.0, 'morassassination')]
>>> natalie(['entrepreneur', 'academic', 'doctor', 'neuropsychologist', 'neurotoxin', 'scientist', 'gist']) #
[(-0.5, 'scieneuropsychologist'), (0.5, 'giscientist'), (2.0, 'acadentrepreneur'), (2.0, 'scieneurotoxin'), (4.5, 'scientrepreneur'), (8.0, 'entrepreneuropsychologist'), (8.0, 'entrepreneurotoxin')]
>>> natalie(['perspicacity', 'cityslicker', 'capability', 'capable'])
[(-1.0, 'caperspicacity'), (-1.0, 'caperspicacity'), (8.0, 'perspicacityslicker')]
>>> natalie(['backfire', 'fireproof', 'backflow', 'flowchart', 'background', 'groundhog'])# == 
[(2.0, 'backfireproof'), (8.0, 'backfireproof'), (8.0, 'backflowchart'), (11.5, 'backgroundhog')]
>>> natalie(['streaker', 'nudist', 'hippie', 'protestor', 'disturbance', 'cops'])# == 
[(0.5, 'coprotestor'), (2.0, 'copstreaker'), (3.0, 'distreaker'), (4.0, 'nudistreaker'), (4.0, 'protestreaker'), (5.5, 'nudisturbance')]
"""

print doctest.testmod()


