from collections import defaultdict
from heapq import *
from constant import M1

def dijkstra_raw(edges, from_node, to_node):
    g = defaultdict(list)
    for l, r, c in edges:
        g[l].append((c, r))
    q, seen = [(0, from_node, ())], set()
    while q:
        (cost, v1, path) = heappop(q)
        if v1 not in seen:
            seen.add(v1)
            path = (v1, path)
            if v1 == to_node:
                return cost, path
            for c, v2 in g.get(v1, ()):
                if v2 not in seen:
                    heappush(q, (cost + c, v2, path))
    return float("inf"), []

def spf_route(adj_graph, from_node, to_node):
    edges = []    
    for i in range(len(adj_graph)):
        for j in range(len(adj_graph[0])):
            if i != j and adj_graph[i][j] != M1:
                edges.append((i, j, adj_graph[i][j]))
    ret_path = []
    length, path_queue = dijkstra_raw(edges, from_node, to_node)
    if len(path_queue) > 0:
        # 1. Get the length firstly;
        # # 2. Decompose the path_queue, to get the passing nodes in the shortest path.
        left = path_queue[0]
        ret_path.append(left)  # # 2.1 Record the destination node firstly;
        right = path_queue[1]
        while len(right) > 0:
            left = right[0]
            ret_path.append(left)  # # 2.2 Record other nodes, till the source-node.
            right = right[1]
        ret_path.reverse()  # # 3. Reverse the list finally, to make it be normal sequence.
    return ret_path

def rtl_route(adj_graph, rtl_graph, from_node, to_node):
    edges = []    
    for i in range(len(adj_graph)):
        for j in range(len(adj_graph[0])):
            if i != j and adj_graph[i][j] != M1:
                edges.append((i, j, adj_graph[i][j]))
    ret_path = []
    length, path_queue = dijkstra_raw(edges, from_node, to_node)
    
    path_mrtl = {}
    
    for path in path_queue:
        max_rtl = 0
        for i in range(len(path) - 1):
            seq1 = path[i]
            seq2 = path[i+1]
            rtl = rtl_graph[seq1][seq2]
            if rtl > max_rtl:
                max_rtl = rtl
            
        path_mrtl[path] = max_rtl
        
    path_list = path_mrtl.keys()
    min_mrtl_path = None
    min_mrtl = 1000000000000000
    for path in path_list:
        mrtl = path_mrtl[path]
        if mrtl < min_mrtl:
            min_mrtl = mrtl
            min_mrtl_path = path
    
    assert min_mrtl_path != None
    
    return min_mrtl_path 
        
        
            
    

