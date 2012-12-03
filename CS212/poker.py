"""
Hey !! Gschool,j3,I dont think im a developer,but i just dont have any expertise in anything
here is some code that i wrote while learning CS212 in udacity
README in this repo,can better assist you get a piture of me :)

"""



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

hand_names = { 0:'hight card', 1:'pair', 2:'2pair', 3:'3pair', 4:'straight',
        5: 'flush', 6:'full house', 7:'4kind', 8: 'none', 9: 'straight flush'}

def hand_percentages(n=80000):
    counts = [0]*10
    for i in range (n/10):
        for hand in deal_cards(10):
            rank = hand_rank(hand)[0]
            counts[rank]+= 1
    for i in reversed(range(10)):

        print "%14s: %6.3f %%" % (hand_names[i],100.*counts[i]/n)

    



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
hand_percentages(n=100000)




