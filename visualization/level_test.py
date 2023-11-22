from typing import List, Set
import networkx as nx
import matplotlib.pyplot as plt
import random
import numpy as np


# networkx version
def gen_erdos_renyi_graph_single_component(n, m, seed=51):
    """
    Generate a random graph with a single connected component.
    """
    try:
        for i in range(5000):
            G = nx.gnm_random_graph(n, m, seed)
            if nx.number_connected_components(G) == 1:
                return G.edges
    except Exception as e:
        print(f"Failed to generate a connected graph: {e}")
    return None


# edge_weight calculation
def total_edge_weight(g, layout):
    total_weight = 0
    for edge in g.edges(data=False):
        # Weight of an edge is the number of nodes it travels over
        weight = abs(layout.index(edge[0]) - layout.index(edge[1])) - 1
        total_weight += weight
    return total_weight


# timestep calculation
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

    return max(timesteps_list)


def generate_updown(n):
    """Generate the updown strategy for a given n."""
    return list(range(1, n)) + list(range(n - 2, 0, -1))


def generate_reverse(n):
    """Generate the reverse strategy for a given n."""
    return list(range(n - 1, 0, -1))


# Naive General Algorithm with level list
def NGAopt_layout(g: nx.Graph, levels: List[int]) -> List[int]:
    nodes = list(g.nodes())
    n = len(nodes)
    best_layout = nodes[:]
    best_weight = total_edge_weight(g, best_layout)

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
                        weight_change = True
            if not weight_change:
                break
    return best_layout


"""
edges = [
    (0, 7), (1, 6), (2, 0), (2, 3), (2, 7), (3, 5), (4, 8), (4, 3),
    (7, 6), (8, 3), (8, 7), (9, 3), (9, 6), (9, 4), (9, 0)
]
g = nx.Graph()
g.add_edges_from(edges)

num_vertices = g.number_of_nodes()
levels = generate_reverse(num_vertices)
optimized_layout = NGAopt_layout(g, levels)

# Calculate timesteps
timesteps = timesteps_for_linear_ancilla_bus(g, optimized_layout)
print(optimized_layout, timesteps)
"""
strategies = ["original", "updown", "reverse"]

results = {strategy: {"num_edges": [], "timesteps": []} for strategy in strategies}

num_vertices = 50

# Iterate over increasing number of edges
for num_edges in range(150, 200, 5):

    # Iterate for _ instances
    for _ in range(4):
        # Generate a graph with the given number of edges
        edges = gen_erdos_renyi_graph_single_component(num_vertices, num_edges, seed=51 + _)
        g = nx.MultiDiGraph()
        g.add_edges_from(edges)
        original_layout = list(range(num_vertices))

        # Compute the timesteps for the original layout
        original_timesteps = timesteps_for_linear_ancilla_bus(g, original_layout)
        results["original"]["num_edges"].append(num_edges)
        results["original"]["timesteps"].append(original_timesteps)

        # Compute the timesteps for each strategy
        for strategy_name in ["updown", "reverse"]:
            levels = globals()[f"generate_{strategy_name}"](num_vertices)
            optimized_layout = NGAopt_layout(g, levels)
            timesteps = timesteps_for_linear_ancilla_bus(g, optimized_layout)
            results[strategy_name]["num_edges"].append(num_edges)
            results[strategy_name]["timesteps"].append(timesteps)

# Plot the results
plt.figure(figsize=(10, 6))
for strategy_name in strategies:
    plt.scatter(
        results[strategy_name]["num_edges"], results[strategy_name]["timesteps"], label=strategy_name
    )


plt.xlabel("Number of Edges")
plt.ylabel("Time Steps")
plt.title("Optimization Effect of Different Level List Strategies")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
