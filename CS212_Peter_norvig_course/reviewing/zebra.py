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

def imright(h1, h2):
    return h2-h1 == 1

def next_to(h1, h2):
    return abs(h1-h2) == 1

def zebra():
    houses = first, _, middle, _, _ = 1, 2, 3, 4, 5
    orders = list(itertools.permutations(houses))
    return next((WATER, ZEBRA)
                for (Englishman, Spaniard, Ukrainian, Norwegian, Japanese) in orders
                if Norwegian is first 
                for (red, green, yellow, blue, ivory) in orders
                if imright(ivory, green) and next_to(Norwegian, blue) and Englishman is red 
                for (dog, snails, fox, horse, ZEBRA) in orders
                for (old_gold, kools, chesterfields, lucky, parliaments) in orders
                if old_gold is snails and next_to(chesterfields, fox) and next_to(horse, kools)
                and Spaniard is dog and Japanese is parliaments 
                for (coffee, tea, milk, orange, WATER) in orders
                if Ukrainian is tea and coffee is green and milk is middle
                and lucky is orange)

print zebra()

