import cProfile
import pstats
from io import StringIO
import graph_tool.all as gt
import random


def total_edge_weight_with_dict_graph_tool(g, layout):
    layout_dict = {node: index for index, node in enumerate(layout)}
    total_weight = 0
    for edge in g.edges():
        source_index = layout_dict[int(edge.source())]
        target_index = layout_dict[int(edge.target())]
        weight = abs(source_index - target_index) - 1
        total_weight += weight
    return total_weight


def timesteps_for_linear_ancilla_bus_graph_tool(g, layout):
    timesteps_list = []
    for u_index, u in enumerate(layout):
        touching_edges = [
            edge
            for edge in g.edges()
            if (
                layout.index(int(edge.source())) < u_index
                and layout.index(int(edge.target())) > u_index
            )
            or (
                layout.index(int(edge.source())) > u_index
                and layout.index(int(edge.target())) < u_index
            )
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


def NGAopt_layout_graph_tool(g, levels):
    nodes = list(range(g.num_vertices()))
    n = len(nodes)
    best_layout = nodes[:]
    best_weight = total_edge_weight_with_dict_graph_tool(g, best_layout)

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

                    new_weight = total_edge_weight_with_dict_graph_tool(g, nodes)
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


def run_experiment():
    strategies = ["original", "updown", "reverse"]

    results = {strategy: {"num_edges": [], "timesteps": []} for strategy in strategies}

    num_vertices = 50

    # Iterate over increasing number of edges
    for num_edges in range(120, 200, 5):
        # Iterate for _ instances
        for _ in range(2):
            # Generate a graph with the given number of edges
            G = gen_erdos_renyi_graph_single_component_gt(num_vertices, num_edges, seed=51 + _)
            edges = [(e.source(), e.target()) for e in G.edges()]
            if edges is None:
                print(
                    f"Failed to generate graph for num_vertices={num_vertices}, num_edges={num_edges}"
                )
                continue  # Skip this iteration if edges is None
            g = gt.Graph(directed=False)
            g.add_edge_list(edges)
            original_layout = list(range(num_vertices))

            # Compute the timesteps for the original layout
            original_timesteps = timesteps_for_linear_ancilla_bus_graph_tool(g, original_layout)
            results["original"]["num_edges"].append(num_edges)
            results["original"]["timesteps"].append(original_timesteps)

            # Compute the timesteps for each strategy
            for strategy_name in ["updown", "reverse"]:
                levels = globals()[f"generate_{strategy_name}"](num_vertices)
                optimized_layout = NGAopt_layout_graph_tool(g, levels)
                timesteps = timesteps_for_linear_ancilla_bus_graph_tool(g, optimized_layout)
                results[strategy_name]["num_edges"].append(num_edges)
                results[strategy_name]["timesteps"].append(timesteps)


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
