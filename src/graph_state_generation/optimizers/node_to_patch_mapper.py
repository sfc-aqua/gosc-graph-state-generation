from typing import List, Set

import networkx as nx
import numpy as np
import sys
import copy
import random
import matplotlib.pyplot as plt


def random_mapper(g: nx.Graph, _: Set[int]) -> List[int]:
    """This mapper randomly permutes the label and ignore the skipped_stabilizer set."""
    return list(np.random.permutation(g.number_of_nodes()))


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
    # currentLen = 0
    # current_edges = {}
    min_cut_len = sys.maxsize
    min_cut_edges = {}
    for i in range(10):  # Repeat the Karger's algorithm several times. 10 is just a trial number.
        currentLen, current_edges = karger(adjacency_list)
        if currentLen < min_cut_len:
            min_cut_len = currentLen
            # min_cut_edges = copy.deepcopy(current_edges)
            min_cut_edges = current_edges
    # Remove minimum cut edges from the original graph
    cut_edge = []
    nodes_in_cut = list(min_cut_edges.keys())
    for i in min_cut_edges[nodes_in_cut[0]]:
        for j in min_cut_edges[nodes_in_cut[1]]:
            if j in adjacency_list[i]:
                cut_edge.append([i, j])
    # print("the shortest length of cut is {}".format(min_cut_len))
    # print("the cut edge is {}".format(cut_edge))
    G.remove_edges_from(cut_edge)
    return G


def min_cut_mapper(g: nx.Graph, skipped_stabilizer: Set[int]) -> List[int]:
    mapping = []
    G = copy.deepcopy(g)

    def mapping_min(G):
        components = list(nx.connected_components(G))
        for component in components:
            component = G.subgraph(component)
            if len(component.nodes) > 2:
                G_copy = min_cut(G, set(component))
                return mapping_min(G_copy)
            else:
                mapping.extend([i for i in list(component)])
                G_copy = G.copy()
                G_copy.remove_nodes_from(component)
                return mapping_min(G_copy)
        return mapping

    return mapping_min(G)


def total_edge_weight(g, layout):
    total_weight = 0
    for edge in g.edges(data=False):
        # Weight of an edge is the number of nodes it travels over
        weight = abs(layout.index(edge[0]) - layout.index(edge[1])) - 1
        total_weight += weight
    return total_weight


def NGAopt_layout(g: nx.Graph, _: Set[int]) -> List[int]:
    nodes = list(g.nodes())
    n = len(nodes)
    best_layout = nodes[:]
    best_weight = total_edge_weight(g, best_layout)
      
    while True:
        weight_change = False
        for i in range(1, n):

            # (3) Swap current with the node to its left
            nodes[i], nodes[i - 1] = nodes[i - 1], nodes[i]

            # (2) Calculate the total edge weight
            new_weight = total_edge_weight(g, nodes)

            # (4) If the new total edge weight is higher or the same, undo the swap
            if new_weight >= best_weight:
                nodes[i], nodes[i - 1] = nodes[i - 1], nodes[i]
            else:
                best_weight = new_weight
                best_layout = nodes[:]
                weight_change = True
        if not weight_change:
            break
    return best_layout
