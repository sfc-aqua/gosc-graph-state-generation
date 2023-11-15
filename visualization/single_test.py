import time
import networkx as nx
import numpy as np

# Redefine necessary functions from previous code snippets


def total_edge_weight_with_dict(g, layout_dict):
    total_weight = 0
    for edge in g.edges(data=False):
        weight = abs(layout_dict[edge[0]] - layout_dict[edge[1]]) - 1
        total_weight += weight
    return total_weight


def timesteps_for_linear_ancilla_bus(g: nx.Graph, layout: list) -> int:
    layout_dict = {node: idx for idx, node in enumerate(layout)}
    timesteps_list = []
    for u in layout:
        u_index = layout_dict[u]
        touching_edges = [
            edge
            for edge in g.edges
            if (
                (layout_dict[edge[0]] < u_index and layout_dict[edge[1]] > u_index)
                or (layout_dict[edge[0]] > u_index and layout_dict[edge[1]] < u_index)
            )
        ]
        touching_nodes = set(node for edge in touching_edges for node in edge if node != u)
        neighbors = set(g.neighbors(u))
        combined_nodes = touching_nodes.union(neighbors)
        timesteps_u = len(combined_nodes) + 1
        timesteps_list.append(timesteps_u)
    return max(timesteps_list)


def generate_reverse(n):
    return list(range(n - 1, 0, -1))


def gen_erdos_renyi_graph_single_component(n, m, seed=None):
    if seed is not None:
        np.random.seed(seed)
    while True:
        G = nx.gnm_random_graph(n, m)
        if nx.is_connected(G):
            return G


# Corrected function to maintain the layout dictionary throughout the optimization process
def NGAopt_layout_corrected(g: nx.Graph, levels: list) -> list:
    nodes = list(g.nodes())
    n = len(nodes)
    layout_dict = {node: idx for idx, node in enumerate(nodes)}
    best_layout = nodes[:]
    best_weight = total_edge_weight_with_dict(g, layout_dict)

    for level in levels:
        while True:
            weight_change = False
            for i in range(level, n):
                if i + 1 < n:
                    if level == 1:
                        # Swap nodes for level 1
                        nodes[i - 1], nodes[i] = nodes[i], nodes[i - 1]
                        # Update layout dict for swapped nodes
                        layout_dict[nodes[i - 1]], layout_dict[nodes[i]] = i - 1, i
                    else:
                        # Rotate nodes for level > 1
                        temp = nodes[i - level]
                        nodes[i - level : i + 1] = nodes[i - (level - 1) : i + 1] + [temp]
                        # Update layout dict for rotated nodes
                        for j in range(i - level, i + 1):
                            layout_dict[nodes[j]] = j

                    # Calculate new weight with updated layout_dict
                    new_weight = total_edge_weight_with_dict(g, layout_dict)
                    if new_weight < best_weight:
                        best_weight = new_weight
                        best_layout = nodes[:]
                        weight_change = True
                    else:
                        # Revert changes if no improvement
                        if level == 1:
                            nodes[i], nodes[i - 1] = nodes[i - 1], nodes[i]
                            layout_dict[nodes[i]], layout_dict[nodes[i - 1]] = i, i - 1
                        else:
                            nodes[i - level : i + 1] = [temp] + nodes[i - level : i]
                            for j in range(i - level, i + 1):
                                layout_dict[nodes[j]] = j
            if not weight_change:
                break
    return best_layout


# Updated run_experiment function with the corrected NGAopt_layout function
def run_experiment_with_timing_corrected():
    strategy_name = "reverse"
    averages = {strategy_name: []}
    std_devs = {strategy_name: []}

    # Number of vertices is fixed at 50
    num_vertices = 500

    # Timing starts here
    start_time = time.time()

    # Iterate over a range of number of edges
    for num_edges in range(2000, 3000, 2000):  # Adjusted for testing
        # Temporary storage for multiple instances
        temp_results = {strategy_name: []}

        # Generate a graph with the given number of edges
        g = gen_erdos_renyi_graph_single_component(num_vertices, num_edges)
        # original_layout = list(range(num_vertices))

        # Compute the timesteps for the "reverse" strategy
        levels = generate_reverse(num_vertices)
        optimized_layout = NGAopt_layout_corrected(g, levels)
        timesteps = timesteps_for_linear_ancilla_bus(g, optimized_layout)
        temp_results[strategy_name].append(timesteps)

        # Store average and standard deviation for the "reverse" strategy
        averages[strategy_name].append(np.mean(temp_results[strategy_name]))
        std_devs[strategy_name].append(np.std(temp_results[strategy_name]))

    # Timing ends here
    end_time = time.time()
    elapsed_time = end_time - start_time

    return averages, std_devs, elapsed_time


# Running the corrected experiment function with timing
(
    averages_corrected,
    std_devs_corrected,
    elapsed_time_corrected,
) = run_experiment_with_timing_corrected()
print(averages_corrected, std_devs_corrected, elapsed_time_corrected)
