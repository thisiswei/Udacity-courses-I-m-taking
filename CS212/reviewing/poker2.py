
import doctest
import itertools
import random


def play(hands):
    return allmax(hands, key=hand_rank)


def all_max(iterable, key=None):
    results = []
    maxval = None
    key = key or (lambda x: x)
    for i in iterable:
        ival = key(i)
        if not maxval or ival > maxval:
            maxval, results = ival, [i]
        elif ival == maxval:
            results.append(i)
    return results

def hand_ranks(cards):
    ranks = ['..23456789TJKQA'.index(r) for r,s in cards]
    group = sorted([(ranks.count(r), r) for r in set(ranks)], reverse=True)
    card_counts,ranks = zip(*group)
    points = {(4, 1):          7,
              (3, 2):          6,
              (3, 1, 1):       3,
              (2, 2, 1):       2,
              (2, 1, 1, 1):    1,
              (1, 1, 1, 1, 1): 0} 
    suits = [s for r,s in cards]
    flush = len(set(suits)) == 1
    straight = (max(ranks)-min(ranks) == 4 and len(set(ranks))==5)

    return max(points[card_counts], 5*straight + 4*flush), ranks

one_deck = [r+s for r in '23456789TJQKA' for s in 'DHSC']

def deal_hands(num_hands, num_cards=5, deck=one_deck):
    random.shuffle(deck)
    return [deck[i*num_cards:(i+1)*num_cards] for i in range(num_hands)]

def seven_stud(hand):
    "pick 5 best card to form a hand from 7 cards"
    return max(itertools.combinations(hand,5), key=hand_ranks)

def best_wild_hand(hand):
    ' ?R = allredcards, ?B ..blacks'
    hands = set(seven_stud(h) for h in itertools.product(*map(replace, hand)))
    return max(hands, key=hand_ranks)
    
ranks = '23456789TJQKA'
redcards = [r+s for r in ranks for s in 'DH']
blackcards = [r+s for r in ranks for s in 'SC']

def replace(card):
    if card == '?B':
        return blackcards
    if card == '?R':
        return redcards
    else:
        return [card]
        
class Test:"""
>>> hand_ranks('7S 7S 7S 8S 9S'.split())

>>> deal_hands(3)

>>> sorted(best_wild_hand("6C 7C 8C 9C TC 5C ?B".split()))

"""

print doctest.testmod()


