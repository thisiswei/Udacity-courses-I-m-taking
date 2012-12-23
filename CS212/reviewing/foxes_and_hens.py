
import random

def memo(f):
    cache = {}
    def _f(*args):
        try:
            return cache[args]
        except KeyError:
            cache[args] = result = f(*args)
            return result
        except TypeError:
            return fn(args)
    return _f

def foxes_and_hens(stretegy, foxes=7, hens=45):
    state = (score, yard, cards) = 0, 0, 'F'*foxes + 'H'*hens
    while cards:
        action = stretegy(state)
        state = (score, yard, cards) = do(action, state)
    return score + yard

def do(action, state):
    score, yard, cards = state
    dealt_card = random.choice(cards)
    remind_cards = cards.replace(dealt_card, '', 1)
    if action == 'gather':
        state =  score + yard, 0
    if action == 'wait':
        if dealt_card == 'F':
            state = score, 0
        else:
            state = score, yard+1
    return tuple(list(state)+[remind_cards])

#----stretegies--------
def take5(state):
    score, yard, cards = state
    return 'wait' if yard<5 else 'gather'
#--my_stretegy-----
@memo
def FH(state):
    score, yard, cards = state
    if not cards:
        return score + yard
    elif not cards.count('F'):
        return score + yard + len(cards)
    else:
        return max(Q_fh(state, action, FH)
                   for action in ['wait', 'gather']) 
@memo
def Q_fh(state, action, U):
    score, yard, cards = state 
    fox_counts = cards.count('F')
    hen_counts = cards.count('H')
    card_counts = float(len(cards))
    if action == 'gather': 
        return (U((score + yard, 0, cards[1:])) * fox_counts +
                U((score + yard, 0, cards[:-1])) * hen_counts) / card_counts
    # probability of getting a 'F' * utility of newstate(<-with 'F' # removed) + ....
    if action == 'wait':
        return (U((score, 0, cards[1:]))*fox_counts +
                U((score, yard+1, cards[:-1]))*hen_counts) / card_counts
    raise ValueError

def removed(cards, remove):
    return cards.replace(remove, '', 1)

def best_action(state, actions, Q, U):
    def EU(action): return Q(state, action, U)
    return max(actions, key=EU)

def best_stretegy(state):
    return best_action(state, ['wait', 'gather'], Q_fh, FH) 

def average_score(stretegy, N=1000):
    return sum(foxes_and_hens(stretegy) for _ in range(N)) / N+0.

def superior(A, B=take5):
    return average_score(A) - average_score(B) > 1.5 

# ---test----------

def test():
    gather = do('gather', (4, 5, 'F'*4 + 'H'*10))
    assert (gather == (9, 0, 'F'*3 + 'H'*10) or 
            gather == (9, 0, 'F'*4 + 'H'*9))
    
    wait = do('wait', (10, 3, 'FFHH'))
    assert (wait == (10, 4, 'FFH') or
            wait == (10, 0, 'FHH'))
    
    assert best_
    return 'tests pass' 
    
# >>> average_score(best_stretegy)
# 32
