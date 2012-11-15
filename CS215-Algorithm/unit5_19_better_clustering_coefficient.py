import random
def make_link(G, node1, node2):
    if node1 not in G:
        G[node1] = {}
    (G[node1])[node2] = 1
    if node2 not in G:
        G[node2] = {}
    (G[node2])[node1] = 1
    return G

flights = [(1,2),(1,3),(2,3),(2,6),(2,4),(2,5),(3,6),(4,5)]
G = {}
for (x,y) in flights: make_link(G,x,y)

##  randomizing clustering coefficient == average_clustering_coefficent
def clustering_coefficient(G,v): 
    vindex = {}
    d = 0
    for w in G[v].keys:
        vindex[d]=w
        d+=1
    total = 0
    for i in range(1000):
        if d>1:
            pick = random.randint(0,d-1)
            v1 = vindex[pick]
            v2 = vindex[(pick + random.randint(1,d-1))%d]#make sure pick diffent node than v1
            if v2 in G[v1]: total+=1
    return (total+0.0)/i



