import networkx as nx

G=nx.Graph()
G.add_nodes_from([1,2,3,4,5,6,7])
G.add_edge(1,3, weight=1)
G.add_edge(2,3, weight=1)
G.add_edge(3,4, weight=1)
G.add_edge(4,5, weight=1)
G.add_edge(2,5, weight=1)
G.add_edge(5,6, weight=1)
G.add_edge(5,7, weight=1)
G.add_edge(6,7, weight=1)
print G.node
print G.edge
path_iter = nx.all_simple_paths(G, 1, 6)
pathes = []
for p in path_iter:
    pathes.append(p)
print pathes

def get_path_length(graph, p):
    length = 0.0
    for i in range(len(p) - 1):
        length += graph[p[i]][p[i + 1]]['weight']
    return length

for p in pathes: print get_path_length(G, p), '\t', p
