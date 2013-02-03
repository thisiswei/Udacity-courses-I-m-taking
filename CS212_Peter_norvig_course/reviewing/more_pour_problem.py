# -----------------
# User Instructions
# 
# In this problem, you will solve the pouring problem for an arbitrary
# number of glasses. Write a function, more_pour_problem, that takes 
# as input capacities, goal, and (optionally) start. This function should 
# return a path of states and actions.
#
# Capacities is a tuple of numbers, where each number represents the 
# volume of a glass. 
#
# Goal is the desired volume and start is a tuple of the starting levels
# in each glass. Start defaults to None (all glasses empty).
#
# The returned path should look like [state, action, state, action, ... ]
# where state is a tuple of volumes and action is one of ('fill', i), 
# ('empty', i), ('pour', i, j) where i and j are indices indicating the 
# glass number. 

def more_pour(capacities, goal, start=None): 
    if not start:
        start = (0,) * len(capacities)
    def is_goal(state): return goal in state

    def successors(state): 
        indices = range(len(capacities))
        dics = {}
        for i in indices:
            dics[replace(state, i, capacities[i])] = ('fill', i)
            dics[replace(state, i, 0)] = ('empty', i)
            for j in indices:
                if j != i:
                    amount = min(capacities[j]-state[j], state[i]) 
                    state2 = replace(state, i, state[i]-amout)
                    dics[replace(state2, j, state[j]+amout)] = ('pour', i, j) 
        return dics 
    return shortest(start, successors, is_goal)

def replace(seq, i, val):
    s = list(seq)
    s[i] = val
    return type(seq)(s)




def shortest(start, successors, is_goal):
    if is_goal(start): return [[start]]
    explored = set()
    frontier = [[start]]
    while frontier:
        path = frontier.pop(0)
        s = path[-1]
        explored.add(s)
        for (state, action) in successors(s).items():
            if state not in explored:
                explored.add(state)
                path2 = path + [action, state]
                if is_goal(state):
                    return path2
                else:
                    frontier.append(path2)
    return Fail

Fail = []
 

def test_more_pour():
    assert more_pour_problem((1, 2, 4, 8), 4) == [
        (0, 0, 0, 0), ('fill', 2), (0, 0, 4, 0)]
    assert more_pour_problem((1, 2, 4), 3) == [
        (0, 0, 0), ('fill', 2), (0, 0, 4), ('pour', 2, 0), (1, 0, 3)] 
    starbucks = (8, 12, 16, 20, 24)
    assert not any(more_pour_problem(starbucks, odd) for odd in (3, 5, 7, 9))
    assert all(more_pour_problem((1, 3, 9, 27), n) for n in range(28))
    assert more_pour_problem((1, 3, 9, 27), 28) == []
    return 'test_more_pour passes'

print test_more_pour()
