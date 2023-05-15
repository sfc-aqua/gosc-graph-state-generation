from typing import List, Set

import networkx as nx
import numpy as np
import sys
import copy
import random
import networkx as nx


def random_mapper(g: nx.Graph, _: Set[int]) -> List[int]:
    """This mapper randomly permutes the label and ignore the skipped_stabilizer set."""
    return list(np.random.permutation(g.number_of_nodes()))


# def min_cut_mapper(g: nx.Graph, skipped_stabilizer: Set[int]) -> List[int]:
# return [x for x in range(g.number_of_nodes())]


def choose_random_key(G):
    v1 = random.choice(list(G.keys()))
    v2 = random.choice(list(G[v1]))
    return v1, v2


def karger(graph):
    G = copy.deepcopy(graph)
    keys = list(graph.keys())
    V = {}
    for key in keys:
        V[key] = []
        V[key].append(key)
    length = []
    while len(G) > 2:
        v1, v2 = choose_random_key(G)
        G[v1].extend(G[v2])  # merge v1 and v2
        # Adjustment of side connections according to merging
        for x in G[v2]:
            G[x].remove(v2)
            G[x].append(v1)
        while v1 in G[v1]:  # remove the rings
            G[v1].remove(v1)
        del G[v2]
        V[v1].extend(V[v2])
        del V[v2]
    for key in G.keys():  # Get the number of minimum cut edges
        length.append(len(G[key]))
    return length[0], V


def min_cut(G, component):
    subgraph = nx.subgraph(G, component)
    adjacency_list = nx.to_dict_of_lists(subgraph)
    currentLen = 0
    currentV = {}
    shortestLen = sys.maxsize
    shortestV = {}
    for i in range(10):
        currentLen, currentV = karger(adjacency_list)
        if currentLen < shortestLen:
            shortestLen = currentLen
            shortestV = copy.deepcopy(currentV)
    cut_edge = []
    keys = list(shortestV.keys())
    for i in shortestV[keys[0]]:
        for j in shortestV[keys[1]]:
            if j in adjacency_list[i]:
                cut_edge.append([i, j])
    # print("the shortest length of cut is {}".format(shortestLen))
    # print("the cut edge is {}".format(cut_edge))
    G.remove_edges_from(cut_edge)
    return G


def min_cut_mapper(g: nx.Graph, skipped_stabilizer: Set[int]) -> List[int]:
    mapping = []
    G = copy.deepcopy(g)

    def mapping_min(G):
        for component in nx.connected_component_subgraphs(G):
            if len(component.nodes) > 2:
                G = min_cut(G, component)
                return mapping_min(G)
            else:
                mapping.extend([i for i in list(component)])
                G.remove_nodes_from(component)
                return mapping_min(G)

    mapping_min(G)
    return mapping
