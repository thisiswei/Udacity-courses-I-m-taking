

def dijkstra(G, v):
    distance = {}
    distance[v] = 0
    dist = {}
    while len(dist) < len(G):
        s = shortest(distance)
        del distance[element]
        for n in G[s]:
            if n not in dist:
                if n not in distance:
                    distance[n] = dist[n] + G[s][n]
                elif dist[s] + G[s][n] < distance[n]:
                    distance[n] = dist[n] + G[s][n]
    return dist
