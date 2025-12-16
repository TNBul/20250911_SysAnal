import numpy as np
from collections import defaultdict
from pprint import pprint

def dfs(graph, edge, visible=None, path=None):
    if visible is None: visible = []
    if path is None: path = [edge]
    
    visible.append(edge)
    
    paths = []
    for e in graph[edge]:
        if e not in visible:
            t_path = path + [e]
            paths.append(tuple(t_path))
            paths.extend(dfs(graph, e, visible[:], t_path))
    
    return paths

def main(s):
    pairs = [item.split(',') for item in s.split('\n')]
    
    adjacency_m = defaultdict(list)
    for (f, s) in pairs:
        adjacency_m[f].append(s)
        
    vertices = []     
    for item in pairs:
        if item[0] not in vertices:
            vertices.append(item[0])
        if item[1] not in vertices:
            vertices.append(item[1])
            
    index = {v: i for i, v in enumerate(vertices)}
    
    n = len(vertices)
    
    r1 = np.zeros((n,n), int)#,bool)     
    for key in adjacency_m:
        f_idx = index[key]
        for item in adjacency_m[key]:
            r1[f_idx][index[item]] = 1
    
    r2 = r1.T
    r3 = np.zeros((n,n), int)#,bool)

    A = np.dot(r1,r1)
    max_path_len = max(len(p) for p in dfs(adjacency_m, pairs[0][0]))

    for i in range(max_path_len - 2):
        r3[np.logical_or(r3,A)] = 1
        A = np.dot(A,r1)
    
    r4 = r3.T
    r5 = np.zeros((n,n), int)#,bool)
    
    for edge in adjacency_m:
        edges = adjacency_m[edge] 
        len_edges = len(edges)
        if len_edges > 1:
            for i in range(len_edges):
                f_idx = index[edges[i]]
                for s_edge in edges[i+1:]:
                    s_idx = index[s_edge]
                    r5[f_idx][s_idx] = 1           
        
    r5[np.logical_or(r5,r5.T)] = 1 

    return r1.tolist(), r2.tolist(), r3.tolist(), r4.tolist(), r5.tolist()

csv_string = "1,2\n1,3\n3,4\n3,5"
csv_string1 = "1,2\n1,3\n3,4\n3,5\n5,6\n6,7"
csv_string2 = "2,3\n2,1\n1,8\n1,5"
csv_string3 = "0,1\n0,2\n0,3\n0,4\n1,5\n1,6"

for i in main(csv_string): pprint(i), print("\n")
