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
    if_connected = 0
    for i in range(3000):
        G = nx.gnm_random_graph(n, m, seed)
        if_connected = nx.number_connected_components(G)
        if if_connected == 1:
            break
    if if_connected == 1:
        return G
    else:
        return None


def test_random_tree(graph_size, start_edges, iterations, step, mapper=min_cut_mapper):
    all_result = {}
    for num in range(0, iterations):
        result = []
        random_seed = 10
        for edges in range(start_edges, math.floor(graph_size * (graph_size - 1) / 2), step):
            graph = gen_erdos_renyi_graph_single_component(graph_size, edges, random_seed + num)

            compiler = TwoRowSubstrateScheduler(
                graph,
                pre_mapping_optimizer=fast_maximal_independent_set_stabilizer_reduction,
                node_to_patch_mapper=random_mapper,
                stabilizer_scheduler=greedy_stabilizer_measurement_scheduler,
            )
            compiler.run()
            compiler_map = TwoRowSubstrateScheduler(
                graph,
                pre_mapping_optimizer=fast_maximal_independent_set_stabilizer_reduction,
                node_to_patch_mapper=mapper,
                stabilizer_scheduler=greedy_stabilizer_measurement_scheduler,
            )
            compiler_map.run()
            result.append(
                [
                    compiler.input_graph.number_of_nodes(),
                    len(compiler.measurement_steps),
                    len(compiler_map.measurement_steps),
                ]
            )
        all_result[num] = result
    with open(f"density_{graph_size}.csv", "w", newline="") as file:
        # create the csv writer
        writer = csv.writer(file)
        # write a row to the csv file
        for i in all_result.keys():
            writer.writerow(all_result[i])


def plot_from_file(filename, start_edges, step):
    random = []
    min = []
    num_instances = 0
    with open(filename, "r") as file:
        reader = csv.reader(file, delimiter=",")
        for row in reader:
            num_instances += 1
            row_random = []
            row_min = []
            for i in row:
                li = list(i.split(" "))
                row_random.append(int(li[1].replace(",", "")))
                graph_size = int(re.sub("\[|,", "", li[0]))
                row_min.append(int(li[2].replace("]", "")))
            random.append(row_random)
            min.append(row_min)
    sum_random = {}
    sum_min = {}
    var_random = {}
    var_min = {}
    for i in random:
        for j in range(len(i)):
            if j not in sum_random.keys():
                sum_random[j] = 0
            sum_random[j] += i[j]
    for i in min:
        for j in range(len(i)):
            if j not in sum_min.keys():
                sum_min[j] = 0
            sum_min[j] += i[j]

    for i in sum_min.keys():
        sum_min[i] = sum_min[i] / num_instances
    for i in sum_random.keys():
        sum_random[i] = sum_random[i] / num_instances

    for i in random:
        for j in range(len(i)):
            if j not in var_random.keys():
                var_random[j] = []
            var_random[j].append(i[j])
    for i in min:
        for j in range(len(i)):
            if j not in var_min.keys():
                var_min[j] = []
            var_min[j].append(i[j])

    for i in var_min.keys():
        var_min[i] = np.std(var_min[i])
    for i in var_random.keys():
        var_random[i] = np.std(var_random[i])
    x = range(start_edges, math.floor(graph_size * (graph_size - 1) / 2), step)
    print(x)

    density = [str(round(i / (graph_size * (graph_size - 1) / 2), 2)) for i in x]
    # plt.style.use("ggplot")
    before = [graph_size for i in x]
    print(before)
    plt.figure(figsize=(8, 6))
    plt.plot(x, before, "o-", color=l_color[2], label="Naive Time Steps")
    plt.plot(
        x, [float(i) for i in sum_random.values()], "+-", color=l_color[0], label="Random Mapper"
    )
    plt.errorbar(
        x,
        [float(i) for i in sum_random.values()],
        yerr=[float(i) for i in var_random.values()],
        color=l_color[0],
        capsize=4,
    )
    plt.plot(x, [float(i) for i in sum_min.values()], "*-", color=l_color[1], label="MinCut Mapper")
    plt.errorbar(
        x,
        [float(i) for i in sum_min.values()],
        yerr=[float(i) for i in var_min.values()],
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
    plt.xticks(x, density)
    plt.legend(loc="lower right")
    # plt.grid(True)
    plt.savefig(f"density_{graph_size}.png")


def test_by_density(graph_size, start_edges, iterations, step, mapper=min_cut_mapper):
    test_random_tree(graph_size, start_edges, iterations, step, mapper)
    plot_from_file("density_10.csv", start_edges, step)

