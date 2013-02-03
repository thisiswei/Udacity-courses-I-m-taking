"""
 Zebra Puzzle 
1 There are five houses.  
2 The Englishman lives in the red house.  
3 The Spaniard owns the dog.  
4 Coffee is drunk in the green house.  
5 The Ukrainian drinks tea.  
6 The green house is immediately to the right of the ivory house.  
7 The Old Gold smoker owns snails.  
8 Kools are smoked in the yellow house.  
9 Milk is drunk in the middle house.  
10 The Norwegian lives in the first house.  
11 The man who smokes Chesterfields lives in the house next to the man with the fox.  
12 Kools are smoked in a house next to the house where the horse is kept.  
13 The Lucky Strike smoker drinks orange juice.  
14 The Japanese smokes Parliaments.  
15 The Norwegian lives next to the blue house.

Who drinks water? Who owns the zebra? 
"""
import itertools

def imright(h1,h2):
    return h2-h1 == 1

def next_to(h1,h2):
    return abs(h1-h2) == 1

def c(s):
    c.starts +=1
    for item in s:
        c.items +=1
        yield item
 
def zebra_puzzle():
    houses = first, _, middle, _, _ = [1,2,3,4,5]
    orderings = list(itertools.permutations(houses))
    return next( (WATER,ZEBRA)
                 for (red,green,ivory,yellow,blue) in c(orderings)
                 if imright(ivory,green)
                 for (englishman,spaniard,ukrainian,norwegian,japanese) in c(orderings)
                 if englishman is red and norwegian is first and next_to(blue,norwegian)
                 for (coffee,milk,orange,tea,WATER) in c(orderings)
                 if coffee is green and (ukrainian is tea and milk is middle) 
                 for (kools,chesterfields,lucky,parliaments,oldgold) in c(orderings)
                 if kools is yellow and lucky is orange    
                 if japanese is parliaments 
                 for (fox,dog,snails,horse,ZEBRA)  in c(orderings)
                 if spaniard is dog and oldgold is snails and next_to(kools,horse) 
                )  

def c(s):
    c.starts +=1
    for item in s:
        c.items +=1
        yield item
 

def instrument(fn,*args):
    c.starts, c.items = 0, 0
    result = fn(*args)
    print '%s got %s with %5d iters over %7d items' %(fn.__name__,result,c.starts,c.items)


instrument(zebra_puzzle)

