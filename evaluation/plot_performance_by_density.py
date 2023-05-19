import sys

sys.path.append("../")

import math
import numpy as np

import warnings
import csv
import matplotlib.pyplot as plt

import networkx as nx
import re

from src.graph_state_generation.optimizers import (
    fast_maximal_independent_set_stabilizer_reduction,
    greedy_stabilizer_measurement_scheduler,
    random_mapper,
    min_cut_mapper,
)
from src.graph_state_generation.substrate_scheduler import TwoRowSubstrateScheduler

warnings.filterwarnings("ignore", category=UserWarning)

paras = {
    "axes.labelsize": 20,
    "axes.titlesize": 21,
    "xtick.labelsize": 17,
    "ytick.labelsize": 18,
    "legend.fontsize": 17,
}
plt.rcParams.update(paras)
plt.rcParams["font.sans-serif"] = ["Arial"]

l_color = [
    "#967AB6",
    "#82D1F4",
    "#E2CB8E",
    "#666469",
]


warnings.filterwarnings("ignore", category=UserWarning)


def gen_erdos_renyi_graph_single_component(n, m, seed=51):
    """
    Generate a random graph with a single connected component.
    """
    try:
        for i in range(5000):
            G = nx.gnm_random_graph(n, m, seed)
            if nx.number_connected_components(G) == 1:
                return G
    except Exception as e:
        print(f"Failed to generate a connected graph: {e}")
    return None


def run_compiler(graph, mapper):
    """
    Run the compiler on the provided graph.
    """
    compiler = TwoRowSubstrateScheduler(
        graph,
        pre_mapping_optimizer=fast_maximal_independent_set_stabilizer_reduction,
        node_to_patch_mapper=mapper,
        stabilizer_scheduler=greedy_stabilizer_measurement_scheduler,
    )
    compiler.run()
    return [compiler.input_graph.number_of_nodes(), len(compiler.measurement_steps)]


def evaluate_graphs_by_density(
    graph_size, start_edges, iterations, step, mapper=min_cut_mapper, seed=10
):
    """
    Evaluate the performance of the compiler on random trees.
    """
    all_result = {}
    for num in range(iterations):
        result = []
        for edges in range(start_edges, math.floor(graph_size * (graph_size - 1) / 2), step):
            graph = gen_erdos_renyi_graph_single_component(graph_size, edges, seed + num)

            result_random = run_compiler(graph, random_mapper)
            result_mapper = run_compiler(graph, mapper)
            # Append results to the list
            result.append(result_random + [result_mapper[1]])
        all_result[num] = result
    with open(f"results/density_{graph_size}.csv", "w", newline="") as file:
        # create the csv writer
        writer = csv.writer(file)
        # write a row to the csv file
        for i in all_result.keys():
            writer.writerow(all_result[i])
    return f"results/density_{graph_size}.csv"


def plot_from_file(filename, start_edges, step):
    """
    Generate a plot from the results file.
    """
    with open(filename, "r") as file:
        data = list(csv.reader(file, delimiter=","))
    num_instances = len(data)
    random_results = [[int(entry.split(" ")[1].replace(",", "")) for entry in row] for row in data]
    min_results = [[int(entry.split(" ")[2].replace("]", "")) for entry in row] for row in data]
    graph_size = [[int(re.sub("\[|,", "", entry.split(" ")[0])) for entry in row] for row in data][0][
        0
    ]
    average_random = [sum(col) / num_instances for col in zip(*random_results)]
    average_min = [sum(col) / num_instances for col in zip(*min_results)]
    std_dev_random = [np.std(col) for col in zip(*random_results)]
    std_dev_min = [np.std(col) for col in zip(*min_results)]

    x_values = list(range(start_edges, math.floor(graph_size * (graph_size - 1) / 2), step))
    densities = [str(round(i / (graph_size * (graph_size - 1) / 2), 2)) for i in x_values]
    naive_time_steps = [graph_size for _ in x_values]
    # plt.style.use("ggplot")
    plt.figure(figsize=(8, 6))
    plt.plot(x_values, naive_time_steps, "o-", color=l_color[2], label="Naive Time Steps")
    plt.plot(
        x_values, [float(i) for i in average_random], "+-", color=l_color[0], label="Random Mapper"
    )
    plt.errorbar(
        x_values,
        [float(i) for i in average_random],
        yerr=[i for i in std_dev_random],
        color=l_color[0],
        capsize=4,
    )
    plt.plot(x_values, [float(i) for i in average_min], "*-", color=l_color[1], label="MinCut Mapper")
    plt.errorbar(
        x_values,
        [float(i) for i in average_min],
        yerr=[float(i) for i in std_dev_min],
        color=l_color[1],
        capsize=4,
        fmt=".",
    )
    spa = graph_size * math.log(graph_size)
    den = graph_size * graph_size / math.log(graph_size)
    plt.axvline(spa, color=l_color[3], linestyle="--", label="$|E|=nlogn$")
    plt.axvline(den, color="r", linestyle="--", label="$|E|=n^{2}/logn$")
    plt.title("Performance Test on Different Density")
    plt.xlabel("Graph Density")
    plt.ylabel("Time step(s)")
    plt.xticks(x_values, densities)
    plt.legend(loc="lower right")
    # plt.grid(True)
    plt.savefig(f"results/density_{graph_size}.png")


def test_by_density(graph_size=100, start_edges=300, iterations=2, step=300, mapper=min_cut_mapper):
    file = evaluate_graphs_by_density(graph_size, start_edges, iterations, step, mapper)
    plot_from_file(file, start_edges, step)


test_by_density(graph_size=100, start_edges=300, iterations=2, step=500, mapper=min_cut_mapper)
