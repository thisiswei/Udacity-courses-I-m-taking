" missionary cannibal problem "

import doctest

def mc(start=(3, 3, 1, 0, 0, 0), goal=None):
    if not goal: goal = (0, 0, 0) + start[:3]
    if start == goal: return [start]
    explored = set()
    frontier = [[start]]
    while frontier:
        path = frontier.pop(0)
        s = path[-1]
        explored.add(s)
        for state, action in csuccessors(s).items():
            if state not in explored:
                explored.add(state)
                path2 = path + [action, state]
                if state == goal:
                    return path2
                else:
                    frontier.append(path2)
    return None





def csuccessors(state):
    """Find successors (including those that result in dining) to this
    state. But a state where the cannibals can dine has no successors."""
    # your code here
    M1, C1, B1, M2, C2, B2 = state
    if C1 > M1 or C2 > M2:
        return {}
    if B1 > 0:
        return dict((add(state,d), action+'->') 
                     for d,action in deltas.items())
    else:
        return dict((sub(state,d), '<-'+action)
                     for d,action in deltas.items())

def add(A, B):
    return tuple(a+b for (a, b) in zip(A,B))

def sub(A, B):
    return tuple(a-b for (a, b) in zip(A,B))


           
deltas  =   {(-2,0,-1,   2,0,1): 'MM',
             (0,-2,-1,   0,2,1): 'CC',
             (-1,0,-1,   1,0,1): 'M',
             (0,-1,-1,   0,1,1): 'C',
             (-1,-1,-1,  1,1,1): 'MC'}
    
class Test:"""
>>> mc((1, 2, 1, 0, 0, 0))

>>> mc((1, 0, 1, 0, 0, 0))

>>> mc((1, 1, 1, 0, 0, 0))

>>> mc((2, 1, 1, 0, 0, 0)) 

"""

print doctest.testmod()
