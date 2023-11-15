import networkx as nx
from typing import List, Set


def timesteps_for_linear_ancilla_bus(g: nx.Graph, layout: List[int], initialized_nodes=None) -> int:
    timesteps_list = []
    for u in layout:
        # Count number of node endpoints of all edges touching vertical line through u
        u_index = layout.index(u)
        touching_edges = [
            edge
            for edge in g.edges
            if (
                (layout.index(edge[0]) < u_index and layout.index(edge[1]) > u_index)
                or (layout.index(edge[0]) > u_index and layout.index(edge[1]) < u_index)
            )
        ]

        touching_nodes = set(node for edge in touching_edges for node in edge if node != u)
        # Neighbors of node u
        neighbors = set(g.neighbors(u))
        # Combine touching nodes and neighbors
        combined_nodes = touching_nodes.union(neighbors)
        # Add one for parity check on u
        timesteps_u = len(combined_nodes) + 1
        timesteps_list.append(timesteps_u)
        print(timesteps_list)

    return max(timesteps_list)


def generate_updown(n):
    """Generate the updown strategy for a given n."""
    return list(range(1, n)) + list(range(n - 2, 0, -1))


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
layout = [12, 0, 7, 6, 3, 1, 9, 2, 14, 10, 8, 4, 5, 11, 13]
g = nx.Graph()
g.add_edges_from(edges)

timesteps = timesteps_for_linear_ancilla_bus(g, layout)
print(timesteps)
print(generate_updown(10))
