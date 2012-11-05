# continue the concert in unit 3 ,and caculate the average of the distance from note V to everyother nodes in Graph G



def centrality(G,v):
    distance_from_start={}
    linked = [v]
    distance_from_start[v]=0
    while len(linked)>0:
        current = linked[0]
        del linked[0]
        for neighbor in G[v].keys():
            if neighbor not in distance_from_start:
                distance_from_start[neighbor] = distance_from_start[current]+1
                linked.append(neighbor)
    return sum(distance_from_start.values()+0.0)/len(distance_from_start)

