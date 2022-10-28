import sys
import copy
import random
import networkx as nx


def choose_random_key(G):
    v1 = random.choice(list(G.keys()))
    v2 = random.choice(list(G[v1]))
    return v1, v2

def karger(graph):
    G=copy.deepcopy(graph)
    keys=list(graph.keys())
    V={}
    for key in keys:
        V[key]=[]
        V[key].append(key)
    length = []
    while len(G) > 2:
        v1, v2 = choose_random_key(G)
        G[v1].extend(G[v2]) # merge v1 and v2
        # Adjustment of side connections according to merging
        for x in G[v2]:
            G[x].remove(v2)
            G[x].append(v1)
        while v1 in G[v1]:# remove the rings
            G[v1].remove(v1)
        del G[v2]
        V[v1].extend(V[v2])
        del V[v2]
    for key in G.keys(): # Get the number of minimum cut edges
        length.append(len(G[key]))
    return length[0],V

graph={1:[2,3],
      2:[1,3],
      3:[1,2],
}


def main(adjacency_list):

    currentLen=0
    currentV={}
    shortestLen=sys.maxsize
    shortestV={}
    for i in range(10):
       currentLen,currentV = karger(adjacency_list)
       if currentLen<shortestLen:
            shortestLen=currentLen
            shortestV=copy.deepcopy(currentV)

    cut_edge=[]
    keys=list(shortestV.keys())
    for i in shortestV[keys[0]]:
        for j in shortestV[keys[1]]:
            if j in adjacency_list[i]:
                cut_edge.append([i,j])
    print("the shortest length of cut is {}".format(shortestLen))
    print("the cut edge is {}".format(cut_edge))
    return cut_edge

main(graph)