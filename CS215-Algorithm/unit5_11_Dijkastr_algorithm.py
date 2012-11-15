
def dj(G,v):
    distance_so_far   = {}
    lockdown_distance = {}
    distance_so_far[v] = 0
    while len(lockdown_distance)< len(G):
        shortest_node_so_far = shortest_distance_node(distance_so_far)
        lockdown_distance[shortest_node_so_far] = distance_so_far[shortest_node_so_far]
        del distance_so_far[shortest_node_so_far]
        for child in G[shortest_node_so_far]: 
            if child not in lockdown_distance:
                if child not in distance_so_far:
                    distance_so_far[child] = lockdown_distance[shortest_node_so_far] + G[shortest_node_so_far][child]
                elif distance_so_far[child] > lockdown_distance[shortest_node_so_far] + G[shortest_node_so_far][child]
                    distance_so_far[child] = lockdown_distance[shortest_node_so_far] + G[shortest_node_so_far][child] 
    return lockdown_distance

def shortest_distance_node(dist):
    shortest_node = 'none'
    shortest_value = 10000000
    for v in dist:
        if dist[v]<shortest_value:
            (shortest_node,shortest_value) = (v,dist[v])
    return shortest_node
