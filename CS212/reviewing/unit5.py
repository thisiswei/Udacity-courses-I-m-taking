# -----------------
# User Instructions
# 
# Write a function, play_pig, that takes two strategy functions as input,
# plays a game of pig between the two strategies, and returns the winning
# strategy. Enter your code at line 41.
#
# You may want to borrow from the random module to help generate die rolls.

import random
from functools import update_wrapper

possible_moves = ['roll', 'hold']
other = {1:0, 0:1}
goal = 40

def decorator(d):
    def _d(fn):
        return update_wrapper(d(fn), fn)
    update_wrapper(_d, d)
    return _d

@decorator
def memo(f):
    CACHE = {}
    def _f(*args):
        try:
            return CACHE[args]
        except KeyError:
            CACHE[args] = result = f(*args)
            return result
        except TypeError:
            return f(*args)
    return _f

def clueless(state):
    "A strategy that ignores the state and chooses at random from possible moves."
    return random.choice(possible_moves)

def hold(state):
    """Apply the hold action to a state to yield a new state:
    Reap the 'pending' points and it becomes the other player's turn."""
    (p, me, you, pending) = state
    return (other[p], you, me+pending, 0)

def roll(state, d):
    """Apply the roll action to a state (and a die roll d) to yield a new state:
    If d is 1, get 1 point (losing any accumulated 'pending' points),
    and it is the other player's turn. If d > 1, add d to 'pending' points."""
    (p, me, you, pending) = state
    if d == 1:
        return (other[p], you, me+1, 0) # pig out; other player's turn
    else:
        return (p, me, you, pending+d)  # accumulate die roll in pending

def rolldies():
    while True:
        yield random.randint(1, 6)

def play_pig(A, B, dies=rolldies()):
    """Play a game of pig between two players, represented by their strategies.
    Each time through the main loop we ask the current player for one decision,
    which must be 'hold' or 'roll', and we update the state accordingly.
    When one player's score exceeds the goal, return that player."""
    strategies = [A, B]
    state = (0, 0, 0, 0)
    while True:
        p, me, you, pending = state
        if me+pending >= goal:
            return strategies[p]
        if you >= goal:
            return strategies[other[p]]
        action = strategies[p](state)
        if action == 'roll':
            state = roll(state, next(dies))
        else:
            state = hold(state)

def Q_pig(state, action, Pwin):
    if action == 'hold':
        return 1 - Pwin(hold(state))
    if action == 'roll':
        return (1 - Pwin(roll(state, 1))+
                sum(Pwin(roll(state, d)) for d in (2, 3, 4, 5, 6))) / 6.
    raise ValueError

def pig_actions(state):
    _, _, _, pending = state
    return ['roll', 'hold'] if pending else ['roll']

@memo
def Pwin(state):
    p, me, you, pending = state
    if me+pending >= goal:
        return 1
    if you >= goal:
        return 0
    return max(Q_pig(state, action, Pwin)
               for action in pig_actions(state))
@memo
def win_diff(state):
    p, me, you, pending = state
    if me+pending >= goal or you >= goal:
        return (me+pending-you)
    else:
        return max(Q_pig(state, action, win_diff)
                   for action in pig_actions(state))

def best_action(state, actions, Q, U):
    def EU(action): return Q(state, action, U)
    return max(actions(state) ,key=EU)        

def max_wins(state):
    return best_action(state, pig_actions, Q_pig, Pwin)

def max_diff(state):
    return best_action(state, pig_actions, Q_pig, win_diff)
        
def always_roll(state):
    return 'roll'

def always_hold(state):
    return 'hold'

def test():
    for _ in range(10):
        winner = play_pig(always_hold, always_roll)
        assert winner.__name__ == 'always_roll'
    return 'tests pass'

print test()




