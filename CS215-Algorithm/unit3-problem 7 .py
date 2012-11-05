def centrality_max(G, v):
    distance_from_start = {}
    linked = [v]
    distance_from_start[v] = 0
    while len(linked)>0:
        current = linked.pop(0)
        for neighbor in G[current].keys():
            if neighbor not in distance_from_start:
                distance_from_start[neighbor] = distance_from_start[current]+1
                linked.append(neighbor)
    return max(list(distance_from_start.values()))
