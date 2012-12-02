def pour_problem(X,Y,goal,start=(0,0)):
    if goal in start:
        return [start]
    explored = set()
    frontier = [[start]] 
    while frontier:
        path = frontier.pop(0)
        x,y = path[-1]
        for (state,action) in successor(x,y,X,Y).items():
            if state not in explored:
                explored.add(state)
                path2 = path + [action,state]
                if goal in state:
                    return path2
                else:
                    frontier.append(path2)
    return []
                
                


def successor(x,y,X,Y):#x,y:current water level, X,Y: full capacity
    return {(X,y):'Fill up X',
            (x,Y):'Fill up Y',
            (0,y):'Empty X',
            (x,0):'Emtry Y',
            (0,x+y) if x+y <= Y else (x-(Y-y),Y) :'Pour X->Y',
            (x+y,0) if x+y <= X else (X,y-(X-x)):'Pour Y->X'
            }

import doctest

class Test: """
>>> successor(0, 0, 4, 9)
{(0, 9): 'Fill up Y', (0, 0): 'Pour Y->X', (4, 0): 'Fill up X'}
    """

print(doctest.testmod())
