import heapq
from collections import defaultdict

def find_best_flights(flights, origin, destination,plans=defaultdict(dict)):
    flights = find_flights(flights)
    openlist = [origin]
    explored = set()
    while len(openlist) > 0:
        start = openlist.pop(0)
        if start not in explored:
            explored.add(start)
            for end in flights[start].keys():
                options = flights[start][end] 
                #print options
                heapq.heapify(options)
                best= heapq.heappop(options)
                plans[start][end] = best[-1]
                openlist.append(end)
    return plans



def find_flights(flights):
    G = {}
    for flight in flights:
        num, origin, dest, depart, arrive, cost = flight
        duration = dura(depart, arrive)
        if origin not in G: G[origin] = {}
        if dest not in G[origin]: G[origin][dest] = {}
        G[origin][dest][num] = [cost, duration]
    return G

def dura(depart, arrive):
    if arrive.startswith('0'): arrive = arrive.replace('0', '', 1)
    if depart.startswith('0'): depart = depart.replace('0', '', 1)
    return sum(map(int, [arrive.replace(':', ''), '-'+depart.replace(':', '')])) 
    
def dijkstra(G, v):
    heap = [[0, v]]
    final = {}
    dist_so_far = {v: 0} 
    while len(final) < len(G):
        s = heapq.heappop(heap) # find shortest one
        w = s[-1]
        final[w] = s[0] #lock it down
        del dist_so_far[w]
        for child in G[w]:
            if child not in final:  # skip already locked down, only update dist_so_far for the distance is less than the one in dist_so_far, update the heap list
                distance = G[w][child] + final[w] 
                if child not in dist_so_far: 
                    dist_so_far[child] = distance
                    heapq.heappush(heap, [distance, child])
                elif distance < dist_so_far[child]:
                    dist_so_far[child] = distance
                    heapq.heappush(heap, [distance, child])
    return final   
                        

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

