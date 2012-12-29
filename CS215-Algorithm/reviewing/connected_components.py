
def makeG(G, node1, node2):
    if node1 not in G:
        G[node1] = {}
    G[node1][node2] = 1 
    if node2 not in G:
        G[node2] = {}
    G[node2][node1] = 1
    return G

#_clustering_coefficient_______
flights = [("ORD", "SEA"), ("ORD", "LAX"), ('ORD', 'DFW'), ('ORD', 'PIT'),
          ('SEA', 'LAX'), ('LAX', 'DFW'), ('ATL', 'PIT'), ('ATL', 'RDU'),
          ('RDU', 'PHL'), ('PIT', 'PHL'), ('PHL', 'PVD')]

G = {} 

for x, y in flights: makeG(G, x, y)

def clustering_coefficent(G,v):
    neighbors = G[v].keys()
    if len(neighbors) == 1: return -1.0
    links = 0 
    for l in neighbors:
        for m in neighbors:
            if m in G[l]: links += 0.5 
    return 2.0*links/len(neighbors)*(len(neighbors)-1)
    

#_connected_components-
connections = [('a', 'g'), ('a', 'd'), ('d', 'g'), ('g', 'c'), ('b', 'f'),
               ('f', 'e'), ('e', 'h')]
G1 = {}
for x, y in connections: makeG(G1, x, y)

def mark_component(G, node, marked):
    marked[node] = True
    total_marked = 1
    for neighbors in G[node]:
        if neighbors not in marked:
            total_marked += mark_component(G, neighbors, marked)
    return total_marked

def list_component_sizes(G):
    marked = {}
    for node in G.keys():
        if node not in marked:
            print node, ': ',  mark_component(G, node, marked)

list_component_sizes(G1)
print G
print G1

