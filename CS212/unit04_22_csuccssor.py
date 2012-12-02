#cross river problem, in either side if c > m  ,m will get eaten
#b == boat ,  m1,c1,b1,m2,c2,b2  to represent left and right states


# -----------------
# User Instructions
# 
# Write a function, csuccessors, that takes a state (as defined below) 
# as input and returns a dictionary of {state:action} pairs. 
#
# A state is a tuple with six entries: (M1, C1, B1, M2, C2, B2), where 
# M1 means 'number of missionaries on the left side.'
#
# An action is one of the following ten strings: 
#
# 'MM->', 'MC->', 'CC->', 'M->', 'C->', '<-MM', '<-MC', '<-M', '<-C'
# where 'MM->' means two missionaries travel to the right side.
# 
# We should generate successor states that include more cannibals than
# missionaries, but such a state should generate no successors.

#http://en.wikipedia.org/wiki/Missionaries_and_cannibals_problem?course=cs212

def mc_problem(start=(3,3,1,0,0,0),goal=None):
    if goal is None:
        goal = (0,0,0)+start[:3]
    if start == goal:
        return [start]
    explored = set()
    frontier = [[start]]
    while frontier:
        path = frontier.pop(0)
        state = path[-1]
        for state1,action in csuccessors(state).items():
            if state1 not in explored: 
                explored.add(state1)
                path2 = path + [action,state1]
                if state1 == goal:
                    return path2
                else: 
                    frontier.append(path2)
    return []
#--------------solution 2 -------------- -------------- -------------- 
def mc_problem2(start=(3, 3, 1, 0, 0, 0), goal=None):
    if goal is None:
        goal = (0, 0, 0) + start[:3]
    return shortest_path_search(start,csuccessors,all_gone)

def all_gone(state):
    return state[:3] == (0, 0, 0)
def shortest_path_search(start, successors, is_goal):
    """Find the shortest path from start state to a state
    such that is_goal(state) is true."""
    if is_goal(start):
        return [start]
    explored = set()
    frontier = [ [start] ] 
    while frontier:
        path = frontier.pop(0)
        s = path[-1]
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
#--------------------------------------------- -------------- 

def csuccessors(state):
    M1,C1,B1,M2,C2,B2 = state
    if C1>M1>0 or C2>M2>0:
        return {}
    items = []
    #boat on leftside 
    if B1>0:
        for delta,a in deltas.items():
            x = sub(state,delta)
            if all(val >= 0 for val in x):
                items.append((sub(state,delta),a+'->'))
    if B2>0:
        for delta,a in deltas.items():
            x = add(state,delta)
            if all(val >=0 for val in x):
                items.append((add(state,delta),a+'<-'))
    return dict(items)




deltas = {(2,0,1,  -2,0,-1):  "MM",
          (0,2,1,  0,-2,-1):  "CC",
          (1,1,1,  -1,-1,-1): "MC",
          (1,0,1,  -1,0,-1):  "M",
          (0,1,1,  0,-1,-1):  "C"
          }

def add(A,B):
    return tuple(a+b for a,b in zip(A,B))

def sub(A,B):
    return tuple(a-b for a,b in zip(A,B))

def path_action(path):return path[1::2]

import doctest
#answer is Move 2 cannibals to the left,
#          Move 1 cannibal back to the right
#          Move 2 cannibal to the left
#          Move 1 cannibal back to right
#          etc solution can be found at
#          http://www.novelgames.com/gametips/details.php?id=29 

class Test:"""
>>> path_action(mc_problem(start=(3,3,1,0,0,0)))
['CC->', 'C<-', 'CC->', 'C<-', 'MM->', 'MC<-', 'MM->', 'C<-', 'CC->', 'C<-', 'CC->']
>>> path_action(mc_problem2(start=(1, 1, 1, 0, 0, 0)))
['MC->']  

"""
print doctest.testmod()
