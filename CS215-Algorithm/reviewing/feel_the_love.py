#
# Take a weighted graph representing a social network where the weight
# between two nodes is the "love" between them.  In this "feel the
# love of a path" problem, we want to find the best path from node `i`
# and node `j` where the score for a path is the maximum love of an
# edge on this path. If there is no path from `i` to `j` return
# `None`.  The returned path doesn't need to be simple, ie it can
# contain cycles or repeated vertices.
#
# Devise and implement an algorithm for this problem.
#

def feel_the_love(G, i, j):
    # return a path (a list of nodes) between `i` and `j`,
    # with `i` as the first node and `j` as the last node,
    # or None if no path exists
    distNow = {i: 0}
    final = {i: [i]}
    heap = [[0, i]]
    while len(heap) > 0:
        _, node = heapq.heappop(heap)
        for child in G[node]:
            new_dist = G[node][child]
            if child not in distNow or new_dist > distNow[child]: 
                distNow[child] = new_dist
                final[child] = final[node] + [child]
                heapq.heappush(heap, [-1 * new_dist, child])
            elif distNow[node] > distNow[child]:
                distNow[child] = distNow[node]
                final[child] = final[node] + [child]
                heapq.heappush(heap, [-1 * distNow[child], child])
    return None if j not in final else final[j]


#########
#
# Test

import heapq

def score_of_path(G, path):
    max_love = -float('inf')
    for n1, n2 in zip(path[:-1], path[1:]):
        love = G[n1][n2]
        if love > max_love:
            max_love = love
    return max_love


def test():
    G = {'a':{'c':1},
         'b':{'c':1},
         'c':{'a':1, 'b':1, 'e':1, 'd':1},
         'e':{'c':1, 'd':2},
         'd':{'e':2, 'c':1},
         'f':{}}
    path = feel_the_love(G, 'a', 'b')
    assert score_of_path(G, path) == 2

    path = feel_the_love(G, 'a', 'f')
    assert path == None

    

