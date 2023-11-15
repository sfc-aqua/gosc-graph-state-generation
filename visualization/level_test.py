from typing import List, Set
import networkx as nx
import matplotlib.pyplot as plt
import random
import numpy as np


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


# Define the 2 level list strategies
strategies = {"updown": [], "reverse": []}


# Reset the results dictionary
results = {"original": [], "updown": [], "reverse": []}
averages = {"original": [], "updown": [], "reverse": []}
std_devs = {"original": [], "updown": [], "reverse": []}


# Number of vertices is fixed at 10
num_vertices = 50

# Iterate over increasing number of edges
for num_edges in range(150, 200, 5):
    # Temporary storage for multiple instances
    temp_results = {"original": [], "updown": [], "reverse": []}

    # Iterate for 10 instances
    for _ in range(4):
        # Generate a graph with the given number of edges
        edges = gen_erdos_renyi_graph_single_component(num_vertices, num_edges, seed=51 + _)
        g = nx.MultiDiGraph()
        g.add_edges_from(edges)
        original_layout = list(range(num_vertices))

        # Compute the timesteps for the original layout
        original_timesteps = timesteps_for_linear_ancilla_bus(g, original_layout)
        temp_results["original"].append(original_timesteps)

        # Compute the timesteps for each strategy
        for strategy_name in ["updown", "reverse"]:
            levels = globals()[f"generate_{strategy_name}"](num_vertices)
            optimized_layout = NGAopt_layout(g, levels)
            timesteps = timesteps_for_linear_ancilla_bus(g, optimized_layout)
            temp_results[strategy_name].append(timesteps)
    # Store average and standard deviation for each strategy
    for strategy_name in ["original", "updown", "reverse"]:
        averages[strategy_name].append(np.mean(temp_results[strategy_name]))
        std_devs[strategy_name].append(np.std(temp_results[strategy_name]))
"""
# Iterate over increasing number of edges
for num_edges in range(200, 300):
    # Generate a graph with the given number of edges
    edges = gen_erdos_renyi_graph_single_component(num_vertices, num_edges)
    g = nx.MultiDiGraph()
    g.add_edges_from(edges)
    original_layout = list(range(num_vertices))

    # Compute the timesteps for the original layout
    original_timesteps = timesteps_for_linear_ancilla_bus(g, original_layout)
    results["original"].append(original_timesteps)

    # Compute the timesteps for each strategy
    for strategy_name in ["updown", "reverse"]:
        levels = globals()[f"generate_{strategy_name}"](num_vertices)
        optimized_layout = NGAopt_layout(g, levels)
        timesteps = timesteps_for_linear_ancilla_bus(g, optimized_layout)
        results[strategy_name].append(timesteps)
"""
# Plot the results
plt.figure(figsize=(10, 6))
x = list(range(150, 200, 5))  # Number of edges
for strategy_name in ["original", "updown", "reverse"]:
    plt.errorbar(
        x,
        averages[strategy_name],
        yerr=std_devs[strategy_name],
        label=strategy_name,
        marker="o",
        capsize=5,
    )
plt.xlabel("Number of Edges")
plt.ylabel("Time Steps")
plt.title("Optimization Effect of Different Level List Strategies")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
"""
# Iterate over increasing number of edges
for num_edges in range(500, 700):
    # Generate a graph with the given number of edges
    edges = gen_erdos_renyi_graph_single_component(num_vertices, num_edges)
    g = nx.MultiDiGraph()
    g.add_edges_from(edges)
    original_layout = list(range(num_vertices))

    # Compute the timesteps for the original layout
    original_timesteps = timesteps_for_linear_ancilla_bus(g, original_layout)
    results["original"].append(original_timesteps)

    # Compute the timesteps for each strategy
    for strategy_name in ["updown", "reverse"]:
        levels = globals()[f"generate_{strategy_name}"](num_vertices)
        optimized_layout = NGAopt_layout(g, levels)
        timesteps = timesteps_for_linear_ancilla_bus(g, optimized_layout)
        results[strategy_name].append(timesteps)

# Plot the results
plt.figure(figsize=(10, 6))
x = list(range(500, 700))  # Number of edges
for strategy_name, timesteps in results.items():
    plt.plot(x, timesteps, label=strategy_name, marker="o")

plt.xlabel("Number of Edges")
plt.ylabel("Time Steps")
plt.title("Optimization Effect of Different Level List Strategies")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
"""
