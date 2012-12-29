from collections import defaultdict
    
def make_link(G, node1, node2):
    (G[node1])[node2] = 1
    (G[node2])[node1] = 1
    return G


def read_graph(filename):
    tsv = csv.reader(open(filename), delimiter = '\t')
    G = defaultdict(dict)
    for node1, node2 in tsv: make_link(G, node1, node2)
    return G

marvelG = read_graph('file.tsv')







