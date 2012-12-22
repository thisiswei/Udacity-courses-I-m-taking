from collections import defaultdict
from functools import update_wrapper

goal = 40
other = {1:0, 0:1}

def decorator(d):
    def _d(fn):
        return update_wrapper(d(fn), fn)
    update_wrapper(_d, d)
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

def dice_roll():
    while True:
        yield random.randint(0, 6)

def play_pig(A, B, roll_dice=dice_roll()):
    """Play a game of pig between two players, represented by their strategies.
    Each time through the main loop we ask the current player for one decision,
    which must be 'hold' or 'roll', and we update the state accordingly.
    When one player's score exceeds the goal, return that player."""
    # your code here
    p = random.choice([0,1])
    state = p, 0, 0, 0
    stretegies = [A, B]
    while True:
        p, me, you, pending = state 
        if me > goal:
            return stretegies[p]
        elif you > goal:
            return stretegies[other[p]]
        elif stretegies[p](state) == 'hold':
            state = hold(state)
        else:
            state = roll(state, next(roll_dice))

# return Quality for the state taking the action

def Q_pig(state, action, Pwin):
    if action == 'hold':
        return 1 - Pwin(hold(state))
    if action == 'roll':
        return (1 - Pwin(roll(state, 1)) +
                sum(Pwin(roll(state, d)) for d in (2,3,4,5,6))) / 6.
    raise ValueError

def P_actions(state): 
    _, _, _, pending = state
    return ['roll', 'hold'] if pending else ['roll']

def roll(state, d):
    p, me, you, pending = state
    return (other[p], you, me+1, 0) if d == 1 else (p, me, you, pending+d)

def hold(state):
    p, me, you, pending = state
    return other[p], you, pending+me, 0

@memo
def Pwin(state):
    (p, me, you, pending) = state
    if me + pending >= goal:
        return 1
    elif you >= goal: 
        return 0
    else:
        return max(Q_pig(state, action, Pwin)
                   for action in P_actions(state))

# play pig using max winning differential 

@memo
def win_diff(state): 
    p, me, you, pending = state
    if me + pending >= goal or you >= goal:
        return me + pending - you
    else:
        return max(Q_pig(state, action, win_diff)
                   for action in P_actions(state))


def best_action(state, actions, Q, U):
    def EU(action): return Q(state, action, U)
    return max(actions(state), key=EU)

def max_win_action(state):
    return best_action(state, P_actions, Q_pig, Pwin)

def max_diff_action(state):
    return best_action(state, P_actions, Q_pig, win_diff)
#----------------------- analyze --------------------------

#  analyze diffenerce between max_win, max_diff 
states = [(0, me, you, pending)
          for me in range(41) 
          for pending in range(41)
          for you in range(41) 
          if me + pending <= goal]
r = defaultdict(int)
for s in states: r[max_win_action(s), max_diff_action(s)] += 1

# >>> dict(r)
#{('hold', 'hold'): 1204,
# ('hold', 'roll'): 381,
# ('roll', 'hold'): 3975,
# ('roll', 'roll'): 29741}

def story():
    r2 = defaultdict(lambda: [0, 0])
    for s in states:
        max_win_decision, max_diff_decision = max_win_action(s), max_diff_action(s)
        if max_win_decision != max_diff_decision:
            i = 0 if max_win_decision == 'roll' else 1
            _, _, _, pending = s
            r2[pending][i] += 1
    for pending, (max_w_rolls_count, max_d_rolls_count) in sorted(r2.items()):
        print '%4d: %3d %3d' % (pending, max_w_rolls_count, max_d_rolls_count) 

# >>> story()
#          who decided to roll
# pending  max_win, max_diff 
#-----------------------------
#   2:  |     0    |      40
#   3:  |     0    |      40
#   4:  |     0    |      40
#   5:  |     0    |      40
#   6:  |     0    |      40
#   7:  |     0    |      40
#   8:  |     0    |      40
#   9:  |     0    |      40
#  10:  |     0    |      28
#  11:  |     0    |      19
#  12:  |     0    |      12
#  13:  |     0    |       2
#  16:  |    11    |       0
#  17:  |    68    |       0
#  18:  |   128    |       0
#  19:  |   201    |       0 # when the pending point is high, 
#  20:  |   287    |       0 # max_diff decide to hold other than max_win,
#  21:  |   327    |       0 # originally we though max_diff would be bold
#  22:  |   334    |       0
#  23:  |   322    |       0
#  24:  |   307    |       0
#  25:  |   290    |       0
#  26:  |   281    |       0
#  27:  |   253    |       0
#  28:  |   243    |       0
#  29:  |   213    |       0
#  30:  |   187    |       0
#  31:  |   149    |       0
#  32:  |   125    |       0
#  33:  |    95    |       0
#  34:  |    66    |       0
#  35:  |    31    |       0
#  36:  |    22    |       0
#  37:  |    16    |       0
#  38:  |    11    |       0
#  39:  |     7    |       0
#  40:  |     1    |       0
#
