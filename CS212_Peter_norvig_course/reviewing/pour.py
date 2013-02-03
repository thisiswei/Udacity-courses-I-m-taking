def pour(X,Y,goal,start=(0,0)):
    if goal in start: return [start]
    frontier = [[start]]
    explored = set()
    while frontier:
        path = frontier.pop(0)
        x, y = state[-1]
        for action, state in successors(x, y, X, Y).items():
            if state not in explored:
                explored.add(state)
                path2 = path + [action, state]
                if goal in state:
                    return path2
                else:
                    frontier.append(path2)
    return []

def successors(x, y, X, Y):
    return {(0, y+x) if Y-y >= x else (x-(Y-y),Y): 'x->y',
            (x+y, 0) if x+y <= X else (X, y-(X-x)): 'x<-y',
            (X, y): 'fillup X',
            (x, Y): 'fillup Y',
            (0, y): 'empty X',
            (x, 0): 'empty Y'
            }

