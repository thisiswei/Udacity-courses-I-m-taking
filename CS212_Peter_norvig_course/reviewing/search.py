
def pour(X, Y, goal, start=(0, 0)):
    if goal in start:
        return [start]
    explored = set()
    frontier = [[start]]
    while frontier:
        path = frontier.pop(0)
        x, y = path[-1]
        for state, action in successor(x, y, X, Y).items():
            if state not in explored:
                explored.add(state)
                path2 = path + [action, state]
                if goal in state:
                    return path2
                else:
                    frontier.append(path2)
    return Fail

Fail = []

def successor(x, y, X, Y):
    assert x <= X and y <= Y
    return {(X,y):'Fill X',
            (x,Y):'Fill Y',
            (0,y):'empty x',
            (x,0):'empty y',
            ((x-(Y-y), Y) if x > Y-y else (0, y+x)): 'x->y',
            ((X, Y-(X-x)) if y > X-x else (x+y, 0)): 'x<-y'}

def bridge(here):
    here = frozenset(here) | frozenset(['light'])
    explored = set()
    frontier = [[(here, frozenset(), 0)]]
    if not here:
        return frontier[0]
    while frontier:
        path = frontier.pop(0)
        s = path[-1]
        for state, action in bsuccessor(s).items():
            if state not in explored:
                explored.add(state)
                path2 = path + [action, state]
                if not in here:
                    return path2
                else:
                    frontier.append(path2)
                    frontier.sort(key=elapsed_time)
    return Fail




