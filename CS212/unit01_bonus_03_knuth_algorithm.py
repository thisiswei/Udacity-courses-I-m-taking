
def shuff(deck):
    n = len(deck)
    for i in range(n-1):
        swap(deck,i,random.randrange(i,n))

def swap(deck,i,j):
    deck[i],deck[j] = deck[j],deck[i]
