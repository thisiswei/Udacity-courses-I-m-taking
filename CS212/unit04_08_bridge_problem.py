def bridge_problem(here):
    here = frozenset(here) | frozenset(['light'])
    explored = set()
    frontier = [ [(here,frozenset())] ]
    if not here:
        return frontier[0]
    while frontier:
        path = frontier.pop(0)
        here,there = state1 = path[-1]
        if not here or here == set(['light']):
            return path 
        explored.add(state1)
        pcost = path_cost(path)
        for (state,action) in bsuccessor1(state1).items(): 
            if state not in explored:
                total_cost =pcost + bcost(action)
                path2 = path + [(action,total_cost),state]
                frontier.append(path2)
                frontier.sort(key=path_cost)
    return []


#-------- ------- ------- ------- ------
#solution 2

def bridge_problem2(here):
    start =( frozenset(here) | frozenset(['light']) , frozenset() )
    return lowest_cost_search(start,bsuccessor1,gone,bcost)

def gone(state):
    here ,there =state
    return len(here) == 0 or here == set(['light']) 

def lowest_cost_search(start,successors,is_goal,action_cost):
    explored  =  set()
    frontier = [[start]]
    while frontier:
        path = frontier.pop(0)
        s    = final_state(path)
        if is_goal(s):
            return path
        explored.add(s)
        pcost = path_cost(path) 
        for (state,action) in successors(s).items():
            if state not in explored:
                total_cost  = pcost+ action_cost(action)
                path2 = path + [ (action,total_cost),state ] 
                add_to_frontier(frontier,path2)
    return []

def add_to_frontier(frontier, path):
    "Add path to frontier, replacing costlier path if there is one."
    old = None
    for i,p in enumerate(frontier):
        if final_state(p) == final_state(path):
            old = i
            break
    if old is not None and path_cost(frontier[old]) < path_cost(path):
        return 
    elif old is not None:
        del frontier[old] 
    frontier.append(path)
    frontier.sort(key=path_cost)

def final_state(path):
    return path[-1]

#----- ---- ---- ---- ---- ---- ---- --- solutin2 end-----

def path_cost(path): 
    if len(path)<2:
        return 0
    else:
        return path[-2][-1]
def bcost(action):
    a,b,c = action 
    return max(a,b)



#state is represented by people over here side ,there side,light and total elpased
#time, bsuccesor generate all the possible state outcome according to specific
#action 
def bsuccessor1(state):
    here,there = state
    if 'light' in here:
        return dict(((here - frozenset([a,b,'light']),
                      there | frozenset([a,b,'light'])),
                     (a,b,'->'))
                    for a in here if a is not 'light'
                    for b in here if b is not 'light')
    else:
        return dict(((here | frozenset([a,b,'light']),
                      there - frozenset([a,b,'light'])),
                      (a,b,'<-'))
                      for a in there if a is not 'light'
                      for b in there if b is not 'light')

def path_states(path):
    return path[0::2]

def path_actions(path):
    return path[1::2]


def path(problem):
    return [ b[0] for b in  problem[1::2] ]

import doctest

class Test:"""

>>> path_cost(bridge_problem([1,2,5,10]))
17
>>> path_cost(bridge_problem([0,1,1,10]))
11
>>> path_actions(bridge_problem([1,2,5,10]))
[((2, 1, '->'), 2), ((1, 1, '<-'), 3), ((5, 10, '->'), 13), ((2, 2, '<-'), 15), ((2, 1, '->'), 17)]
>>> [path_cost(bridge_problem([1,2,5,10][:N])) for N in range(5)]
[0, 1, 2, 8, 17]
>>> path_cost( (bridge_problem2([1,2,5,10])) )
17

#both path get 17
>>> S1 = [(2, 1, '->'), (2, 2, '<-'), (5, 10, '->'), (1, 1, '<-'), (2, 1, '->')] 
>>> S2 = [(2, 1, '->'), (1, 1, '<-'), (5, 10, '->'), (2, 2, '<-'), (2, 1, '->')]
>>> path( bridge_problem2([1,2,5,10]) ) in (S1, S2)
True
"""
print doctest.testmod()



