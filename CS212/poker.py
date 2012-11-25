import random



def poker(hands):
    return all_max(hands,key=hand_rank)


def all_max(iterable,key=None):
    max_val,result = None , []
    key = key or (lambda x: x)
    for x in iterable:
        x_val = key(x)
        if not result or x_val > max_val:
            max_val , result = x_val , [x]
        elif x_val == max_val:
            result.append(x)
    return result

def openzip(pairs):
    return zip(*pairs) 

def group(hand):
    return sorted([ (hand.count(x),x) for x in set(hand) ],reverse=True) 

def hand_rank(hand):
    groups = group(['..23456789TJQKA'.index(r) for r,s in hand])
    count,ranks = openzip(groups)
    if ranks == (14,5,4,3,2):
        ranks = (5,4,3,2,1)
    straight = len(set(ranks))==5 and max(ranks)-min(ranks)==4
    flush   = len(set([s  for r,s in hand]))==1
    points = {(5,)       :10,
              (4,1)      :7,
              (3,2)      :6,
              (3,1,1)    :3,
              (2,2,1)    :2,
              (2,1,1,1)  :1,
              (1,1,1,1,1):0} 
    return (max(points[count],5*flush+4*straight),ranks)




    



# creating a deck,and deal numhands of n number cards 
one_deck=[r+s for r in '23456789TJQKA' for s in 'DHSC' ]
def deal_cards(numhands,n=5,deck=one_deck):
    random.shuffle(deck)
    return [deck[n*i:n*(i+1)] for i in range(numhands)]


def test():
    hands = [['7S', '4S', '8H', '3D', 'AH'], ['QD', 'QH', 'JH', 'TH', '6C'],['JS', '5S', 'TS', '8S', '3S']]
    assert hand_rank(['5C','4C','3C','2C','AC']) == (9,(5,4,3,2,1))
    assert hand_rank(hands[0]) == (0,(14,8,7,4,3))
    assert hand_rank(hands[1]) == (1,(12,11,10,6))
    assert hand_rank(hands[2]) == (5,(11,10,8,5,3))
    assert poker(hands) ==  [hands[2]]
    print 'you nailed it' 

test()





