
def centrality_max(G, v):
    openlist = [v]
    distance = {}
    distance[v] = 0
    while len(openlist) > 0:
        ele = openlist.pop(0)
        for neighbor in G[ele].keys():
            if neighbor not in distance:
                distance[neighbor] = distance[ele] + 1
                openlist.append(neighbor)
    return max(distance.values())  


#def path1(G, v1, v2):
#    openlist, total_path = [v1], 0
#    while len(openlist) > 0:
#        node = openlist.pop(0)
#        for neighbor in G[node].keys():
#            if neighbor == v2:
#                return total_path
#            else:
#                total_path += 1
#                openlist.append(neighbor)
#    return False

# return distance from node v1, v2 in Graph G
def path(G, v1, v2):
    distance = {}
    openlist = [v1]
    distance[v1] = 0
    while len(openlist) > 0:
        node = openlist.pop(0)
        for neighbor in G[node].keys():
            if neighbor not in distance:
                distance[neighbor] = distance[node] + 1
                if neighbor == v2: return distance[neighbor]
                openlist.append(neighbor)
    return False


#def mark_component1(G, node, marked):
#    marked[node] = True
#    total_marked = 1
#    for neighbor in G[node]:                
#        if neighbor not in marked:
#            total_marked += mark_component(G, neighbor, marked)
#    return total_marked

# return all the node connected to node in G

def mark_component(G, node, marked):
    openlist = [node]
    if not marked: marked = {}
    while len(openlist) > 0:
        element = openlist.pop(0)
        for neighbor in G[element].keys():
            if element not in marked:
                marked[element] = True
        openlist.append(neighbor)
    return marked



def test():
    test_edges = [(1, 2), (2, 3), (4, 5), (5, 6)]
    G = {}
    for n1, n2 in test_edges:
        make_link(G, n1, n2)
    marked = {}
    assert mark_component(G, 1, marked) == 3
    assert 1 in marked
    assert 2 in marked
    assert 3 in marked
    assert 4 not in marked
    assert 5 not in marked
    assert 6 not in marked




