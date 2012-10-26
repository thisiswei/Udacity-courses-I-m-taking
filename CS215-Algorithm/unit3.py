def make_link(G, node1, node2):
    if node1 not in G:
        G[node1] = {}
    (G[node1])[node2] = 1
    if node2 not in G:
        G[node2] = {}
    (G[node2])[node1] = 1
    return G


flights = [("ORD", "SEA"), ("ORD", "LAX"), ('ORD', 'DFW'), ('ORD', 'PIT'),
          ('SEA', 'LAX'), ('LAX', 'DFW'), ('ATL', 'PIT'), ('ATL', 'RDU'),
          ('RDU', 'PHL'), ('PIT', 'PHL'), ('PHL', 'PVD')]

G={}

### make graph betweetn these flight citys => 'ord':{'sea':1}
for x,y in flights:
    make_link(G,x,y)
# write a procedure to caculate a graph's clustering_coefficient
# clustering_coefficient:  2* number of links between neighbors of the node / itsdegree * (itsdegree - 1)
# so we will add all individul node's coefficent then divide by the total node

# 
def clustering_coefficient(G,v):
    neighbors = G[v].keys()
    if len(neighbors) == 1 : return 0
    links = 0

    for neighbor in neighbors:
        for nei in neighbors:
            if nei in G[neighbor]: links+=0.5
    return 2*links/len(neighbors)*(len(neighbors)-1)

def average_cc(G):
    total = 0
    for v in G.keys():
        total += clustering_coefficient(G,v)
    return total/len(G)
