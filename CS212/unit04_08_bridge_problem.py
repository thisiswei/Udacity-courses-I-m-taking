def bridge_problem(here):
    here = frozenset(here) | frozenset(['light'])
    explored = set()
    frontier = [ [(here,frozenset(),0)] ]
    if not here:
        return frontier[0]
    while frontier:
        path = frontier.pop(0)
        for (state,action) in bsuccessor(path[-1]).items():
            if state not in explored:
                here,there,t = state
                explored.add(state)
                path2 = path + [action,state]
                if not here:
                    return path2
                else:
                    frontier.append(path2)
                    frontier.sort(key=elapsed_time)
    return []

def elapsed_time(path): 
    return path[-1][2]

#state is represented by people over here side ,there side,light and total elpased
#time, bsuccesor generate all the possible state outcome according to specific
#action 
def bsuccessor(state): 
    here,there,t = state 
    if 'light' in here:
        return dict(((here - frozenset([a,b,'light']),
                      there | frozenset([a,b,'light']),
                      t + max(a,b)),
                      (a,b,'->'))
                    for a in here if a is not 'light'
                    for b in here if b is not 'light')
    else:
        return dict(((here | frozenset([a,b,'light']),
                      there - frozenset([a,b,'light']),
                      t + max(a,b)),
                      (a,b,'<-'))
                      for a in there if a is not 'light'
                      for b in there if b is not 'light')


print bridge_problem([1,2,5,10])[1::2]





