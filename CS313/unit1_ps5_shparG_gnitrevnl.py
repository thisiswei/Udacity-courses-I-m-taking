# Write a function inverse_graph which takes as its input the
# adjacency matrix of a graph and returns the adjacency matrix
# of the inverse graph.

def inverse_graph(graph):
    g = graph
    l = len(g)
    ng=[]
    for i in range(l):
        ng.append([])
        for j in range(l):
            if j == i:
                ng[i].append(0)
            else:
                ng[i].append(abs(g[i][j]-1))

    return ng
    



def test():
    g1 = [[0, 1, 1, 0],
          [1, 0, 0, 1],
          [1, 0, 0, 1],
          [0, 1, 1, 0]]
    assert inverse_graph(g1) == [[0, 0, 0, 1],
                                 [0, 0, 1, 0],
                                 [0, 1, 0, 0],
                                 [1, 0, 0, 0]]
    g2 = [[0, 1, 1, 1],
          [1, 0, 1, 1],
          [1, 1, 0, 1],
          [1, 1, 1, 0]]
    assert inverse_graph(g2) == [[0, 0, 0, 0],
                                 [0, 0, 0, 0],
                                 [0, 0, 0, 0],
                                 [0, 0, 0, 0]]
    print 'nailed'
# If you've not seen testing like this before, all you need to do is
# to call test(). If the tests pass, you'll get no output. If they don't
# you'll get an assertion error. Don't forget to remove the call to the
# test before submitting your code.

test()
