from functools import update_wrapper

goal = 40 
other = {1:0, 0:1}

#------------------------- decorater,memoize ----------------
def decorator(d):
    def _d(fn):
        return update_wrapper(d(fn),fn)
    update_wrapper(_d,d)
    return _d

@decorator
def memo(f):
    cache = {}
    def _f(*args):
        try: 
            return cache[args]
        except KeyError:
            cache[args] = result = f(*args)
            return result
        except TypeError:
            return f(args)
    return _f 
# -----------------  -----decorator,memoize end -----------  --------------- 
def max_wins(state):
    return best_action(state,pig_actions,Q_pig,Pwin) 

def best_action(state,actions,Q,U):
    'return the optimal action for state,Given utility U,Quality Q'
    def EU(action): return Q(state,action,U)
    return max(actions(state), key = EU)
 
def Q_pig(state,action,Pwin):
    if action == 'hold':
        return 1 - Pwin( hold(state) )   # 1 - other_player's_probability_of_taking the new_state -> hold(state)
    if action == 'roll':
        return (1 - Pwin( roll(state,1) )   # 1 - probability of rolling a 1 
               + sum( Pwin( roll(state, d))  for d in  (2,3,4,5,6) ) ) / 6.    #probability of rolling others 
    raise ValueError
  
@memo
def Pwin(state):
    p, me, you, pending = state
    if me + pending >= goal:
        return 1
    elif you >= goal:
        return 0
    else:
        return max(Q_pig(state,action,Pwin) 
                   for action in pig_actions(state)) 

def pig_actions(state):
    _, _, _, pending = state 
    return ['roll','hold'] if pending else ['roll'] 

def roll(state,d):
    p, me, you, pending = state
    if d == 1 : 
        return (other[p], you, me+1, 0) #pig out, other player's turn
    else:
        return (p, me, you, pending+d)

def hold(state):
    p, me, you, pending = state
    return (other[p], you, me+pending, 0) 


def test():
    assert(max_wins((1, 5, 34, 4)))   == "roll"
    assert(max_wins((1, 18, 27, 8)))  == "roll"
    assert(max_wins((0, 23, 8, 8)))   == "roll"
    assert(max_wins((0, 31, 22, 9)))  == "hold"
    assert(max_wins((1, 11, 13, 21))) == "roll"
    assert(max_wins((1, 33, 16, 6)))  == "roll"
    assert(max_wins((1, 12, 17, 27))) == "roll"
    assert(max_wins((1, 9, 32, 5)))   == "roll"
    assert(max_wins((0, 28, 27, 5)))  == "roll"
    assert(max_wins((1, 7, 26, 34)))  == "hold"
    assert(max_wins((1, 20, 29, 17))) == "roll"
    assert(max_wins((0, 34, 23, 7)))  == "hold"
    assert(max_wins((0, 30, 23, 11))) == "hold"
    assert(max_wins((0, 22, 36, 6)))  == "roll"
    assert(max_wins((0, 21, 38, 12))) == "roll"
    assert(max_wins((0, 1, 13, 21)))  == "roll"
    assert(max_wins((0, 11, 25, 14))) == "roll"
    assert(max_wins((0, 22, 4, 7)))   == "roll"
    assert(max_wins((1, 28, 3, 2)))   == "roll"
    assert(max_wins((0, 11, 0, 24)))  == "roll" 
    return 'tests pass'

print test()
