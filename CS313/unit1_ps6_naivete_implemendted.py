# Write two functions, the first, validity_check which takes a potential
# cover and the adjacency matrix of a graph as its inputs and returns True
# if the potential cover is a cover of the graph and False otherwise.
# The second, vertex_cover_naive, takes the adjacency matrix of a graph
# as its input, checks all potential covers, and returns the size of a
# minimum vertex cover. You should assume there are no loops in the graph.

from itertools import *

def validity_check(cover, graph):
    # Your code should go here.
    L = len(graph)
    for i in range(L):
        for j in range(L):
            if graph[i][j]==1 and cover[i]!=1 and cover[j]!=1:
                return False
    return True


def vertex_cover_naive(input_graph):
    n = len(input_graph)
    minimum_vertex_cover = n
    # loops through all strings of 0s and 1s of length n
    for assignment in product([0,1], repeat=n):
        
        if validity_check(assignment,input_graph):
            size = sum(assignment)
            if size < minimum_vertex_cover:
                minimum_vertex_cover = size
    return minimum_vertex_cover
            
            
        # Your code should go here.
        # Based on the assignment (a list of 0s and 1s)
        # - Check the assignment is valid
        # - Calculate the size of assignment
        # - Update the minimum_vertex_cover variable if appropriate


    # End of your code
    return minimum_vertex_cover

def test():
    graph = [[0, 1, 1, 1, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 1, 1],
        [1, 0, 1, 0, 1],
        [1, 1, 1, 1, 0]]

    assert vertex_cover_naive(graph)==3 
    print 'nailed'

# If you've not seen testing like this before, all you need to do is
# to call test(). If the tests pass, you'll get no output. If they don't
# you'll get an assertion error. Don't forget to remove the call to the
# test before submitting your code.

test()
