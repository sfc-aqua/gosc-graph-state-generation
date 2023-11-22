from graph_tool.all import *
import graph_tool.all as gt
import matplotlib.pyplot as plt
import numpy as np
import random


def gen_erdos_renyi_graph_single_component_gt(n, m, seed=51):
    """
    Generate a random Erdős-Rényi graph with a single connected component using graph-tool.
    """
    random.seed(seed)
    G = gt.Graph(directed=False)
    G.add_vertex(n)

    try:
        for _ in range(5000):
            gt.add_random_edges(G, m)
            _, component_labels = gt.label_components(G)
            if len(set(component_labels)) == 1:
                return G
    except Exception as e:
        print(f"Failed to generate a connected graph: {e}")
    return None


def total_edge_weight_with_dict_graph_tool(g, layout_dict):
    total_weight = 0
    for edge in g.edges():
        source = edge.source()
        target = edge.target()
        weight = abs(layout_dict[source] - layout_dict[target]) - 1
        total_weight += weight
    return total_weight


def timesteps_for_linear_ancilla_bus_graph_tool(g, layout):
    timesteps_list = []
    for u_index, u in enumerate(layout):
        touching_edges = [
            edge
            for edge in g.edges()
            if (layout[int(edge.source())] < u_index and layout[int(edge.target())] > u_index)
            or (layout[int(edge.source())] > u_index and layout[int(edge.target())] < u_index)
        ]

        touching_nodes = set()
        for edge in touching_edges:
            touching_nodes.add(int(edge.source()))
            touching_nodes.add(int(edge.target()))
        touching_nodes.discard(u)

        neighbors = set(g.get_all_neighbours(u))

        combined_nodes = touching_nodes.union(neighbors)

        timesteps_u = len(combined_nodes) + 1
        timesteps_list.append(timesteps_u)

    return max(timesteps_list)


def generate_updown(n):
    return list(range(1, n)) + list(range(n - 2, 0, -1))


def generate_reverse(n):
    return list(range(n - 1, 0, -1))


def NGAopt_layout_graph_tool(g, levels):
    nodes = list(range(g.num_vertices()))
    node_dict = {node: i for i, node in enumerate(nodes)}
    best_layout = nodes[:]
    best_weight = total_edge_weight_with_dict_graph_tool(g, node_dict)

    for level in levels:
        while True:
            weight_change = False
            for i in range(level, len(nodes)):
                if i + 1 <= len(nodes):
                    if level == 1:
                        nodes[i - 1], nodes[i] = nodes[i], nodes[i - 1]
                        node_dict[nodes[i]], node_dict[nodes[i - 1]] = i, i - 1

                    elif level >= 2:
                        temp = nodes[i]
                        for j in range(i - level, i + 1):
                            node_dict[nodes[j]] = j - 1
                        nodes[i - (level - 1) : i + 1] = nodes[i - level : i]
                        nodes[i - level] = temp
                        node_dict[temp] = i - level

                    new_weight = total_edge_weight_with_dict_graph_tool(g, node_dict)
                    if new_weight >= best_weight:
                        if level == 1:
                            nodes[i], nodes[i - 1] = nodes[i - 1], nodes[i]
                            node_dict[nodes[i]], node_dict[nodes[i - 1]] = i, i - 1

                        elif level >= 2:
                            temp = nodes[i - level]
                            for j in range(i - level, i):
                                node_dict[nodes[j]] = j + 1
                            nodes[i - level : i] = nodes[i - (level - 1) : i + 1]
                            nodes[i] = temp
                            node_dict[temp] = i

                    else:
                        best_weight = new_weight
                        best_layout = nodes[:]
                        weight_change = True
            if not weight_change:
                break
    return best_layout


strategies = {"updown": [], "reverse": []}
results = {"original": [], "updown": [], "reverse": []}
averages = {"original": [], "updown": [], "reverse": []}
std_devs = {"original": [], "updown": [], "reverse": []}

num_vertices = 50

# Iterate over increasing number of edges
for num_edges in range(150, 200, 5):
    # Temporary storage for multiple instances
    temp_results = {"original": [], "updown": [], "reverse": []}

    # Iterate for 10 instances
    for _ in range(4):
        # Generate a graph with the given number of edges
        G = gen_erdos_renyi_graph_single_component_gt(num_vertices, num_edges, seed=51 + _)
        edges = [(e.source(), e.target()) for e in G.edges()]
        if edges is None:
            print(f"Failed to generate graph for num_vertices={num_vertices}, num_edges={num_edges}")
            continue  # Skip this iteration if edges is None
        g = gt.Graph(directed=False)
        g.add_edge_list(edges)
        original_layout = list(range(num_vertices))

        # Compute the timesteps for the original layout
        original_timesteps = timesteps_for_linear_ancilla_bus_graph_tool(g, original_layout)
        temp_results["original"].append(original_timesteps)

        # Compute the timesteps for each strategy
        for strategy_name in ["updown", "reverse"]:
            levels = globals()[f"generate_{strategy_name}"](num_vertices)
            optimized_layout = NGAopt_layout_graph_tool(g, levels)
            timesteps = timesteps_for_linear_ancilla_bus_graph_tool(g, optimized_layout)
            temp_results[strategy_name].append(timesteps)
    # Store average and standard deviation for each strategy
    for strategy_name in ["original", "updown", "reverse"]:
        averages[strategy_name].append(np.mean(temp_results[strategy_name]))
        std_devs[strategy_name].append(np.std(temp_results[strategy_name]))

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
