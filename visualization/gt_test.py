import graph_tool.all as gt
import matplotlib.pyplot as plt
import numpy as np
import random


# graph-tool version
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


def total_edge_weight_with_dict_graph_tool(g, layout):
    total_weight = 0
    for edge in g.edges():
        weight = abs(layout.index(int(edge.source())) - layout.index(int(edge.target()))) - 1
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


"""
edges = [
    (0, 7),
    (1, 6),
    (2, 0),
    (2, 3),
    (2, 7),
    (3, 5),
    (4, 8),
    (4, 3),
    (7, 6),
    (8, 3),
    (8, 7),
    (9, 3),
    (9, 6),
    (9, 4),
    (9, 0),
]
g = gt.Graph(directed=False)
g.add_edge_list(edges)
num_vertices = 10
levels = generate_reverse(num_vertices)
optimized_layout = NGAopt_layout_graph_tool(g, levels)
# Calculate timesteps
timesteps = timesteps_for_linear_ancilla_bus_graph_tool(g, optimized_layout)
print(optimized_layout, timesteps)
"""
strategies = ["original", "updown", "reverse"]

results = {strategy: {"num_edges": [], "timesteps": []} for strategy in strategies}

num_vertices = 100

# Iterate over increasing number of edges
for num_edges in range(250, 800, 10):
    # Iterate for _ instances
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
        results["original"]["num_edges"].append(num_edges)
        results["original"]["timesteps"].append(original_timesteps)

        # Compute the timesteps for each strategy
        for strategy_name in ["updown", "reverse"]:
            levels = globals()[f"generate_{strategy_name}"](num_vertices)
            optimized_layout = NGAopt_layout_graph_tool(g, levels)
            timesteps = timesteps_for_linear_ancilla_bus_graph_tool(g, optimized_layout)
            results[strategy_name]["num_edges"].append(num_edges)
            results[strategy_name]["timesteps"].append(timesteps)

plt.figure(figsize=(10, 6))
plt.scatter(
    results["original"]["num_edges"],
    results["original"]["timesteps"],
    label="original",
    marker="o",
)
plt.scatter(
    results["updown"]["num_edges"],
    results["updown"]["timesteps"],
    label="updown",
    marker="^",
)
plt.scatter(
    results["reverse"]["num_edges"],
    results["reverse"]["timesteps"],
    label="reverse",
    marker="*",
)
plt.xlabel("Number of Edges")
plt.ylabel("Time Steps")
plt.title("Optimization Effect of Different Level List Strategies")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
