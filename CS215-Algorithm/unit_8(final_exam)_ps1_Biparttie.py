#
# Write a function, `bipartite` that
# takes as input a graph, `G` and tries
# to divide G into two sets where 
# there are no edges between elements of the
# the same set - only between elements in
# different sets.
# If two sets exists, return one of them
# or `None` otherwise
# Assume G is connected
#

def bipartite(G):
    keys                 = G.keys()
    first_node           = keys[0]
    set_one              = [first_node]
    set_two              = []
    checking             = [first_node]
    checked              = []
    while len(checked) < len(G):
        node       = checking.pop(0)
        neighbors  = G[node].keys()
        checked.append( node )
        for neighbor in neighbors:
            if (neighbor in set_one and node in set_one) or ( neighbor in set_two and node in set_two): return None
            if node in set_one:set_two.append(neighbor)
            if node in set_two:set_one.append(neighbor)
            if neighbor not in checking: checking.append(neighbor) 
    return set(set_one)
        
        


########
#
# Test

def make_link(G, node1, node2, weight=1):
    if node1 not in G:
        G[node1] = {}
    (G[node1])[node2] = weight
    if node2 not in G:
        G[node2] = {}
    (G[node2])[node1] = weight
    return G


def test():
    edges = [(1, 2), (2, 3), (1, 4), (2, 5),
             (3, 8), (5, 6)]
    G = {}
    for n1, n2 in edges:
        make_link(G, n1, n2)
    g1 = bipartite(G)
    assert (g1 == set([1, 3, 5]) or
            g1 == set([2, 4, 6, 8]))
    edges = [(1, 2), (1, 3), (2, 3)]
    G = {}
    for n1, n2 in edges:
        make_link(G, n1, n2)
    g1 = bipartite(G)
    assert g1 == None

