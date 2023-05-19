import sys

sys.path.append("../")
import math
import numpy as np
import re


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
from typing import List


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


def run_compiler(graph, mapper) -> List[int]:
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


def test_random_tree(
    iterations,
    start_size,
    end_size,
    step,
    density,
    end_size_mapper,
    mapper=min_cut_mapper,
    seed=51,
):
    all_result = {}
    for num in range(0, iterations):
        result = []
        for i in range(start_size, end_size + 1, step):
            if density=="dense":
                graph = gen_erdos_renyi_graph_single_component(i, i * i / math.log(i), seed + num)
            elif density=="sparse":
                graph = gen_erdos_renyi_graph_single_component(i, i*math.log(i), seed + num)

            result_random = run_compiler(graph, random_mapper)

            if i < end_size_mapper + 1:
                result_mapper = run_compiler(graph, mapper)
                # Append results to the list
                result.append(result_random + [result_mapper[1]])
            else:
                result.append(result_random)
        all_result[num] = result
    filename = f"results/performance_scale_{end_size}.csv"
    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        for i in all_result.keys():
            writer.writerow(all_result[i])
    return filename


def plot_from_csv(filename: str, start_size: int, end_size: int, step: int, mapper_size: int):
    with open(filename, "r") as file:
        data = list(csv.reader(file, delimiter=","))

    num_instances = len(data)
    random_results = [[int(re.sub("\]|,", "", entry.split(" ")[1])) for entry in row] for row in data]
    min_results = [
        [
            int(re.sub("\]|,", "", entry.split(" ")[2]))
            for entry in row[: math.floor(mapper_size / step)]
        ]
        for row in data
    ]
    naive_time_steps = [
        [int(re.sub("\[|,", "", entry.split(" ")[0])) for entry in row] for row in data
    ]

    average_random = [sum(col) / num_instances for col in zip(*random_results)]
    average_min = [sum(col) / num_instances for col in zip(*min_results)]
    std_dev_random = [np.std(col) for col in zip(*random_results)]
    std_dev_min = [np.std(col) for col in zip(*min_results)]

    x_values = list(range(start_size, end_size + 1, step))
    # density=[str(round(i/(100*(100-1)/2),2)) for i in x]
    # plt.style.use("ggplot")
    plt.figure(figsize=(8, 6))
    before = naive_time_steps[0]

    plt.plot(x_values, before, "+-", color=l_color[2], label="Naive Time Steps")
    plt.plot(x_values, average_random, "o-", color=l_color[0], label="Random Mapper")
    #plt.errorbar(x_values, average_random, yerr = std_dev_random,color=l_color[0],capsize=4)
    plt.plot(
        x_values[0 : math.floor(mapper_size / step)],
        average_min,
        "*-",
        color=l_color[1],
        label="MinCut Mapper",
    )
    #plt.errorbar(x_values[0 : math.floor(mapper_size / step)], average_min, yerr = std_dev_min,color=l_color[0],capsize=4)

    plt.axvline(1000, color="r", linestyle="--", label="1000 Vertices")
    # plt.title("Performance Test on Different Graph Size")
    plt.xlabel("Number of Vertices")
    plt.ylabel("Time step(s)")
    plt.legend(loc="lower right")
    # plt.grid(True)
    plt.savefig(f"results/performance_scale_{end_size}.png")


def test_by_scale(start_size, end_size, iterations, step, end_size_mapper, density, mapper=min_cut_mapper):
    file = test_random_tree(
        iterations=iterations,
        start_size=start_size,
        end_size=end_size,
        step=step,
        density=density,
        end_size_mapper=end_size_mapper,
        mapper=mapper
    )
    plot_from_csv(file, start_size, end_size, step, end_size_mapper)
