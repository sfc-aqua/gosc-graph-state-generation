from typing import List, Set
import networkx as nx
import matplotlib.pyplot as plt


def total_edge_weight(g, layout):
    total_weight = 0
    for edge in g.edges(data=False):
        # Weight of an edge is the number of nodes it travels over
        weight = abs(layout.index(edge[0]) - layout.index(edge[1])) - 1
        total_weight += weight
    return total_weight


def NGAopt_layout(g: nx.Graph) -> List[int]:
    nodes = list(g.nodes())
    n = len(nodes)
    best_layout = nodes[:]
    best_weight = total_edge_weight(g, best_layout)
    levels = [14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]

    for level in levels:
        while True:
            weight_change = False
            for i in range(level, n):
                if i + 1 <= n:
                    if level == 1:
                        nodes[i - 1], nodes[i] = nodes[i], nodes[i - 1]
                    elif level >= 2:
                        temp = nodes[i]
                        nodes[i - (level - 1) : i + 1] = nodes[i - level : i]
                        nodes[i - level] = temp

                    new_weight = total_edge_weight(g, nodes)
                    if new_weight >= best_weight:
                        if level == 1:
                            nodes[i], nodes[i - 1] = nodes[i - 1], nodes[i]
                        elif level >= 2:
                            temp = nodes[i - level]
                            nodes[i - level : i] = nodes[i - (level - 1) : i + 1]
                            nodes[i] = temp
                    else:
                        best_weight = new_weight
                        best_layout = nodes[:]
                        print(best_layout)
                        weight_change = True
            if not weight_change:
                break
    return best_layout


def draw_layout(g, layout):
    pos = {node: (index, 0) for index, node in enumerate(layout)}

    plt.figure(figsize=(10, 6))
    nx.draw(
        g,
        pos,
        with_labels=True,
        node_size=1000,
        node_color="skyblue",
        connectionstyle="arc3,rad=0.3",
        arrowstyle="-",
        edge_color="gray",
        width=2,
        font_size=15,
    )
    plt.show()


nodes_layout = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
edges = [
    (14, 4),
    (3, 1),
    (3, 7),
    (3, 10),
    (9, 2),
    (9, 14),
    (13, 11),
    (4, 5),
    (4, 8),
    (9, 1),
    (9, 10),
    (0, 7),
    (10, 5),
    (10, 14),
    (6, 7),
    (14, 2),
    (9, 6),
    (0, 12),
    (8, 10),
    (6, 0),
]
g = nx.MultiDiGraph()
g.add_nodes_from(nodes_layout)
g.add_edges_from(edges)

NGAopt_layout(g)
print(NGAopt_layout(g))
print(total_edge_weight(g, nodes_layout))
print(total_edge_weight(g, NGAopt_layout(g)))
draw_layout(g, NGAopt_layout(g))
