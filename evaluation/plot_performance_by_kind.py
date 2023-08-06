import sys

sys.path.append("../")

import warnings
import csv
import matplotlib.pyplot as plt

import networkx as nx

from src.graph_state_generation.optimizers import (
    approximate_static_stabilizer_reduction,
    fast_maximal_independent_set_stabilizer_reduction,
    greedy_stabilizer_measurement_scheduler,
    random_mapper,
    min_cut_mapper,
)
from src.graph_state_generation.substrate_scheduler import TwoRowSubstrateScheduler

warnings.filterwarnings("ignore", category=UserWarning)

paras = {
    "axes.labelsize": 23,
    "axes.titlesize": 23,
    "xtick.labelsize": 21,
    "ytick.labelsize": 22,
    "legend.fontsize": 21,
}
plt.rcParams.update(paras)
plt.rcParams["font.sans-serif"] = ["Arial"]

l_color = [
    "#967AB6",
    "#82D1F4",
    "#E2CB8E",
    "#666469",
]


def run_compiler(graph, mapper):
    compiler = TwoRowSubstrateScheduler(
        graph,
        pre_mapping_optimizer=fast_maximal_independent_set_stabilizer_reduction,
        node_to_patch_mapper=mapper,
        stabilizer_scheduler=greedy_stabilizer_measurement_scheduler,
    )
    compiler.run()
    return [compiler.input_graph.number_of_nodes(), len(compiler.measurement_steps)]


def test_by_kind(graph_type, graph_size=100, step=10, mapper=min_cut_mapper):
    """
    Parameters:
    - graph_type: Available graph types: star, line, random_tree, complete.
    - graph size: The number of vertices in the largest graph to be tested.
    - step: The number of vertices to increase at each step.
    - mapper: The mapper to be compared with the random mapper.
    """

    results = []
    for i in range(10, graph_size + 1, step):
        if graph_type == "star":
            graph = nx.star_graph(i)
        elif graph_type == "line":
            graph = nx.path_graph(i)
        elif graph_type == "random_tree":
            random_seed = 10
            graph = nx.random_tree(i, seed=random_seed)
        elif graph_type == "complete":
            graph = nx.complete_graph(i)

        # Test with random mapper
        result_random = run_compiler(graph, random_mapper)
        result_mapper = run_compiler(graph, mapper)
        # Append results to the list
        results.append(result_random + [result_mapper[1]])
    # Save the results to a CSV file
    with open(f"results/{graph_type}_{graph_size}.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(results)
    # Plot the results
    x = range(10, graph_size + 1, step)
    # plt.style.use("ggplot")
    plt.figure(figsize=(8, 6))
    before = [x[0] for x in results]
    random = [x[1] for x in results]
    min_map = [x[2] for x in results]

    plt.plot(x, before, "+-", color=l_color[2], label="Naive Time Steps")
    plt.plot(x, random, "o-", color=l_color[0], label="Random Mapper")
    plt.plot(x, min_map, "*-", color=l_color[1], label="MinCut Mapper")

    plt.xlabel("Number of Vertices")
    plt.ylabel("Time step(s)")
    plt.legend(loc="upper left")
    plt.savefig(f"results/{graph_type}_{graph_size}.png")
