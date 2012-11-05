def make_link(G, node1, node2):
    if node1 not in G:
        G[node1] = {}
    (G[node1])[node2] = 1
    if node2 not in G:
        G[node2] = {}
    (G[node2])[node1] = 1
    return G


//give a graph G,note V1,V2, find the shortest path


def path(G,v1,v2):
    distance_from_start = {}
    distance_from_start[v1]=0
    linked=[v1]
    while len(linked)>0:
        current=linked[0]
        del linked[0]
        for neighbor in G[connected].keys():
            if neighbor not in distance_from_start:
                distance_from_start[neighbor]=distance_from_start[current]+1
                if neighbor == v2 : return distance_from_start[neighbor]
                linked.append(neighbor)
    return False



