from typing import List, Set
import networkx as nx

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