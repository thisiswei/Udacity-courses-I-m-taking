'shortest path search'

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
    return False

'lowest cost search'

def lowest(start, successors, is_goal, action_cost):
    explored = set()
    frontier = [[start]]
    while frontier:
        path = frontier.pop(0)
        s = path[-1]
        if is_goal(s): return path
        explored.add(s)
        pcost = path_cost(path)
        for state, action in successors(s).items():
            if state not in explored:
                explored.add(state)
                total_cost = pcost + action_cost(state)
                path2 = path + [(action, total_cost), state]
                add_to_frontier(frontier, path2)
    return False

def add_to_frontier(frontier, path):
    "Add path to frontier, replacing costlier path if there is one."
    old = None
    for i, p in enumerate(frontier):
        if final_state(path) == final_state(p):
            old = i
            break
    if old is not old and path_cost(frontier[old]) < path_cost(path):
        return
    if old is not:
        del frontier[old]
    frontier.append(path)
    frontier.sort(key = path_cost)



def final_state(path): return path[-1]

def path_cost(path):
    if len(path)<3:
        return 0
    else:
        action, total_cost = path[-2]
        return total_cost

