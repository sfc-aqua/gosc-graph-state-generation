import cProfile
import pstats
from io import StringIO
import networkx as nx
import numpy as np


# edge_weight calculation
def total_edge_weight(g, layout):
    total_weight = 0
    for edge in g.edges(data=False):
        # Weight of an edge is the number of nodes it travels over
        weight = abs(layout.index(edge[0]) - layout.index(edge[1])) - 1
        total_weight += weight
    return total_weight


def total_edge_weight_with_dict(g, layout_dict):
    total_weight = 0
    for edge in g.edges(data=False):
        # Weight of an edge is the number of nodes it travels over
        weight = abs(layout_dict[edge[0]] - layout_dict[edge[1]]) - 1
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
    node_dict = {node: i for i, node in enumerate(nodes)}
    best_layout = nodes[:]
    best_weight = total_edge_weight_with_dict(g, node_dict)

    for level in levels:
        while True:
            weight_change = False
            for i in range(level, n):
                if i + 1 <= n:
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

                    new_weight = total_edge_weight_with_dict(g, node_dict)
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


def run_experiment():
    strategies = {
        "updown": [],
        "reverse": [],
    }

    results = {"original": [], "updown": [], "reverse": []}
    averages = {"original": [], "updown": [], "reverse": []}
    std_devs = {"original": [], "updown": [], "reverse": []}

    # Number of vertices is fixed at 10
    num_vertices = 50

    # Iterate over a reduced range of number of edges
    for num_edges in range(120, 200, 5):
        # Temporary storage for multiple instances
        temp_results = {"original": [], "updown": [], "reverse": []}

        # Iterate for a reduced number of instances
        for _ in range(2):
            # Generate a graph with the given number of edges
            edges = gen_erdos_renyi_graph_single_component(num_vertices, num_edges, seed=51 + _)
            g = nx.MultiDiGraph()
            g.add_edges_from(edges)
            original_layout = list(range(num_vertices))
            original_layout_dict = {node: idx for idx, node in enumerate(original_layout)}

            # Compute the timesteps for the original layout
            original_timesteps = timesteps_for_linear_ancilla_bus(g, original_layout)
            temp_results["original"].append(original_timesteps)

            # Compute the timesteps for each strategy
            for strategy_name in ["updown", "reverse"]:
                levels = globals()[f"generate_{strategy_name}"](num_vertices)
                optimized_layout = NGAopt_layout(g, levels)
                optimized_layout_dict = {node: idx for idx, node in enumerate(optimized_layout)}
                timesteps = timesteps_for_linear_ancilla_bus(g, optimized_layout)
                temp_results[strategy_name].append(timesteps)
        # Store average and standard deviation for each strategy
        for strategy_name in ["original", "updown", "reverse"]:
            averages[strategy_name].append(np.mean(temp_results[strategy_name]))
            std_devs[strategy_name].append(np.std(temp_results[strategy_name]))


# Use cProfile to profile the reduced run_experiment function
pr = cProfile.Profile()
pr.enable()
run_experiment()
pr.disable()

# Store the stats in a StringIO to display it neatly
s = StringIO()
ps = pstats.Stats(pr, stream=s).sort_stats("cumulative")
ps.print_stats()
profiling_output = s.getvalue()

print(profiling_output)
