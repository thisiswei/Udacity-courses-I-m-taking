import csv

def make_link(G, node1, node2):
    if node1 not in G:
        G[node1] = {}
    if node2 not in G[node1]:
        (G[node1])[node2] = 1
    else:
        (G[node1])[node2] += 1
    if node2 not in G:
        G[node2] = {}
    if node1 not in G[node2]:
        (G[node2])[node1] = 1
    else:
        (G[node2])[node1] += 1
    return G

def read_graph(filename):
    # Read an undirected graph in CSV format. Each line is an edge
    tsv = csv.reader(open(filename), delimiter='\t')
    G = {}
    chars = {}
    for (node1, node2) in tsv: 
        if node1 not in chars:
            chars[node1] = 1
        make_link(G, node1, node2)
    return G,chars

marvelG,chars = read_graph('marvel')

G = {}
for char1 in chars:
    for book in marvelG[char1]:
        for char2 in marvelG[book]:
            if char1 != char2:
                make_link(G,char1,char2)

maxVal = 0
maxChars = ''
for char1 in G:
    for char2 in G[char1]:
        if char1 > char2:
            val = G[char1][char2]
            if maxVal < val:
                maxVal = val
                maxChars = char1+' - '+char2

print maxChars,maxVal
