from collections import defaultdict 

Fail = None
# --------- pour problem ----------------
def pour(X, Y, goal, start=(0, 0)):
    if goal in start:
        return [start]
    explored = set()
    frontier = [[start]]
    while frontier:
        path = frontier.pop(0)
        x, y = path[-1]
        for state, action in successors(x, y, X, Y).items():
            if state not in explored:
                explored.add(state)
                path2 = path + [action, state]
                if goal in state:
                    return path2
                else:
                    frontier.append(path2)
    return Fail

def successors(x, y, X, Y): 
    assert x <= X and y <= Y
    return {((0, x+y) if x+y <= Y else (x-(Y-y), Y)): 'X->Y',
            ((x+y, 0) if x+y <= X else (X, y-(X-x))): 'X<-Y',
            (X, y): 'fill X', (x, Y): 'fill Y',
            (0, y): 'empty X', (x, 0): 'empty Y'} 

# --------- pour problem ----------------


#-----------cross bridge problem ----------------------
def bsuccessors(state):
    here, there = state
    if 'light' in here:
        return dict(((here - frozenset([a, b, 'light']),
                   there | frozenset([a, b, 'light'])), 
                   (a, b, '->'))
                   for a in here if a != 'light'
                   for b in here if b != 'light')
    else:
        return dict(((here | frozenset([a, b, 'light']),
                    there - frozenset([a, b, 'light'])),
                    (a, b, '<-'))
                    for a in there if a != 'light'
                    for b in there if b != 'light')    

def pathcost(path):
    if len(path)<3:
        return 0
    else:
        return path[-2][-1]

def bcost(action):
    a, b, _ = action
    return max(a, b)

def bridge(here):
    here = frozenset(here) | frozenset(['light'])
    explored = set()
    frontier = [[(here, frozenset())]]
    if not here:
        return frontier[0]
    while frontier:
        path = frontier.pop(0)
        s = path[-1]
        here1, there1 = s
        if not here1 or here1 == set(['light']):
            return path   
        explored.add(s)
        pcost = pathcost(path)
        for state, action in bsuccessors(s).items():
            if state not in explored:
                totalcost = pcost + bcost(action)
                path2 = path + [(action, totalcost), state] 
                frontier.append(path2)
                frontier.sort(key=pathcost)
    return Fail


#-----------cross bridge problem ----------------------

#----------  missionaries cannibals--------------------

def csuccessors(state):
    M1, C1, B1, M2, C2, B2 = state
    if C1 > M1 > 0 or C2 > M2 > 0:
        return {}
    if B1 > 0:
        return dict((add(state, d), action+'->')
                   for d, action in delta.items())
    else:
        return dict((sub(state, d), action+'<-')
                   for d, action in delta.items())

delta = {(-2, 0, -1,     2, 0, 1): 'MM', 
         (0, -2, -1,     0, 2, 1): 'CC',
         (-1, -1, -1,    1, 1, 1): 'MC', 
         (0, -1, -1,     0, 1, 1): 'C',
         (-1, 0, -1,     1, 0, 1): 'M'}

def add(X, Y):
    return tuple(x+y for (x, y) in zip(X, Y)) 

def sub(X, Y):
    return tuple(x-y for (x, y) in zip(X, Y))


def missionaries_cannibals(start=(3, 3, 1, 0, 0, 0), goal=None):
    if not goal:
        goal = (0, 0, 0) + start[:3]
    if goal == start: return [start]
    frontier = [[start]]
    explored = set()
    while frontier:
        path = frontier.pop(0)
        s = path[-1]
        for state, action in csuccessors(s).items():
            if state not in explored:
                explored.add(state)
                path2 = path + [action, state]
                if goal == state:
                    return path2
                else:
                    frontier.append(path2)
    return Fail
#---------------------------------------------------------------

def lowest_cost_search(start, successors, is_goal, action_cost):
    """Return the lowest cost path, starting from start state,
    and considering successors(state) => {state:action,...},
    that ends in a state for which is_goal(state) is true,
    where the cost of a path is the sum of action costs,
    which are given by action_cost(action)."""

    if is_goal(start): return [start]
    frontier = [[start]]
    explored = set()
    while frontier:
        path = frontier.pop(0)
        s = path[-1]
        if is_goal(s): return path
        pcost = path_cost(path)
        explored.add(s)
        for state, action in successors(s).items():
            if state not in explored:
                totalcost = pcost + action_cost(action)
                path2 = path + [(action, totalcost), state]
                add_to_frontier(frontier, path2)
    return Fail

def shortest_path_search(start, successors, is_goal):
    if is_goal(start): return [start]
    explored = set()
    frontier = [[start]]
    while frontier:
        path = frontier.pop(0)
        s = path[-1]
        for state, action in successors(s).items():
            if state not in explored:
                explored.add(state)
                path2 = path + [action, state]
                if is_goal(state):
                    return path2
                else:
                    frontier.append(path2)
    return Fail

#---         ---         ---   homework      ---         ---        
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



def more_pour_problem(capacities, goal, start=None):
    """The first argument is a tuple of capacities (numbers) of glasses; the
    goal is a number which we must achieve in some glass.  start is a tuple
    of starting levels for each glass; if None, that means 0 for all.
    Start at start state and follow successors until we reach the goal.
    Keep track of frontier and previously explored; fail when no frontier.
    On success return a path: a [state, action, state2, ...] list, where an
    action is one of ('fill', i), ('empty', i), ('pour', i, j), where
    i and j are indices indicating the glass number."""
    # your code here
    def is_goal(state): return goal in state 
    L = range(len(capacities)) 

    def mp_successors(state): 
        d = {}
        for i in L:
            d[replace(state, i, capacities[i])] = 'fill', i
            d[replace(state, i, 0)] = 'empty', i
            for j in L:
                if i != j:
                    amount = min(state[i], capacities[j] - state[j])
                    newstate = replace(state, i, state[i] - amount)
                    d[replace(newstate, j, state[j] + amount)] = 'pour', i, j
        return d 

    if not start: start = (0,) * len(capacities)
    return shortest_path_search(start, mp_successors, goal)


def replace(state, i, val):
    s = list(state)
    s[i] = val
    return tuple(s)

#-------------------- ------------homework 3------- ------------------- ------------------

# User Instructions
# 
# Write a function, subway, that takes lines as input (read more about
# the **lines notation in the instructor comments box below) and returns
# a dictionary of the form {station:{neighbor:line, ...}, ... } 
#
# For example, when calling subway(boston), one of the entries in the 
# resulting dictionary should be 'foresthills': {'backbay': 'orange'}. 
# This means that foresthills only has one neighbor ('backbay') and 
# that neighbor is on the orange line. Other stations have more neighbors:
# 'state', for example, has 4 neighbors.
#
# Once you've defined your subway function, you can define a ride and 
# longest_ride function. ride(here, there, system) takes as input 
# a starting station (here), a destination station (there), and a subway
# system and returns the shortest path.
#
# longest_ride(system) returns the longest possible ride in a given 
# subway system. 

# -------------
# Grading Notes
#
# The subway() function will not be tested directly, only ride() and 
# longest_ride() will be explicitly tested. If your code passes the 
# assert statements in test_ride(), it should be marked correct.

def subway(**lines):
    """Define a subway map. Input is subway(linename='station1 station2...'...).
    Convert that and return a dict of the form: {station:{neighbor:line,...},...}"""
    d = collections.defaultdict(dict) 
    for line, stations in lines.items():
        for s1, s2 in overlapping(stations.split()):
            d[s1][s2] = line
            d[s2][s1] = line
    return d

def overlapping(stations):
    return [stations[i:i+2] for i in range(len(stations)-1)]



boston = subway(
    blue='bowdoin government state aquarium maverick airport suffolk revere wonderland',
    orange='oakgrove sullivan haymarket state downtown chinatown tufts backbay foresthills',
    green='lechmere science north haymarket government park copley kenmore newton riverside',
    red='alewife davis porter harvard central mit charles park downtown south umass mattapan')

def ride(here, there, system=boston):
    "Return a path on the subway system from here to there."
    ## your code here
    return shortest_path_search(here, lambda s: system[s], lambda t: t==there) 

def longest_ride(system):
    """"Return the longest possible 'shortest path' 
    ride between any two stops in the system."""
    ## your code here
    stations = set(s for dic in system.values() for s in dic)
    return max([ride(a, b, system) for a in stations for b in stations], key=len)


def path_states(path):
    "Return a list of states in this path."
    return path[0::2]
    
def path_actions(path):
    "Return a list of actions in this path."
    return path[1::2]

def test_ride():
    assert ride('mit', 'government') == [
        'mit', 'red', 'charles', 'red', 'park', 'green', 'government']
    assert ride('mattapan', 'foresthills') == [
        'mattapan', 'red', 'umass', 'red', 'south', 'red', 'downtown',
        'orange', 'chinatown', 'orange', 'tufts', 'orange', 'backbay', 'orange', 'foresthills']
    assert ride('newton', 'alewife') == [
        'newton', 'green', 'kenmore', 'green', 'copley', 'green', 'park', 'red', 'charles', 'red',
        'mit', 'red', 'central', 'red', 'harvard', 'red', 'porter', 'red', 'davis', 'red', 'alewife']
    assert (path_states(longest_ride(boston)) == [
        'wonderland', 'revere', 'suffolk', 'airport', 'maverick', 'aquarium', 'state', 'downtown', 'park',
        'charles', 'mit', 'central', 'harvard', 'porter', 'davis', 'alewife'] or 
        path_states(longest_ride(boston)) == [
                'alewife', 'davis', 'porter', 'harvard', 'central', 'mit', 'charles', 
                'park', 'downtown', 'state', 'aquarium', 'maverick', 'airport', 'suffolk', 'revere', 'wonderland'])
    assert len(path_states(longest_ride(boston))) == 16
    return 'test_ride passes'

print test_ride()





