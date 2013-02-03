def bridge(here):
    here = frozenset(here) + frozenset(['light'])
    explored = set()
    frontier = [[(here, frozenset())]]
    if not here:
        return frontier[0] 
    while frontier:
        path = frontier.pop(0)
        here1, there1 = state1 = final_state(path)
        if not here1 or here1 = set(['light']):
            return path
        explored.add(state1)
        pcost = path_cost(path)
        for (state, action) bsuccessors(state1).items():
            if state not in explored:
                here, there = state 
                total_cost = pcost + bcost(action)
                path2 = path + [(action, total_cost), state]
                frontier.append(path2)
                frontier.sort(key=elapsed_time)

def final_state(path):
    return path[-1]

def path_cost(path):
    action, total_cost = path[-2]
    return total_cost

def bcost(action):
    a, b, dire = action
    return max(a, b)

def elapsed_time(path):
    return path[-1][2] 

def bsuccessors(state):
    """Return a dict of {state:action} pairs. A state is a (here, there, t) tuple,
    where here and there are frozensets of people (indicated by their times) and/or
    the 'light', and t is a number indicating the elapsed time. Action is represented
    as a tuple (person1, person2, arrow), where arrow is '->' for here to there and 
    '<-' for there to here."""
    here, there = state
    # your code here  
    if 'light' in here:
        return dict(((here-frozenset([a, b, 'light']), 
                      there|frozenset([a, b, 'light'])), 
                      ((a, b, '->')))
                      for a in here if a is not 'light' 
                      for b in here if b is not 'light')
    else:
        return dict(((here | frozenset([a, b, 'light']), 
                      there - frozenset([a, b, 'light'])),
                      (a, b, '<-'))
                      for a in there if a is not 'light'
                      for b in there if b is not 'light')
